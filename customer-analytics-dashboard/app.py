# 客户分析看板
# 基于 Streamlit + Plotly 的客户细分与留存分析

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="客户分析看板",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #333;
    }
    .stMetric {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# 生成示例客户数据
@st.cache_data
def generate_customer_data():
    """生成示例客户数据"""
    np.random.seed(42)
    
    # 生成客户数据
    customers = []
    customer_ids = [f'CUST{i:04d}' for i in range(1, 1001)]
    
    for customer_id in customer_ids:
        # RFM指标
        recency = np.random.randint(1, 365)  # 最近购买天数
        frequency = np.random.randint(1, 50)  # 购买频率
        monetary = np.random.randint(100, 10000)  # 消费金额
        
        # 客户属性
        registration_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 700))
        last_purchase = datetime.now() - timedelta(days=recency)
        
        # 地理位置
        cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安']
        city = np.random.choice(cities)
        
        # 客户分层
        if monetary > 5000 and frequency > 20:
            segment = '高价值客户'
        elif monetary > 2000 and frequency > 10:
            segment = '重要保持客户'
        elif recency < 30:
            segment = '新客户'
        elif recency > 180:
            segment = '流失风险客户'
        else:
            segment = '一般客户'
        
        customers.append({
            'customer_id': customer_id,
            'recency': recency,
            'frequency': frequency,
            'monetary': monetary,
            'registration_date': registration_date,
            'last_purchase': last_purchase,
            'city': city,
            'segment': segment,
            'ltv': monetary * (frequency / 10)  # 生命周期价值估算
        })
    
    return pd.DataFrame(customers)

# 生成留存数据
@st.cache_data
def generate_retention_data():
    """生成留存数据"""
    months = pd.date_range('2023-01', '2024-12', freq='M')
    retention_data = []
    
    for i, month in enumerate(months):
        cohort_size = np.random.randint(100, 200)
        for j in range(min(12, len(months) - i)):
            retention_rate = max(0, 100 - j * 8 + np.random.randint(-5, 5))
            retention_data.append({
                'cohort_month': month.strftime('%Y-%m'),
                'period': j,
                'retention_rate': retention_rate,
                'users': int(cohort_size * retention_rate / 100)
            })
    
    return pd.DataFrame(retention_data)

# 加载数据
df_customers = generate_customer_data()
df_retention = generate_retention_data()

# 侧边栏
with st.sidebar:
    st.title("🔧 筛选设置")
    
    # 客户分层筛选
    selected_segments = st.multiselect(
        "客户分层",
        options=df_customers['segment'].unique(),
        default=df_customers['segment'].unique()
    )
    
    # 城市筛选
    selected_cities = st.multiselect(
        "城市",
        options=df_customers['city'].unique(),
        default=df_customers['city'].unique()
    )
    
    # R值范围
    recency_range = st.slider(
        "最近购买天数 (R)",
        min_value=int(df_customers['recency'].min()),
        max_value=int(df_customers['recency'].max()),
        value=(1, 365)
    )
    
    # M值范围
    monetary_range = st.slider(
        "消费金额 (M)",
        min_value=int(df_customers['monetary'].min()),
        max_value=int(df_customers['monetary'].max()),
        value=(100, 10000)
    )

# 数据筛选
filtered_df = df_customers[
    (df_customers['segment'].isin(selected_segments)) &
    (df_customers['city'].isin(selected_cities)) &
    (df_customers['recency'] >= recency_range[0]) &
    (df_customers['recency'] <= recency_range[1]) &
    (df_customers['monetary'] >= monetary_range[0]) &
    (df_customers['monetary'] <= monetary_range[1])
]

# 主页面
st.title("👥 客户分析看板")
st.markdown("客户细分、留存分析与生命周期价值评估")

# 标签页
tab1, tab2, tab3, tab4 = st.tabs(["📊 概览", "🎯 RFM分析", "📈 留存分析", "🗺️ 地理分布"])

