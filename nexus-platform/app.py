# NexusTik 统一分析平台
# 整合销售分析、客户分析、抖音分析三大模块
# 支持顶部选项卡切换和语言切换

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
import warnings
warnings.filterwarnings('ignore')

# ==================== 多语言支持 ====================

TRANSLATIONS = {
    "zh": {
        "title": "NexusTik 数据分析平台",
        "subtitle": "抖音电商智能分析系统",
        "sales_tab": "📊 销售分析",
        "customer_tab": "👥 客户分析",
        "tiktok_tab": "📱 抖音分析",
        "settings_tab": "⚙️ 设置",
        "language": "语言",
        "chinese": "中文",
        "english": "English",
        "theme": "主题",
        "data_source": "数据源",
        "refresh": "刷新数据",
        "export": "导出数据",
        "date_range": "日期范围",
        "category": "类目",
        "channel": "渠道",
        "city": "城市",
        "all": "全部",
        "total_sales": "总销售额",
        "total_profit": "总利润",
        "total_orders": "总订单",
        "total_customers": "总客户",
        "aov": "客单价",
        "margin": "利润率",
        "trend": "趋势分析",
        "distribution": "分布分析",
        "top_products": "热销商品",
        "rfm_analysis": "RFM分析",
        "cohort_analysis": "留存分析",
        "video_analysis": "视频分析",
        "live_analysis": "直播分析",
        "overview": "数据概览",
        "settings_title": "系统设置",
        "language_setting": "语言设置",
        "theme_setting": "主题设置",
        "data_setting": "数据设置",
        "save_settings": "保存设置",
        "reset_settings": "重置设置",
        "current_language": "当前语言",
    },
    "en": {
        "title": "NexusTik Analytics Platform",
        "subtitle": "Douyin E-commerce Intelligence System",
        "sales_tab": "📊 Sales",
        "customer_tab": "👥 Customers",
        "tiktok_tab": "📱 Douyin",
        "settings_tab": "⚙️ Settings",
        "language": "Language",
        "chinese": "中文",
        "english": "English",
        "theme": "Theme",
        "data_source": "Data Source",
        "refresh": "Refresh",
        "export": "Export",
        "date_range": "Date Range",
        "category": "Category",
        "channel": "Channel",
        "city": "City",
        "all": "All",
        "total_sales": "Total Sales",
        "total_profit": "Total Profit",
        "total_orders": "Total Orders",
        "total_customers": "Total Customers",
        "aov": "AOV",
        "margin": "Margin",
        "trend": "Trend Analysis",
        "distribution": "Distribution",
        "top_products": "Top Products",
        "rfm_analysis": "RFM Analysis",
        "cohort_analysis": "Cohort Analysis",
        "video_analysis": "Video Analysis",
        "live_analysis": "Live Analysis",
        "overview": "Overview",
        "settings_title": "System Settings",
        "language_setting": "Language",
        "theme_setting": "Theme",
        "data_setting": "Data Settings",
        "save_settings": "Save",
        "reset_settings": "Reset",
        "current_language": "Current Language",
    }
}

def get_text(key):
    """获取当前语言的文本"""
    lang = st.session_state.get('language', 'zh')
    return TRANSLATIONS.get(lang, TRANSLATIONS['zh']).get(key, key)

# ==================== 彩色主题配置 ====================

COLOR_THEMES = {
    "vibrant": {
        "primary": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8"],
        "secondary": ["#FF8E53", "#FF6B9D", "#C44569", "#F8B500", "#6C5CE7", "#A29BFE"],
        "background": "#FFFFFF",
        "text": "#2D3436",
        "grid": "#F0F0F0"
    },
    "ocean": {
        "primary": ["#006BA6", "#0496FF", "#3A86FF", "#7209B7", "#F72585", "#4CC9F0"],
        "secondary": ["#5C8D89", "#74B49B", "#A7D7C5", "#F4F9F4", "#2C3E50"],
        "background": "#F8FAFB",
        "text": "#1A1A2E",
        "grid": "#E8EEF2"
    },
    "sunset": {
        "primary": ["#FF6B35", "#F7931E", "#FFD23F", "#EE4266", "#540D6E", "#0EAD69"],
        "secondary": ["#F4A261", "#E76F51", "#2A9D8F", "#E9C46A", "#264653"],
        "background": "#FFF8F0",
        "text": "#2A1810",
        "grid": "#F5E6D3"
    }
}

