# NexusTik 客户分析看板 - 极简主义设计版
# 基于 Data Storytelling Dashboard 核心逻辑，极简UI重构

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import date, datetime
import warnings
warnings.filterwarnings('ignore')

# ==================== 页面配置 ====================

st.set_page_config(
    page_title="NexusTik 客户分析",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 极简主义CSS注入 ====================

def load_minimalist_css():
    css = """
    <style>
    /* 全局背景 - 纯白 */
    .stApp {
        background: #FFFFFF;
    }
    
    /* 主内容区 */
    .main .block-container {
        background: #FFFFFF;
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* 侧边栏 - 浅灰 */
    [data-testid="stSidebar"] {
        background: #FAFAFA !important;
        border-right: 1px solid #E5E5E5;
    }
    
    [data-testid="stSidebar"] .block-container {
        background: transparent;
        padding: 2rem 1.5rem;
    }
    
    /* 侧边栏文字 */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #1A1A1A !important;
        font-weight: 500;
    }
    
    /* 标题 - 极简黑 */
    h1 {
        color: #1A1A1A;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }
    
    h2 {
        color: #1A1A1A;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.01em;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #1A1A1A;
        font-size: 16px;
        font-weight: 600;
    }
    
    /* 副标题 */
    .subtitle {
        color: #666666;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* KPI卡片 - 极简白底 */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 4px !important;
        padding: 24px !important;
        transition: all 150ms ease;
    }
    
    [data-testid="stMetric"]:hover {
        background: #FAFAFA !important;
        border-color: #D0D0D0 !important;
    }
    
    /* KPI数值 - 大号黑色 */
    [data-testid="stMetricValue"] {
        color: #1A1A1A !important;
        font-size: 28px !important;
        font-weight: 700;
        font-family: -apple-system, monospace;
        letter-spacing: -0.02em;
    }
    
    /* KPI标签 - 灰色小字 */
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
        font-size: 12px !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    
    /* 分隔线 - 极简 */
    hr {
        border: none;
        height: 1px;
        background: #E5E5E5;
        margin: 2rem 0;
    }
    
    /* 数据表格 - 极简 */
    .stDataFrame {
        border: 1px solid #E5E5E5 !important;
        border-radius: 4px;
    }
    
    /* 表格头部 */
    .stDataFrame thead th {
        background: #FAFAFA !important;
        color: #666666 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 12px 16px !important;
        border-bottom: 1px solid #E5E5E5 !important;
    }
    
    /* 表格单元格 */
    .stDataFrame tbody td {
        color: #1A1A1A !important;
        font-size: 13px !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid #F0F0F0 !important;
    }
    
    /* 表格行悬停 */
    .stDataFrame tbody tr:hover td {
        background: #FAFAFA !important;
    }
    
    /* 按钮 - 极简 */
    .stButton > button {
        background: #1A1A1A !important;
        border: none !important;
        border-radius: 4px !important;
        color: #FFFFFF !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 10px 24px !important;
        transition: all 150ms ease;
    }
    
    .stButton > button:hover {
        background: #333333 !important;
        opacity: 0.9;
    }
    
    .stButton > button:active {
        opacity: 0.8;
        transform: scale(0.98);
    }
    
    /* 下拉框 - 极简 */
    .stSelectbox > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 4px !important;
        color: #1A1A1A;
    }
    
    /* 日期选择器 */
    .stDateInput > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 4px !important;
    }
    
    /* 多选框 */
    .stMultiSelect > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 4px !important;
    }
    
    /* 标签页 - 极简 */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border: none;
        border-bottom: 1px solid #E5E5E5;
        padding: 0;
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        color: #666666;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 500;
        transition: all 150ms ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #1A1A1A;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1A1A1A !important;
        background: transparent !important;
        border-bottom: 2px solid #1A1A1A !important;
        font-weight: 600;
    }
    
    /* 图表容器 - 极简 */
    .js-plotly-plot {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5;
        border-radius: 4px;
    }
    
    /* 文字说明 */
    .stCaption {
        color: #999999 !important;
        font-size: 12px !important;
        margin-top: 8px;
    }
    
    /* 页脚 */
    footer {
        color: #999999;
        text-align: center;
        padding: 3rem 2rem;
        font-size: 12px;
        border-top: 1px solid #E5E5E5;
        margin-top: 3rem;
    }
    
    /* 滚动条 - 极简 */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #D0D0D0;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #999999;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_minimalist_css()

# ==================== 核心算法函数（保留原版逻辑）====================

def load_orders(csv_path: str) -> pd.DataFrame:
    """加载订单数据（原版函数）"""
    df = pd.read_csv(csv_path, parse_dates=["order_date"])
    df["order_month"] = df["order_date"].values.astype("datetime64[M]")
    df["profit"] = df["revenue"] - df["cost"]
    return df

def filter_df(df, date_range, cities=None, channels=None, categories=None):
    """筛选数据（修复城市筛选）"""
    mask = (df["order_date"].dt.date >= date_range[0]) & (df["order_date"].dt.date <= date_range[1])
    if cities and "city" in df.columns: 
        mask &= df["city"].isin(cities)
    if channels: 
        mask &= df["channel"].isin(channels)
    if categories: 
        mask &= df["category"].isin(categories)
    return df.loc[mask].copy()

def compute_kpis(df):
    """计算KPI指标（原版函数）"""
    kpis = {}
    kpis["Revenue"] = df["revenue"].sum()
    kpis["Profit"] = df["profit"].sum()
    kpis["Orders"] = df["order_id"].nunique()
    kpis["Customers"] = df["customer_id"].nunique()
    kpis["AOV"] = df.groupby("order_id")["revenue"].sum().mean()
    kpis["Margin%"] = (df["profit"].sum() / df["revenue"].sum()) if df["revenue"].sum() > 0 else 0
    return kpis

def cohort_analysis(df):
    """留存分析（原版核心算法）"""
    first = df.groupby("customer_id")["order_month"].min().rename("cohort_month")
    tmp = df.merge(first, on="customer_id", how="left")
    tmp["cohort_index"] = ((tmp["order_month"].dt.year - tmp["cohort_month"].dt.year) * 12 +
                           (tmp["order_month"].dt.month - tmp["cohort_month"].dt.month)) + 1
    cohort = tmp.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
    cohort_pivot = cohort.pivot(index="cohort_month", columns="cohort_index", values="customer_id").fillna(0).astype(int)
    cohort_ret = cohort_pivot.divide(cohort_pivot[1], axis=0).round(3)
    return cohort_pivot, cohort_ret

def rfm_segmentation(df, as_of=None):
    """RFM客户细分（原版核心算法）"""
    if as_of is None:
        as_of = df["order_date"].max().normalize() + pd.Timedelta(days=1)
    recency = df.groupby("customer_id")["order_date"].max().apply(lambda d: (as_of - d).days)
    frequency = df.groupby("customer_id")["order_id"].nunique()
    monetary = df.groupby("customer_id")["revenue"].sum()
    r = pd.qcut(recency, 3, labels=[3, 2, 1])
    f = pd.qcut(frequency.rank(method="first"), 3, labels=[1, 2, 3])
    m = pd.qcut(monetary.rank(method="first"), 3, labels=[1, 2, 3])
    rfm = pd.DataFrame({"R": r.astype(int), "F": f.astype(int), "M": m.astype(int)})
    rfm["RFM_Score"] = rfm.sum(axis=1)
    rfm["Segment"] = pd.cut(rfm["RFM_Score"], bins=[2, 5, 7, 9], 
                             labels=["新客户/冷淡", "活跃客户", "高价值客户"], include_lowest=True)
    rfm.index.name = "customer_id"
    return rfm.reset_index()

# ==================== 抖音电商数据适配 ====================

def generate_douyin_customer_data():
    """生成抖音电商模拟数据（保持原版数据结构）"""
    np.random.seed(42)
    n_orders = 3000
    
    dates = pd.date_range('2023-01-01', '2024-12-31', periods=n_orders)
    customers = [f'CUST{str(i).zfill(4)}' for i in np.random.randint(1, 500, n_orders)]
    
    df = pd.DataFrame({
        'order_id': [f'DY{str(i).zfill(6)}' for i in range(n_orders)],
        'customer_id': customers,
        'order_date': dates,
        'revenue': np.random.randint(50, 2000, n_orders),
        'cost': np.random.randint(30, 1500, n_orders),
        'country': np.random.choice(['中国'], n_orders),
        'city': np.random.choice(['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安'], n_orders),
        'channel': np.random.choice(['抖音直播', '抖音短视频', '抖音商城', '达人带货'], n_orders),
        'category': np.random.choice(['服装', '美妆', '数码', '家居', '食品'], n_orders),
        'product_id': [f'SKU{str(i).zfill(4)}' for i in np.random.randint(1, 200, n_orders)]
    })
    
    df['profit'] = df['revenue'] - df['cost']
    df['order_month'] = df['order_date'].values.astype('datetime64[M]')
    
    return df

# ==================== 主应用 ====================

# 极简标题
st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1>客户分析</h1>
        <p class="subtitle">基于RFM模型和留存分析的客户洞察</p>
    </div>
""", unsafe_allow_html=True)