# Tab 1: 概览
with tab1:
    st.header("客户数据概览")
    
    # KPI指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="总客户数",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df_customers):,}"
        )
    
    with col2:
        avg_monetary = filtered_df['monetary'].mean()
        st.metric(
            label="平均消费",
            value=f"¥{avg_monetary:,.0f}"
        )
    
    with col3:
        avg_frequency = filtered_df['frequency'].mean()
        st.metric(
            label="平均购买次数",
            value=f"{avg_frequency:.1f}"
        )
    
    with col4:
        total_ltv = filtered_df['ltv'].sum()
        st.metric(
            label="总LTV",
            value=f"¥{total_ltv:,.0f}"
        )
    
    st.divider()
    
    # 客户分层分布
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("客户分层分布")
        segment_counts = filtered_df['segment'].value_counts().reset_index()
        segment_counts.columns = ['segment', 'count']
        
        fig_pie = px.pie(
            segment_counts,
            values='count',
            names='segment',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("消费金额分布")
        fig_hist = px.histogram(
            filtered_df,
            x='monetary',
            nbins=30,
            color='segment',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="消费金额",
            yaxis_title="客户数"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# Tab 2: RFM分析
with tab2:
    st.header("RFM客户细分分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("RFM散点图")
        fig_scatter = px.scatter(
            filtered_df,
            x='recency',
            y='monetary',
            size='frequency',
            color='segment',
            hover_data=['customer_id'],
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="最近购买天数 (R)",
            yaxis_title="消费金额 (M)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("RFM热力图")
        # 创建RFM评分
        filtered_df['R_score'] = pd.qcut(filtered_df['recency'], 5, labels=[5,4,3,2,1])
        filtered_df['F_score'] = pd.qcut(filtered_df['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        filtered_df['M_score'] = pd.qcut(filtered_df['monetary'], 5, labels=[1,2,3,4,5])
        
        rfm_heatmap = filtered_df.groupby(['R_score', 'F_score']).size().reset_index(name='count')
        rfm_pivot = rfm_heatmap.pivot(index='R_score', columns='F_score', values='count').fillna(0)
        
        fig_heatmap = px.imshow(
            rfm_pivot,
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig_heatmap.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title="消费频率 (F)",
            yaxis_title="最近购买 (R)"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.divider()
    
    # RFM详细表格
    st.subheader("高价值客户TOP 20")
    top_customers = filtered_df.nlargest(20, 'ltv')[['customer_id', 'recency', 'frequency', 'monetary', 'ltv', 'segment', 'city']]
    st.dataframe(
        top_customers.style.background_gradient(subset=['monetary', 'ltv'], cmap='Reds'),
        use_container_width=True
    )

# Tab 3: 留存分析
with tab3:
    st.header("客户留存分析")
    
    # 留存热力图
    st.subheader("留存率热力图")
    retention_pivot = df_retention.pivot(index='cohort_month', columns='period', values='retention_rate')
    
    fig_retention = px.imshow(
        retention_pivot,
        color_continuous_scale='Blues',
        aspect='auto',
        labels=dict(x="周期 (月)", y=" cohort月份", color="留存率%")
    )
    fig_retention.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_retention, use_container_width=True)
    
    st.divider()
    
    # 留存曲线
    st.subheader("平均留存曲线")
    avg_retention = df_retention.groupby('period')['retention_rate'].mean().reset_index()
    
    fig_line = px.line(
        avg_retention,
        x='period',
        y='retention_rate',
        markers=True,
        line_shape='spline'
    )
    fig_line.update_traces(line_color='#FF4B4B', marker_color='#FF4B4B')
    fig_line.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="周期 (月)",
        yaxis_title="留存率 (%)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Tab 4: 地理分布
with tab4:
    st.header("客户地理分布")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("城市分布")
        city_data = filtered_df.groupby('city').agg({
            'customer_id': 'count',
            'monetary': 'sum'
        }).reset_index()
        city_data.columns = ['city', 'customer_count', 'total_revenue']
        
        fig_city = px.bar(
            city_data.sort_values('customer_count', ascending=True),
            x='customer_count',
            y='city',
            orientation='h',
            color='total_revenue',
            color_continuous_scale='Reds'
        )
        fig_city.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_city, use_container_width=True)
    
    with col2:
        st.subheader("城市消费占比")
        fig_city_pie = px.pie(
            city_data,
            values='total_revenue',
            names='city',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_city_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_city_pie, use_container_width=True)
    
    st.divider()
    
    # 城市详细数据
    st.subheader("城市详细数据")
    city_summary = filtered_df.groupby('city').agg({
        'customer_id': 'count',
        'monetary': ['sum', 'mean'],
        'frequency': 'mean'
    }).round(2)
    city_summary.columns = ['客户数', '总消费', '平均消费', '平均购买次数']
    city_summary = city_summary.sort_values('总消费', ascending=False)
    st.dataframe(city_summary, use_container_width=True)

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>客户分析看板 | 数据更新时间: {}</p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

if __name__ == '__main__':
    print("🚀 客户分析看板已启动")
    print("📊 访问地址: http://localhost:8501")