def get_theme():
    """获取当前主题"""
    theme_name = st.session_state.get('theme', 'vibrant')
    return COLOR_THEMES.get(theme_name, COLOR_THEMES['vibrant'])

# ==================== 页面配置 ====================

st.set_page_config(
    page_title="NexusTik Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 初始化Session State ====================

if 'language' not in st.session_state:
    st.session_state.language = 'zh'
if 'theme' not in st.session_state:
    st.session_state.theme = 'vibrant'

# ==================== 全局CSS样式 ====================

def load_global_css():
    theme = get_theme()
    css = f"""
    <style>
    /* 全局背景 */
    .stApp {{
        background: {theme['background']};
    }}
    
    /* 主内容区 */
    .main .block-container {{
        background: {theme['background']};
        padding: 1rem 2rem;
        max-width: 1400px;
    }}
    
    /* 顶部导航栏 */
    .top-nav {{
        background: linear-gradient(135deg, {theme['primary'][0]}, {theme['primary'][2]});
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    
    .top-nav h1 {{
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
    }}
    
    .top-nav p {{
        color: rgba(255,255,255,0.8);
        font-size: 14px;
        margin: 4px 0 0 0;
    }}
    
    /* 选项卡样式 */
    .stTabs [data-baseweb="tab-list"] {{
        background: white;
        border: 1px solid {theme['grid']};
        border-radius: 12px;
        padding: 8px;
        gap: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border: none;
        border-radius: 8px;
        color: {theme['text']};
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 600;
        transition: all 200ms ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: {theme['grid']};
        color: {theme['primary'][0]};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {theme['primary'][0]}, {theme['primary'][1]}) !important;
        color: white !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }}
    
    /* KPI卡片 - 彩色 */
    [data-testid="stMetric"] {{
        background: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 8px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        transition: all 200ms ease;
        border-left: 4px solid {theme['primary'][0]};
    }}

    [data-testid="stMetric"]:nth-child(2) {{
        border-left-color: {theme['primary'][1]};
    }}

    [data-testid="stMetric"]:nth-child(3) {{
        border-left-color: {theme['primary'][2]};
    }}

    [data-testid="stMetric"]:nth-child(4) {{
        border-left-color: {theme['primary'][3]};
    }}

    [data-testid="stMetric"]:nth-child(5) {{
        border-left-color: {theme['primary'][4]};
    }}

    [data-testid="stMetric"]:nth-child(6) {{
        border-left-color: {theme['primary'][5]};
    }}

    [data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }}

    /* KPI数值 */
    [data-testid="stMetricValue"] {{
        color: {theme['text']} !important;
        font-size: 18px !important;
        font-weight: 700;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: {theme['text']};
        opacity: 0.7;
        font-size: 11px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}
    
    /* 图表容器 */
    .js-plotly-plot {{
        background: white !important;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}
    
    /* 按钮 */
    .stButton > button {{
        background: linear-gradient(135deg, {theme['primary'][0]}, {theme['primary'][1]}) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 200ms ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }}
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {{
        background: white !important;
        border-right: 1px solid {theme['grid']};
    }}
    
    /* 下拉框 */
    .stSelectbox > div > div,
    .stDateInput > div > div,
    .stMultiSelect > div > div {{
        background: white !important;
        border: 1px solid {theme['grid']} !important;
        border-radius: 8px !important;
    }}
    
    /* 分隔线 */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {theme['grid']}, transparent);
        margin: 2rem 0;
    }}
    
    /* 页脚 */
    footer {{
        text-align: center;
        padding: 2rem;
        color: {theme['text']};
        opacity: 0.6;
        font-size: 12px;
        border-top: 1px solid {theme['grid']};
        margin-top: 3rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_global_css()

# ==================== 数据生成函数 ====================

def generate_sales_data():
    """生成销售数据"""
    np.random.seed(42)
    n_orders = 5000
    dates = pd.date_range('2023-01-01', '2024-12-31', periods=n_orders)
    
    df = pd.DataFrame({
        'order_id': [f'S{str(i).zfill(6)}' for i in range(n_orders)],
        'order_date': dates,
        'revenue': np.random.randint(50, 2000, n_orders),
        'cost': np.random.randint(30, 1500, n_orders),
        'quantity': np.random.randint(1, 5, n_orders),
        'category': np.random.choice(['服装', '美妆', '数码', '家居', '食品', '配饰'], n_orders),
        'product_name': [f'商品{i}' for i in range(n_orders)],
        'customer_id': [f'CUST{np.random.randint(1, 1000)}' for _ in range(n_orders)],
        'city': np.random.choice(['北京', '上海', '广州', '深圳', '杭州', '成都'], n_orders),
        'channel': np.random.choice(['抖音直播', '短视频', '商城', '达人带货'], n_orders)
    })
    df['profit'] = df['revenue'] - df['cost']
    df['order_month'] = df['order_date'].values.astype('datetime64[M]')
    return df

def generate_customer_data():
    """生成客户数据"""
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
        'city': np.random.choice(['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安'], n_orders),
        'channel': np.random.choice(['抖音直播', '抖音短视频', '抖音商城', '达人带货'], n_orders),
        'category': np.random.choice(['服装', '美妆', '数码', '家居', '食品'], n_orders),
    })
    df['profit'] = df['revenue'] - df['cost']
    df['order_month'] = df['order_date'].values.astype('datetime64[M]')
    return df

def generate_tiktok_data():
    """生成抖音数据"""
    np.random.seed(42)
    n_videos = 50
    
    df_videos = pd.DataFrame({
        'video_id': [f'VID{str(i).zfill(4)}' for i in range(n_videos)],
        'title': [f'视频 {i+1}' for i in range(n_videos)],
        'create_time': pd.date_range(end=datetime.now(), periods=n_videos, freq='D'),
        'category': np.random.choice(['服装', '美妆', '数码', '家居', '食品'], n_videos),
        'likes': np.random.randint(1000, 50000, n_videos),
        'shares': np.random.randint(100, 5000, n_videos),
        'comments': np.random.randint(50, 2000, n_videos),
        'plays': np.random.randint(10000, 500000, n_videos),
        'duration': np.random.randint(15, 180, n_videos),
    })
    df_videos['engagement_rate'] = ((df_videos['likes'] + df_videos['comments'] + df_videos['shares']) / df_videos['plays'] * 100).round(2)
    
    n_lives = 30
    df_lives = pd.DataFrame({
        'live_id': [f'LIVE{str(i).zfill(3)}' for i in range(n_lives)],
        'title': [f'直播 {i+1}' for i in range(n_lives)],
        'start_time': pd.date_range(end=datetime.now(), periods=n_lives, freq='2D'),
        'duration': np.random.randint(60, 240, n_lives),
        'max_online': np.random.randint(500, 5000, n_lives),
        'avg_online': np.random.randint(200, 3000, n_lives),
        'gmv': np.random.randint(5000, 50000, n_lives),
        'orders': np.random.randint(50, 500, n_lives),
    })
    df_lives['conversion_rate'] = (df_lives['orders'] / df_lives['avg_online'] * 100).round(2)
    
    return df_videos, df_lives

# ==================== 核心算法函数 ====================

def compute_kpis(df):
    """计算KPI"""
    return {
        "Revenue": df["revenue"].sum(),
        "Profit": df["profit"].sum(),
        "Orders": df["order_id"].nunique(),
        "Customers": df["customer_id"].nunique(),
        "AOV": df.groupby("order_id")["revenue"].sum().mean(),
        "Margin%": (df["profit"].sum() / df["revenue"].sum()) if df["revenue"].sum() > 0 else 0
    }

def render_kpi_cards(metrics, theme):
    """渲染KPI卡片 - 使用Streamlit原生st.metric组件"""
    colors = theme['primary']
    cols = st.columns(len(metrics))
    for i, (label, value) in enumerate(metrics):
        with cols[i]:
            # 使用原生metric，通过CSS控制样式
            st.metric(label=label, value=value)

def cohort_analysis(df):
    """留存分析"""
    first = df.groupby("customer_id")["order_month"].min().rename("cohort_month")
    tmp = df.merge(first, on="customer_id", how="left")
    tmp["cohort_index"] = ((tmp["order_month"].dt.year - tmp["cohort_month"].dt.year) * 12 +
                           (tmp["order_month"].dt.month - tmp["cohort_month"].dt.month)) + 1
    cohort = tmp.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
    cohort_pivot = cohort.pivot(index="cohort_month", columns="cohort_index", values="customer_id").fillna(0).astype(int)
    cohort_ret = cohort_pivot.divide(cohort_pivot[1], axis=0).round(3)
    return cohort_pivot, cohort_ret

def rfm_segmentation(df):
    """RFM分析"""
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

# ==================== 模块页面函数 ====================

def load_sales_data(uploaded_file=None):
    """加载销售数据，支持CSV上传和模拟数据"""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # 适配中文列名
        column_mapping = {
            '订单日期': 'order_date',
            '订单金额': 'revenue',
            '订单成本': 'cost',
            '商品数量': 'quantity',
            '商品类目': 'category',
            '商品名称': 'product_name',
            '客户ID': 'customer_id',
            '城市': 'city',
            '渠道': 'channel',
            '利润': 'profit'
        }
        df = df.rename(columns=column_mapping)
        df['order_date'] = pd.to_datetime(df['order_date'])
        if 'profit' not in df.columns and 'revenue' in df.columns and 'cost' in df.columns:
            df['profit'] = df['revenue'] - df['cost']
        df['order_month'] = df['order_date'].values.astype('datetime64[M]')
        return df
    else:
        return generate_sales_data()

def sales_analysis_page():
    """销售分析页面"""
    t = get_text
    theme = get_theme()
    
    st.header(t("sales_tab"))
    
    # 文件上传
    uploaded_file = st.file_uploader("📁 上传销售数据CSV文件（可选）", type=['csv'], key="sales_file_upload")
    if uploaded_file is not None:
        st.success(f"✅ 已上传文件: {uploaded_file.name}")
    
    df = load_sales_data(uploaded_file)
    
    # 筛选器
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input(t("date_range"), value=(df["order_date"].dt.date.min(), df["order_date"].dt.date.max()), key="sales_date_range")
    with col2:
        categories = st.multiselect(t("category"), df["category"].unique().tolist(), key="sales_categories")
    with col3:
        channels = st.multiselect(t("channel"), df["channel"].unique().tolist(), key="sales_channels")
    
    # 数据筛选
    mask = (df["order_date"].dt.date >= date_range[0]) & (df["order_date"].dt.date <= date_range[1])
    if categories: mask &= df["category"].isin(categories)
    if channels: mask &= df["channel"].isin(channels)
    fdf = df[mask]
    
    # KPI
    kpis = compute_kpis(fdf)
    metrics = [
        (t("total_sales"), f"¥{kpis['Revenue']:,.0f}"),
        (t("total_profit"), f"¥{kpis['Profit']:,.0f}"),
        (t("total_orders"), f"{kpis['Orders']:,}"),
        (t("total_customers"), f"{kpis['Customers']:,}"),
        (t("aov"), f"¥{kpis['AOV']:,.2f}"),
        (t("margin"), f"{kpis['Margin%']*100:,.1f}%")
    ]
    render_kpi_cards(metrics, theme)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 趋势图
    ts = fdf.groupby("order_month").agg({"revenue": "sum", "profit": "sum"}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["order_month"], y=ts["revenue"], mode="lines+markers", 
                              name=t("total_sales"), line=dict(color=theme['primary'][0], width=3)))
    fig.add_trace(go.Scatter(x=ts["order_month"], y=ts["profit"], mode="lines+markers", 
                              name=t("total_profit"), line=dict(color=theme['primary'][1], width=3)))
    fig.update_layout(title=t("trend"), plot_bgcolor='white', paper_bgcolor='white',
                      font=dict(color=theme['text']), height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # 分布图
    col1, col2 = st.columns(2)
    cat_data = fdf.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
    fig1 = px.bar(cat_data, x="category", y="revenue", title=t("distribution"),
                  color="revenue", color_continuous_scale=theme['primary'][:3])
    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    col1.plotly_chart(fig1, use_container_width=True)
    
    ch_data = fdf.groupby("channel")["revenue"].sum().reset_index()
    fig2 = px.pie(ch_data, values="revenue", names="channel", title=t("channel"),
                  color_discrete_sequence=theme['primary'])
    fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    col2.plotly_chart(fig2, use_container_width=True)

def load_customer_data(uploaded_file=None):
    """加载客户数据，支持CSV上传和模拟数据"""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        column_mapping = {
            '订单日期': 'order_date',
            '客户ID': 'customer_id',
            '订单金额': 'revenue',
            '订单成本': 'cost',
            '城市': 'city',
            '渠道': 'channel',
            '商品类目': 'category',
            '订单ID': 'order_id'
        }
        df = df.rename(columns=column_mapping)
        df['order_date'] = pd.to_datetime(df['order_date'])
        if 'profit' not in df.columns and 'revenue' in df.columns and 'cost' in df.columns:
            df['profit'] = df['revenue'] - df['cost']
        df['order_month'] = df['order_date'].values.astype('datetime64[M]')
        return df
    else:
        return generate_customer_data()

def customer_analysis_page():
    """客户分析页面"""
    t = get_text
    theme = get_theme()
    
    st.header(t("customer_tab"))
    
    # 文件上传
    uploaded_file = st.file_uploader("📁 上传客户数据CSV文件（可选）", type=['csv'], key="customer_file_upload")
    if uploaded_file is not None:
        st.success(f"✅ 已上传文件: {uploaded_file.name}")
    
    df = load_customer_data(uploaded_file)
    
    # 筛选器
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input(t("date_range"), value=(df["order_date"].dt.date.min(), df["order_date"].dt.date.max()), key="cust_date_range")
    with col2:
        cities = st.multiselect(t("city"), df["city"].unique().tolist(), key="cust_cities")
    with col3:
        categories = st.multiselect(t("category"), df["category"].unique().tolist(), key="cust_categories")
    
    mask = (df["order_date"].dt.date >= date_range[0]) & (df["order_date"].dt.date <= date_range[1])
    if cities: mask &= df["city"].isin(cities)
    if categories: mask &= df["category"].isin(categories)
    fdf = df[mask]
    
    # KPI
    kpis = compute_kpis(fdf)
    metrics = [
        (t("total_sales"), f"¥{kpis['Revenue']:,.0f}"),
        (t("total_profit"), f"¥{kpis['Profit']:,.0f}"),
        (t("total_orders"), f"{kpis['Orders']:,}"),
        (t("total_customers"), f"{kpis['Customers']:,}"),
        (t("aov"), f"¥{kpis['AOV']:,.2f}"),
        (t("margin"), f"{kpis['Margin%']*100:,.1f}%")
    ]
    render_kpi_cards(metrics, theme)

    st.markdown("<hr>", unsafe_allow_html=True)

    # RFM分析
    st.subheader(t("rfm_analysis"))
    rfm = rfm_segmentation(fdf)
    seg_counts = rfm["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Customers"]
    fig = px.bar(seg_counts, x="Segment", y="Customers", title=t("rfm_analysis"),
                 color="Customers", color_continuous_scale=theme['primary'][:3])
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)
    
    # 留存分析
    st.subheader(t("cohort_analysis"))
    cohort_abs, cohort_ret = cohort_analysis(fdf)
    st.dataframe(cohort_abs.style.background_gradient(cmap="YlOrRd"))
    st.caption("Retention Rate (%)")
    st.dataframe((cohort_ret*100).round(1).style.background_gradient(cmap="YlOrRd"))

def tiktok_analysis_page():
    """抖音分析页面"""
    t = get_text
    theme = get_theme()
    
    st.header(t("tiktok_tab"))
    
    df_videos, df_lives = generate_tiktok_data()
    
    # 视频分析
    st.subheader(t("video_analysis"))
    video_metrics = [
        ("总播放量", f"{df_videos['plays'].sum():,}"),
        ("总点赞", f"{df_videos['likes'].sum():,}"),
        ("总评论", f"{df_videos['comments'].sum():,}"),
        ("平均互动率", f"{df_videos['engagement_rate'].mean():.2f}%")
    ]
    render_kpi_cards(video_metrics, theme)

    # 视频趋势
    daily = df_videos.groupby(df_videos['create_time'].dt.date).agg({
        'plays': 'sum', 'likes': 'sum', 'comments': 'sum'
    }).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily['create_time'], y=daily['plays'], mode='lines+markers',
                              name='播放量', line=dict(color=theme['primary'][0], width=3)))
    fig.add_trace(go.Scatter(x=daily['create_time'], y=daily['likes'], mode='lines+markers',
                              name='点赞', line=dict(color=theme['primary'][1], width=3)))
    fig.update_layout(title='视频数据趋势', plot_bgcolor='white', paper_bgcolor='white', height=400)
    st.plotly_chart(fig, use_container_width=True)

    # 直播分析
    st.subheader(t("live_analysis"))
    live_metrics = [
        ("总GMV", f"¥{df_lives['gmv'].sum():,}"),
        ("总订单", f"{df_lives['orders'].sum():,}"),
        ("平均在线", f"{df_lives['avg_online'].mean():.0f}"),
        ("平均转化率", f"{df_lives['conversion_rate'].mean():.2f}%")
    ]
    render_kpi_cards(live_metrics, theme)
    
    # 直播趋势
    fig2 = px.scatter(df_lives, x='avg_online', y='gmv', size='orders', color='conversion_rate',
                      title='直播效果分析', color_continuous_scale=theme['primary'][:4])
    fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig2, use_container_width=True)

def settings_page():
    """设置页面"""
    t = get_text
    theme = get_theme()
    
    st.header(t("settings_title"))
    
    # 语言设置
    st.subheader(t("language_setting"))
    lang_cols = st.columns(2)
    with lang_cols[0]:
        if st.button("🇨🇳 中文", use_container_width=True):
            st.session_state.language = 'zh'
            st.rerun()
    with lang_cols[1]:
        if st.button("🇺🇸 English", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    
    st.info(f"{t('current_language')}: {t('chinese') if st.session_state.language == 'zh' else t('english')}")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 主题设置
    st.subheader(t("theme_setting"))
    theme_options = {
        "vibrant": "🌈 " + ("活力" if st.session_state.language == 'zh' else "Vibrant"),
        "ocean": "🌊 " + ("海洋" if st.session_state.language == 'zh' else "Ocean"),
        "sunset": "🌅 " + ("日落" if st.session_state.language == 'zh' else "Sunset")
    }
    selected_theme = st.radio("", list(theme_options.keys()), 
                              format_func=lambda x: theme_options[x],
                              horizontal=True)
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 数据设置
    st.subheader(t("data_setting"))
    if st.button(t("refresh"), use_container_width=True):
        st.cache_data.clear()
        st.success("数据已刷新！")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 保存/重置
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("save_settings"), use_container_width=True):
            settings = {
                "language": st.session_state.language,
                "theme": st.session_state.theme
            }
            st.success("设置已保存！")
    with col2:
        if st.button(t("reset_settings"), use_container_width=True):
            st.session_state.language = 'zh'
            st.session_state.theme = 'vibrant'
            st.rerun()

# ==================== 主应用入口 ====================

def main():
    """主函数"""
    t = get_text
    
    # 顶部导航栏
    st.markdown(f"""
        <div class="top-nav">
            <h1>{t('title')}</h1>
            <p>{t('subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 选项卡导航
    tabs = st.tabs([
        t("sales_tab"),
        t("customer_tab"),
        t("tiktok_tab"),
        t("settings_tab")
    ])
    
    with tabs[0]:
        sales_analysis_page()
    
    with tabs[1]:
        customer_analysis_page()
    
    with tabs[2]:
        tiktok_analysis_page()
    
    with tabs[3]:
        settings_page()
    
    # 页脚
    st.markdown(f"""
        <footer>
            <p>NexusTik Analytics Platform · {datetime.now().year}</p>
            <p style="margin-top: 8px;">{t('current_language')}: {t('chinese') if st.session_state.language == 'zh' else t('english')}</p>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    print("🚀 NexusTik Platform 启动...")
    print("📊 访问地址: http://localhost:8501")
    main()