# 数据加载
DATA_PATH = os.environ.get("ORDERS_CSV", os.path.join(os.path.dirname(__file__), "..", "data", "douyin_orders.csv"))

@st.cache_data(show_spinner=False)
def load_data():
    """加载数据"""
    if os.path.exists(DATA_PATH):
        return load_orders(DATA_PATH)
    else:
        return generate_douyin_customer_data()

df = load_data()
min_d, max_d = df["order_date"].dt.date.min(), df["order_date"].dt.date.max()

# 侧边栏筛选 - 极简风格
st.sidebar.markdown("""
    <div style="margin-bottom: 2rem;">
        <h3 style="font-size: 14px; font-weight: 600; color: #1A1A1A; margin-bottom: 1rem;">筛选条件</h3>
    </div>
""", unsafe_allow_html=True)

date_range = st.sidebar.date_input("日期范围", value=(min_d, max_d), min_value=min_d, max_value=max_d)
cities = st.sidebar.multiselect("城市", sorted(df["city"].unique().tolist()) if "city" in df.columns else [])
channels = st.sidebar.multiselect("渠道", sorted(df["channel"].unique().tolist()))
categories = st.sidebar.multiselect("类目", sorted(df["category"].unique().tolist()))

# 数据筛选（修复城市筛选）
fdf = filter_df(df, date_range, 
                cities=cities if cities else None,
                channels=channels if channels else None,
                categories=categories if categories else None)

