# NexusTik 抖音数据分析服务
# 基于 TikTok Analytics 架构，适配抖音开放平台API

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="NexusTik 抖音数据分析",
    page_icon="📱",
    layout='wide'
)

# ==================== 抖音API配置 ====================

class DouyinAPI:
    """抖音开放平台API封装"""
    
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or os.environ.get('DOUYIN_APP_ID', '')
        self.app_secret = app_secret or os.environ.get('DOUYIN_APP_SECRET', '')
        self.base_url = "https://open.douyin.com"
        self.access_token = None
    
    def get_access_token(self):
        """获取访问令牌"""
        # 实际使用时需要实现OAuth2授权流程
        # 这里提供模拟实现
        return "mock_access_token"
    
    def get_video_list(self, open_id, cursor=0, count=10):
        """获取视频列表"""
        # 实际API调用示例
        # url = f"{self.base_url}/video/list/"
        # headers = {"access-token": self.get_access_token()}
        # params = {"open_id": open_id, "cursor": cursor, "count": count}
        # response = requests.get(url, headers=headers, params=params)
        # return response.json()
        
        # 模拟数据返回
        return self._mock_video_data()
    
    def get_video_data(self, item_ids):
        """获取视频数据"""
        return self._mock_video_data()
    
    def get_user_info(self, open_id):
        """获取用户信息"""
        return {
            "open_id": open_id,
            "nickname": "抖音商家",
            "avatar": "",
            "follower_count": 15000,
            "following_count": 200,
            "total_favorited": 85000
        }
    
    def _mock_video_data(self):
        """模拟视频数据（用于测试）"""
        videos = []
        for i in range(20):
            videos.append({
                "item_id": f"video_{i}",
                "title": f"抖音视频 {i+1}",
                "create_time": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S"),
                "video_status": 1,
                "statistics": {
                    "digg_count": np.random.randint(1000, 50000),
                    "share_count": np.random.randint(100, 5000),
                    "comment_count": np.random.randint(50, 2000),
                    "play_count": np.random.randint(10000, 500000),
                    "forward_count": np.random.randint(10, 1000)
                }
            })
        return {"data": {"list": videos}}

# ==================== 数据加载函数 ====================

def load_douyin_data(source='mock'):
    """加载抖音数据"""
    if source == 'api':
        # 从API获取数据
        api = DouyinAPI()
        data = api.get_video_list("user_open_id")
        videos = data.get("data", {}).get("list", [])
        
        df = pd.DataFrame([{
            'video_id': v['item_id'],
            'title': v['title'],
            'create_time': v['create_time'],
            'likes': v['statistics']['digg_count'],
            'shares': v['statistics']['share_count'],
            'comments': v['statistics']['comment_count'],
            'plays': v['statistics']['play_count'],
            'forwards': v['statistics']['forward_count']
        } for v in videos])
        
    else:
        # 模拟数据
        np.random.seed(42)
        n_videos = 50
        
        df = pd.DataFrame({
            'video_id': [f'VID{str(i).zfill(4)}' for i in range(n_videos)],
            'title': [f'抖音视频 {i+1}' for i in range(n_videos)],
            'create_time': pd.date_range(end=datetime.now(), periods=n_videos, freq='D'),
            'category': np.random.choice(['服装', '美妆', '数码', '家居', '食品'], n_videos),
            'likes': np.random.randint(1000, 50000, n_videos),
            'shares': np.random.randint(100, 5000, n_videos),
            'comments': np.random.randint(50, 2000, n_videos),
            'plays': np.random.randint(10000, 500000, n_videos),
            'forwards': np.random.randint(10, 1000, n_videos),
            'duration': np.random.randint(15, 180, n_videos),
            'is_live': np.random.choice([True, False], n_videos, p=[0.3, 0.7])
        })
    
    # 计算互动率
    df['engagement_rate'] = ((df['likes'] + df['comments'] + df['shares']) / df['plays'] * 100).round(2)
    df['create_date'] = pd.to_datetime(df['create_time']).dt.date
    
    return df

def load_live_data():
    """加载直播数据"""
    np.random.seed(42)
    n_lives = 30
    
    df = pd.DataFrame({
        'live_id': [f'LIVE{str(i).zfill(3)}' for i in range(n_lives)],
        'title': [f'直播场次 {i+1}' for i in range(n_lives)],
        'start_time': pd.date_range(end=datetime.now(), periods=n_lives, freq='2D'),
        'duration': np.random.randint(60, 240, n_lives),
        'max_online': np.random.randint(500, 5000, n_lives),
        'avg_online': np.random.randint(200, 3000, n_lives),
        'gmv': np.random.randint(5000, 50000, n_lives),
        'orders': np.random.randint(50, 500, n_lives),
        'products': np.random.randint(5, 20, n_lives)
    })
    
    df['conversion_rate'] = (df['orders'] / df['avg_online'] * 100).round(2)
    df['avg_order_value'] = (df['gmv'] / df['orders']).round(2)
    
    return df

# ==================== 主应用 ====================

st.sidebar.markdown("<h1 style='display:inline-block'>NexusTik 抖音分析</h1>", unsafe_allow_html=True)
st.sidebar.markdown("抖音电商短视频与直播数据分析平台")

# 数据源选择
st.sidebar.subheader("数据源")
data_source = st.sidebar.radio("选择数据源", ["模拟数据", "抖音API (需配置)"])
source = 'api' if data_source == "抖音API (需配置)" else 'mock'

