# 销售智能分析看板
# 基于 Python + Plotly Dash 的电商销售数据分析平台

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 初始化 Dash 应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "抖音电商销售智能分析"

# 生成示例数据
def generate_sample_data():
    """生成示例销售数据"""
    np.random.seed(42)
    
    # 日期范围
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # 商品类别
    categories = ['服装', '美妆', '数码', '家居', '食品', '配饰']
    
    # 生成订单数据
    data = []
    for date in dates:
        daily_orders = np.random.randint(50, 200)
        for _ in range(daily_orders):
            category = np.random.choice(categories)
            base_amount = {
                '服装': 150, '美妆': 200, '数码': 800,
                '家居': 300, '食品': 80, '配饰': 100
            }[category]
            
            amount = base_amount * np.random.uniform(0.5, 2.0)
            quantity = np.random.randint(1, 5)
            
            data.append({
                'order_date': date,
                'category': category,
                'amount': round(amount, 2),
                'quantity': quantity,
                'customer_id': f'CUST{np.random.randint(1000, 9999)}',
                'product_name': f'{category}商品{np.random.randint(1, 50)}'
            })
    
    return pd.DataFrame(data)

# 加载数据
df = generate_sample_data()

# 计算KPI指标
def calculate_kpis(df, start_date=None, end_date=None):
    """计算关键绩效指标"""
    if start_date and end_date:
        mask = (df['order_date'] >= start_date) & (df['order_date'] <= end_date)
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    total_sales = filtered_df['amount'].sum()
    total_orders = len(filtered_df)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    total_customers = filtered_df['customer_id'].nunique()
    
    return {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'total_customers': total_customers
    }

# 布局设计
app.layout = dbc.Container([
    # 头部
    dbc.Row([
        dbc.Col([
            html.H1("📊 抖音电商销售智能分析", className="text-center my-4"),
            html.P("实时销售数据分析与可视化平台", className="text-center text-muted")
        ])
    ]),
    
    # 筛选器
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📅 时间筛选", className="card-title"),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date=df['order_date'].min(),
                        end_date=df['order_date'].max(),
                        display_format='YYYY-MM-DD'
                    )
                ])
            ], className="mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🏷️ 商品类别", className="card-title"),
                    dcc.Dropdown(
                        id='category-filter',
                        options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
                        multi=True,
                        placeholder="选择商品类别..."
                    )
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    # KPI 卡片
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💰 总销售额", className="card-title text-center"),
                    html.H2(id='kpi-sales', className="text-center text-success")
                ])
            ], color="dark", inverse=True)
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📦 总订单数", className="card-title text-center"),
                    html.H2(id='kpi-orders', className="text-center text-info")
                ])
            ], color="dark", inverse=True)
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💵 客单价", className="card-title text-center"),
                    html.H2(id='kpi-aov', className="text-center text-warning")
                ])
            ], color="dark", inverse=True)
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("👥 客户数", className="card-title text-center"),
                    html.H2(id='kpi-customers', className="text-center text-primary")
                ])
            ], color="dark", inverse=True)
        ], width=3)
    ], className="mb-4"),
    
    # 图表区域
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📈 销售趋势", className="card-title"),
                    dcc.Graph(id='sales-trend-chart')
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🥧 类别占比", className="card-title"),
                    dcc.Graph(id='category-pie-chart')
                ])
            ])
        ], width=4)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🏆 热销商品 TOP 10", className="card-title"),
                    dcc.Graph(id='top-products-chart')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📊 月度销售对比", className="card-title"),
                    dcc.Graph(id='monthly-comparison-chart')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # 数据表格
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📋 详细数据", className="card-title"),
                    html.Div(id='data-table')
                ])
            ])
        ])
    ])
    
], fluid=True)

# 回调函数
@callback(
    [Output('kpi-sales', 'children'),
     Output('kpi-orders', 'children'),
     Output('kpi-aov', 'children'),
     Output('kpi-customers', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('category-filter', 'value')]
)
def update_kpis(start_date, end_date, categories):
    """更新KPI指标"""
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['order_date'] >= start_date) & 
            (filtered_df['order_date'] <= end_date)
        ]
    
    if categories:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    
    kpis = calculate_kpis(filtered_df)
    
    return (
        f"¥{kpis['total_sales']:,.2f}",
        f"{kpis['total_orders']:,}",
        f"¥{kpis['avg_order_value']:.2f}",
        f"{kpis['total_customers']:,}"
    )

@callback(
    Output('sales-trend-chart', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('category-filter', 'value')]
)
def update_sales_trend(start_date, end_date, categories):
    """更新销售趋势图"""
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['order_date'] >= start_date) & 
            (filtered_df['order_date'] <= end_date)
        ]
    
    if categories:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    
    daily_sales = filtered_df.groupby('order_date')['amount'].sum().reset_index()
    
    fig = px.line(
        daily_sales, 
        x='order_date', 
        y='amount',
        title='日销售额趋势',
        labels={'order_date': '日期', 'amount': '销售额 (¥)'}
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

@callback(
    Output('category-pie-chart', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_category_pie(start_date, end_date):
    """更新类别饼图"""
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['order_date'] >= start_date) & 
            (filtered_df['order_date'] <= end_date)
        ]
    
    category_sales = filtered_df.groupby('category')['amount'].sum().reset_index()
    
    fig = px.pie(
        category_sales,
        values='amount',
        names='category',
        title='商品类别销售占比'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

@callback(
    Output('top-products-chart', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('category-filter', 'value')]
)
def update_top_products(start_date, end_date, categories):
    """更新热销商品图"""
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['order_date'] >= start_date) & 
            (filtered_df['order_date'] <= end_date)
        ]
    
    if categories:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    
    product_sales = filtered_df.groupby('product_name')['amount'].sum().reset_index()
    product_sales = product_sales.nlargest(10, 'amount')
    
    fig = px.bar(
        product_sales,
        x='amount',
        y='product_name',
        orientation='h',
        title='热销商品 TOP 10',
        labels={'amount': '销售额 (¥)', 'product_name': '商品名称'}
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

@callback(
    Output('monthly-comparison-chart', 'figure'),
    [Input('category-filter', 'value')]
)
def update_monthly_comparison(categories):
    """更新月度对比图"""
    filtered_df = df.copy()
    
    if categories:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    
    filtered_df['month'] = filtered_df['order_date'].dt.to_period('M')
    monthly_sales = filtered_df.groupby('month')['amount'].sum().reset_index()
    monthly_sales['month'] = monthly_sales['month'].astype(str)
    
    fig = px.bar(
        monthly_sales,
        x='month',
        y='amount',
        title='月度销售对比',
        labels={'month': '月份', 'amount': '销售额 (¥)'}
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

if __name__ == '__main__':
    print("🚀 启动销售智能分析看板...")
    print("📊 访问地址: http://localhost:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
