# NexusTik 销售智能分析看板
# 基于 Madhav Dashboard 核心逻辑，适配抖音电商数据

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# 数据加载函数 - 支持CSV导入和模拟数据
def load_douyin_data(file_path=None):
    """加载抖音电商数据，支持真实数据导入"""
    if file_path and os.path.exists(file_path):
        # 加载真实数据
        df = pd.read_csv(file_path)
        # 适配抖音电商数据格式
        if '订单日期' in df.columns:
            df['Order Date'] = pd.to_datetime(df['订单日期'])
            df['Amount'] = df['订单金额']
            df['Profit'] = df['订单金额'] * 0.2  # 假设利润率20%
            df['Quantity'] = df['商品数量']
            df['Category'] = df['商品类目']
            df['Sub-Category'] = df['商品名称']
            df['State'] = df['省份']
            df['CustomerName'] = df['买家昵称']
            df['PaymentMode'] = df['支付方式']
    else:
        # 生成模拟数据（保持与原版一致的结构）
        np.random.seed(42)
        n_orders = 5000
        
        categories = ['服装', '美妆', '数码', '家居', '食品']
        states = ['广东', '浙江', '江苏', '山东', '河南', '四川', '湖北', '湖南']
        payment_modes = ['支付宝', '微信支付', '银行卡', '抖音月付']
        
        df = pd.DataFrame({
            'Order ID': [f'DY{str(i).zfill(6)}' for i in range(n_orders)],
            'Order Date': pd.date_range('2024-01-01', periods=n_orders, freq='h'),
            'Amount': np.random.randint(50, 2000, n_orders),
            'Profit': np.random.randint(10, 400, n_orders),
            'Quantity': np.random.randint(1, 5, n_orders),
            'Category': np.random.choice(categories, n_orders),
            'Sub-Category': [f'商品{i}' for i in range(n_orders)],
            'State': np.random.choice(states, n_orders),
            'CustomerName': [f'用户{i}' for i in range(n_orders)],
            'PaymentMode': np.random.choice(payment_modes, n_orders)
        })
    
    # 统一数据格式（与原版一致）
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Month'] = df['Order Date'].dt.strftime('%b')
    df['Quater'] = df['Order Date'].dt.quarter
    
    return df

import os

# 尝试加载数据
try:
    # 优先加载用户上传的数据
    if os.path.exists('data/douyin_orders.csv'):
        df = load_douyin_data('data/douyin_orders.csv')
    else:
        df = load_douyin_data()
except:
    df = load_douyin_data()

# 初始化Dash应用
app = Dash(__name__)
app.title = "NexusTik 销售智能分析"

def kpi_figure(value, title, prefix=""):
    """KPI指标卡片（保持原版样式）"""
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=value,
            title={"text": title, "font": {"size": 14}},
            number={"prefix": prefix, "font": {"size": 28}},
            domain={"x": [0, 1], "y": [0, 1]}
        )
    )
    fig.update_layout(
        height=120,
        margin=dict(l=8, r=8, t=30, b=8),
        paper_bgcolor="white"
    )
    return fig

app.layout = html.Div(children=[
    html.H1("NexusTik 抖音电商销售分析",
            style={"textAlign": "center", "color": "#1D37CAD6"}),
    html.Br(),
    
    # 数据上传
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div(['拖拽或 ', html.A('选择CSV文件')]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px auto'
            },
            multiple=False
        )
    ]),
    
    html.Div([
        "商品类目",
        dcc.Dropdown(id="input_category",
                     options=[{'label': '全部', 'value': "all"}] +
                               [{'label': cat, 'value': cat} for cat in df['Category'].unique()],
                     value="all",
                     clearable=False,
                     style={'textAlign': 'center', 'height': '25px', 'width': '200px', 'margin': '0 auto'})
    ], style={'textAlign': 'center', 'fontSize': 20}),
    html.Br(),
    
    html.Div([
        "季度: ",
        dcc.Dropdown(id="input_quater",
                     options=[{'label': '全年', 'value': 'all'},
                              {'label': 'Q1 (1-3月)', 'value': 1},
                              {'label': 'Q2 (4-6月)', 'value': 2},
                              {'label': 'Q3 (7-9月)', 'value': 3},
                              {'label': 'Q4 (10-12月)', 'value': 4}],
                     value='all',
                     clearable=False,
                     style={'height': '25px', 'width': '200px', 'margin': '0 auto', 'textAlign': 'center'})
    ], style={'textAlign': 'center', 'fontSize': 20}),
    html.Br(), html.Br(),
    
    # KPI指标
    html.Div([
        dcc.Graph(id='total_revenue',
                  config={'displayModeBar': False},
                  style={'width': '24%', 'height': '130px'}),
        dcc.Graph(id='total_profit',
                  config={'displayModeBar': False},
                  style={'width': '24%', 'height': '130px'}),
        dcc.Graph(id='quantity_sold',
                  config={'displayModeBar': False},
                  style={'width': '24%', 'height': '130px'}),
        dcc.Graph(id='aov',
                  config={'displayModeBar': False},
                  style={'width': '24%', 'height': '130px'})
    ], style={'display': 'flex', 'gap': '4px', "justifyContent": "space-between"}),
    html.Br(), html.Br(),
    
    # 图表区域
    html.Div([
        html.Div(html.Img(id='monthly_profit'), style={'width': '50%'}),
        html.Div(dcc.Graph(id='sub_category_profit'), style={'width': '50%'})
    ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='revenue_states'), style={'width': '50%'}),
        html.Div(dcc.Graph(id='category_quantity_sold'), style={'width': '50%'})
    ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='payment_dist'), style={'width': '50%'}),
        html.Div(dcc.Graph(id='top_customers'), style={'width': '50%'})
    ], style={'display': 'flex'})
], style={'backgroundColor': 'white'})