# 显示数据概览
st.caption(f"显示 {len(fdf):,} 条订单记录，{fdf['customer_id'].nunique():,} 位客户")

# KPI指标 - 极简卡片
st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
kpis = compute_kpis(fdf)
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("销售额", f"¥{kpis['Revenue']:,.0f}")
col2.metric("利润", f"¥{kpis['Profit']:,.0f}")
col3.metric("订单数", f"{kpis['Orders']:,}")
col4.metric("客户数", f"{kpis['Customers']:,}")
col5.metric("客单价", f"¥{kpis['AOV']:,.2f}")
col6.metric("利润率", f"{kpis['Margin%']*100:,.1f}%")

st.markdown("<hr>", unsafe_allow_html=True)

# 时间序列分析
ts = fdf.groupby("order_month").agg({"revenue": "sum", "profit": "sum", "order_id": "nunique"}).reset_index()
ts = ts.sort_values("order_month")
fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(x=ts["order_month"], y=ts["revenue"], mode="lines+markers", name="销售额",
                              line=dict(color='#1A1A1A', width=2),
                              marker=dict(size=6, color='#1A1A1A')))
fig_ts.add_trace(go.Scatter(x=ts["order_month"], y=ts["profit"], mode="lines+markers", name="利润", 
                              yaxis="y2",
                              line=dict(color='#666666', width=2),
                              marker=dict(size=6, color='#666666')))