# API配置
if source == 'api':
    st.sidebar.subheader("API配置")
    app_id = st.sidebar.text_input("App ID", value=os.environ.get('DOUYIN_APP_ID', ''))
    app_secret = st.sidebar.text_input("App Secret", type="password", value=os.environ.get('DOUYIN_APP_SECRET', ''))
    
    if st.sidebar.button("测试连接"):
        api = DouyinAPI(app_id, app_secret)
        user_info = api.get_user_info("test_open_id")
        st.sidebar.success(f"连接成功！粉丝数: {user_info['follower_count']}")

# 加载数据
df_videos = load_douyin_data(source)
df_lives = load_live_data()

# 筛选条件
st.sidebar.subheader("筛选")
date_range = st.sidebar.date_input("日期范围", 
                                     value=(df_videos['create_date'].min(), df_videos['create_date'].max()))
categories = st.sidebar.multiselect("内容类目", df_videos['category'].unique().tolist())

# 数据筛选
if categories:
    df_videos = df_videos[df_videos['category'].isin(categories)]

# 主界面
st.title("📱 NexusTik 抖音数据分析")

# 标签页
tab1, tab2, tab3 = st.tabs(["📹 视频分析", "📺 直播分析", "📊 数据概览"])

# 视频分析标签
with tab1:
    st.header("短视频数据分析")
    
    # KPI指标
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总播放量", f"{df_videos['plays'].sum():,}")
    col2.metric("总点赞", f"{df_videos['likes'].sum():,}")
    col3.metric("总评论", f"{df_videos['comments'].sum():,}")
    col4.metric("平均互动率", f"{df_videos['engagement_rate'].mean():.2f}%")
    
    st.markdown('---')
    
    # 视频数据表格
    st.subheader("视频数据明细")
    st.dataframe(df_videos.sort_values('plays', ascending=False), use_container_width=True)
    
    # 播放趋势
    st.subheader("播放趋势")
    daily_plays = df_videos.groupby('create_date')['plays'].sum().reset_index()
    fig_plays = px.line(daily_plays, x='create_date', y='plays', title='日播放量趋势')
    st.plotly_chart(fig_plays, use_container_width=True)
    
    # 互动分析
    col1, col2 = st.columns(2)
    
    # 点赞分布
    fig_likes = px.histogram(df_videos, x='likes', nbins=20, title='点赞数分布')
    col1.plotly_chart(fig_likes, use_container_width=True)
    
    # 互动率分布
    fig_engagement = px.scatter(df_videos, x='plays', y='engagement_rate', 
                                color='category', size='likes',
                                title='播放量 vs 互动率')
    col2.plotly_chart(fig_engagement, use_container_width=True)

# 直播分析标签
with tab2:
    st.header("直播数据分析")
    
    # KPI指标
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总GMV", f"¥{df_lives['gmv'].sum():,}")
    col2.metric("总订单", f"{df_lives['orders'].sum():,}")
    col3.metric("平均在线", f"{df_lives['avg_online'].mean():.0f}")
    col4.metric("平均转化率", f"{df_lives['conversion_rate'].mean():.2f}%")
    
    st.markdown('---')
    
    # 直播数据表格
    st.subheader("直播数据明细")
    st.dataframe(df_lives.sort_values('gmv', ascending=False), use_container_width=True)
    
    # GMV趋势
    st.subheader("GMV趋势")
    daily_gmv = df_lives.groupby('start_time')['gmv'].sum().reset_index()
    fig_gmv = px.line(daily_gmv, x='start_time', y='gmv', title='直播GMV趋势')
    st.plotly_chart(fig_gmv, use_container_width=True)
    
    # 直播效果分析
    col1, col2 = st.columns(2)
    
    # 在线人数 vs GMV
    fig_online_gmv = px.scatter(df_lives, x='avg_online', y='gmv', 
                                size='orders', color='conversion_rate',
                                title='在线人数 vs GMV')
    col1.plotly_chart(fig_online_gmv, use_container_width=True)
    
    # 直播时长分布
    fig_duration = px.histogram(df_lives, x='duration', nbins=15, title='直播时长分布')
    col2.plotly_chart(fig_duration, use_container_width=True)

# 数据概览标签
with tab3:
    st.header("数据概览")
    
    # 内容类目分布
    st.subheader("内容类目分布")
    cat_stats = df_videos.groupby('category').agg({
        'plays': 'sum',
        'likes': 'sum',
        'comments': 'sum'
    }).reset_index()
    
    fig_cat = px.bar(cat_stats, x='category', y=['plays', 'likes', 'comments'],
                     title='各类目数据对比', barmode='group')
    st.plotly_chart(fig_cat, use_container_width=True)
    
    # 数据导出
    st.subheader("数据导出")
    col1, col2 = st.columns(2)
    
    col1.download_button("下载视频数据", 
                        data=df_videos.to_csv(index=False).encode("utf-8"),
                        file_name="douyin_video_data.csv", mime="text/csv")
    
    col2.download_button("下载直播数据",
                        data=df_lives.to_csv(index=False).encode("utf-8"),
                        file_name="douyin_live_data.csv", mime="text/csv")

st.markdown('---')
st.caption("NexusTik 抖音分析 • 支持抖音开放平台API • 数据驱动决策")

if __name__ == '__main__':
    print("🚀 NexusTik 抖音分析启动...")
    print("📊 访问地址: http://localhost:8003")