@app.callback([
    Output('total_revenue', 'figure'),
    Output('total_profit', 'figure'),
    Output('quantity_sold', 'figure'),
    Output('aov', 'figure'),
    Output('monthly_profit', 'src'),
    Output('sub_category_profit', 'figure'),
    Output('revenue_states', 'figure'),
    Output('category_quantity_sold', 'figure'),
    Output('payment_dist', 'figure'),
    Output('top_customers', 'figure')],
    Input('input_quater', 'value'),
    Input('input_category', 'value'))

def get_graph(quater, category):
    """核心分析逻辑（保持原版算法）"""
    filtered_df = df.copy()
    
    if quater != 'all':
        filtered_df = filtered_df[filtered_df['Quater'] == quater]
    if category != 'all':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    
    # Total revenue
    total_revenue = filtered_df['Amount'].sum()
    fig1 = kpi_figure(total_revenue, "总销售额", "¥")
    
    # Total Profit
    total_profit = filtered_df['Profit'].sum()
    fig2 = kpi_figure(total_profit, "总利润", "¥")
    
    # Quantity Sold
    quantity_sold = filtered_df['Quantity'].sum()
    fig3 = kpi_figure(quantity_sold, "销售数量")
    
    # Average Order value
    aov = filtered_df['Amount'].sum() / filtered_df['Quantity'].sum() if filtered_df['Quantity'].sum() > 0 else 0
    fig4 = kpi_figure(aov, "客单价", "¥")
    
    # Monthly Profit
    df_month_profit = filtered_df.groupby("Order Month")['Profit'].sum().reset_index()
    df_month_profit['Month_No'] = pd.to_datetime(df_month_profit['Order Month'], format='%b').dt.month
    df_month_profit.sort_values('Month_No', inplace=True)
    df_month_profit.drop("Month_No", axis=1, inplace=True)
    
    plt.figure(figsize=(7.5, 5))
    sns.set_theme(style='ticks')
    bar_color = ["green" if profit >= 0 else "red" for profit in df_month_profit['Profit']]
    sns.barplot(data=df_month_profit, x='Order Month', y="Profit", edgecolor='black', palette=bar_color)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f"¥{int(y/1000)}K"))
    plt.title("月度利润", fontsize=15)
    plt.ylabel("利润")
    plt.xlabel("")
    sns.despine()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    fig5 = f"data:image/png;base64,{encoded}"
    
    # Profit by Sub-category
    df_sub_category_profit = filtered_df.groupby(['Sub-Category'])['Profit'].sum().sort_values(ascending=False).head().reset_index()
    fig6 = px.bar(data_frame=df_sub_category_profit[::-1], x="Profit", y="Sub-Category", template="plotly_white")
    fig6.update_layout(title="商品利润排行", title_x=0.5, xaxis_title="", yaxis_title="")
    fig6.update_traces(marker={'line': {'width': 1, 'color': 'black'}},
                       text=[f"¥{x:,}" for x in df_sub_category_profit['Profit'][::-1]],
                       textposition='inside')
    fig6.update_xaxes(showticklabels=False)
    
    # Category Quantity
    df_category_quantity = filtered_df.groupby('Category')['Quantity'].sum().reset_index()
    fig7 = px.pie(data_frame=df_category_quantity, values='Quantity', names='Category', template='plotly_white')
    fig7.update_layout(title="类目销量分布", title_x=0.5, showlegend=True)
    
    # Top Revenue States
    df_top_revenue_states = filtered_df.groupby('State')['Amount'].sum().sort_values(ascending=False).head().reset_index()
    df_top_revenue_states['Percent'] = df_top_revenue_states['Amount'] / df["Amount"].sum() * 100
    fig8 = px.bar(data_frame=df_top_revenue_states.iloc[::-1], x='Percent', y='State', template='plotly_white')
    fig8.update_layout(title="销售额省份排行", title_x=0.5, xaxis_title="", yaxis_title="")
    fig8.update_traces(marker={'line': {'width': 1, 'color': 'black'}},
                       text=[f"{x:.1f}%" for x in df_top_revenue_states['Percent'][::-1]],
                       textposition='inside')
    fig8.update_xaxes(showticklabels=False)
    
    # Payment Mode Distribution
    df_payment_mode = df["PaymentMode"].value_counts().reset_index()
    fig9 = px.pie(data_frame=df_payment_mode, values='count', names='PaymentMode', template='plotly_white')
    fig9.update_layout(title="支付方式分布", title_x=0.5, showlegend=True)
    
    # Top 5 Customers
    df_top_customers = filtered_df.groupby("CustomerName")['Amount'].sum().sort_values(ascending=False).head().reset_index()
    fig10 = px.bar(data_frame=df_top_customers, x='CustomerName', y='Amount', template="plotly_white")
    fig10.update_layout(title="TOP5客户", title_x=0.5, xaxis_title="", yaxis_title="")
    fig10.update_traces(marker={'line': {'width': 1, 'color': 'black'}},
                        text=[f"¥{x/1000:.1f}K" for x in df_top_customers['Amount']],
                        textposition='outside')
    fig10.update_yaxes(showticklabels=False)
    
    return [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10]

if __name__ == '__main__':
    print("🚀 NexusTik 销售智能分析启动...")
    print("📊 访问地址: http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