fig_ts.update_layout(
    title="月度销售与利润趋势",
    title_font=dict(size=16, color='#1A1A1A'),
    xaxis_title="",
    yaxis_title="销售额",
    margin=dict(l=40, r=40, t=60, b=40),
    height=400,
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(color='#1A1A1A', size=12),
    legend=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='#E5E5E5', borderwidth=1),
    xaxis=dict(showgrid=False, linecolor='#E5E5E5'),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0', linecolor='#E5E5E5'),
    yaxis2=dict(title="利润", overlaying="y", side="right", showgrid=False, linecolor='#E5E5E5')
)
st.plotly_chart(fig_ts, use_container_width=True)

# 类目和渠道分析
c1, c2 = st.columns(2)
cat_rev = fdf.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
fig_cat = px.bar(cat_rev, x="category", y="revenue", title="类目销售额排行",
                 color="revenue", color_continuous_scale=["#F0F0F0", "#999999", "#1A1A1A"])
fig_cat.update_layout(
    plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
    font=dict(color='#1A1A1A', size=12), title_font=dict(size=14),
    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#F0F0F0')
)
c1.plotly_chart(fig_cat, use_container_width=True)

ch = fdf.groupby("channel")["revenue"].sum().reset_index()
fig_ch = px.pie(ch, values="revenue", names="channel", title="渠道销售占比", hole=0.5,
                color_discrete_sequence=["#1A1A1A", "#666666", "#999999", "#CCCCCC"])
fig_ch.update_layout(
    plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
    font=dict(color='#1A1A1A', size=12), title_font=dict(size=14),
    showlegend=True
)
c2.plotly_chart(fig_ch, use_container_width=True)

# 留存分析
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("客户留存分析")
cohort_abs, cohort_ret = cohort_analysis(fdf)
st.caption("各批次客户活跃人数（行=首次购买月份，列=购买后第N月）")
st.dataframe(cohort_abs.style.background_gradient(cmap="Greys"))
st.caption("留存率 (%)")
st.dataframe((cohort_ret*100).round(1).style.background_gradient(cmap="Greys"))

# RFM分析
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("RFM客户细分")
rfm = rfm_segmentation(fdf)
seg_counts = rfm["Segment"].value_counts().reset_index()
seg_counts.columns = ["Segment", "Customers"]
fig_rfm = px.bar(seg_counts, x="Segment", y="Customers", title="RFM客户分层",
                 color="Customers", color_continuous_scale=["#F0F0F0", "#999999", "#1A1A1A"])
fig_rfm.update_layout(
    plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
    font=dict(color='#1A1A1A', size=12), title_font=dict(size=14),
    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#F0F0F0')
)
st.plotly_chart(fig_rfm, use_container_width=True)

# RFM详细数据
st.subheader("RFM客户明细")
st.dataframe(rfm.sort_values("RFM_Score", ascending=False), use_container_width=True)

# 下载按钮
st.markdown("<hr>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.download_button("下载筛选数据", data=fdf.to_csv(index=False).encode("utf-8"),
                       file_name="douyin_customer_analysis.csv", mime="text/csv")

# 页脚
st.markdown("""
    <footer>
        <p>NexusTik 客户分析 · 基于真实RFM算法 · 极简设计</p>
        <p style="color: #999999; margin-top: 8px;">数据更新时间: {}</p>
    </footer>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

if __name__ == '__main__':
    print("🚀 NexusTik 客户分析启动...")
    print("📊 访问地址: http://localhost:8501")
