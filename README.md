# 抖音电商数据分析平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/React-18+-61DAFB.svg" alt="React 18+">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/Power%20BI-Desktop-yellow.svg" alt="Power BI">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</p>

<p align="center">
  <b>一站式抖音电商数据分析解决方案</b><br>
  整合销售智能分析、短视频数据看板、客户细分与留存分析的完整平台
</p>

---

## ✨ 项目概述

本项目整合了三个优秀的开源电商数据分析项目，为抖音电商商家提供全方位的数据分析能力：

1. **销售智能分析** - 基于 Python + Plotly/Dash 的销售数据分析
2. **抖音短视频看板** - React + ECharts 的短视频/直播数据可视化
3. **客户分析** - Streamlit + Plotly 的客户细分与留存分析

---

## 🎯 核心功能

### 📊 销售智能分析 (sales-intelligence-dashboard)
- **实时销售看板**: 总销售额、订单数、客单价 KPI
- **产品性能分析**: 热销商品、品类分析、库存预警
- **收入优化**: 销售趋势预测、定价策略建议
- **自动化管道**: 数据自动采集、清洗、分析

### 🎬 抖音短视频看板 (douyin-video-dashboard)
- **视频数据分析**: 播放量、点赞、评论、转发统计
- **直播数据分析**: 直播时长、观看人数、GMV、转化率
- **内容ROI分析**: 投入产出比、内容效果评估
- **抖音风格UI**: 黑色主题 + 霓虹效果

### 👥 客户分析 (customer-analytics-dashboard)
- **RFM客户细分**: 价值客户识别、分层运营
- **留存分析**: 客户生命周期、复购率分析
- **地理分析**: 区域销售分布、热力图
- **预测模型**: 客户流失预警、LTV预测

---

## 🛠️ 技术架构

```
抖音电商数据分析平台
├── 📁 sales-intelligence-dashboard/     # 销售智能分析
│   ├── python/                          # Python数据处理
│   ├── powerbi/                         # Power BI报表
│   └── data/                            # 销售数据
├── 📁 douyin-video-dashboard/           # 抖音短视频看板
│   ├── src/                             # React源代码
│   ├── public/                          # 静态资源
│   └── package.json                     # 依赖配置
├── 📁 customer-analytics-dashboard/     # 客户分析
│   ├── app.py                           # Streamlit主应用
│   ├── utils/                           # 工具函数
│   └── data/                            # 客户数据
├── 📁 data/                             # 统一数据目录
│   ├── raw/                             # 原始数据
│   ├── processed/                       # 处理后数据
│   └── sample/                          # 示例数据
├── 📁 docs/                             # 文档
│   ├── 安装指南.md
│   ├── 使用手册.md
│   └── API文档.md
└── 📁 scripts/                          # 脚本工具
    ├── setup.py                         # 环境安装
    ├── start_all.py                     # 一键启动
    └── data_sync.py                     # 数据同步
```

---

## 📦 安装部署

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn
- Git

### 快速开始

#### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/抖音电商数据分析.git
cd 抖音电商数据分析
```

#### 2. 安装依赖
```bash
# 运行安装脚本
python scripts/setup.py
```

或手动安装：
```bash
# Python依赖
pip install -r requirements.txt

# 抖音看板依赖
cd douyin-video-dashboard
npm install
```

#### 3. 启动服务
```bash
# 一键启动所有服务
python scripts/start_all.py
```

或单独启动：
```bash
# 启动销售分析 (端口:8050)
cd sales-intelligence-dashboard
python app.py

# 启动抖音看板 (端口:3000)
cd douyin-video-dashboard
npm start

# 启动客户分析 (端口:8501)
cd customer-analytics-dashboard
streamlit run app.py
```

---

## 📊 数据源配置

### 抖音电商罗盘数据
1. 登录抖音电商罗盘
2. 导出直播数据、短视频数据、商品数据
3. 将CSV文件放入 `data/raw/` 目录

### 店铺后台数据
1. 从抖店后台导出订单数据
2. 放入 `data/raw/orders/` 目录

### 数据格式示例

#### 订单数据
```csv
order_id,product_name,amount,quantity,order_date,customer_id
ORD001,商品A,199.00,2,2024-01-15,CUST001
ORD002,商品B,299.00,1,2024-01-16,CUST002
```

#### 视频数据
```csv
video_id,title,play_count,like_count,comment_count,share_date
VID001,视频标题A,125000,8500,320,2024-01-15
VID002,视频标题B,98000,6200,280,2024-01-16
```

---

## 🎨 界面预览

### 销售智能看板
- 实时KPI指标卡片
- 销售趋势折线图
- 产品类别饼图
- 区域销售热力图

### 抖音短视频看板
- 视频数据概览
- 播放/互动趋势图
- 直播数据大屏
- 转化率分析

### 客户分析看板
- RFM客户分层
- 留存率曲线
- 客户生命周期价值
- 地理分布图

---

## 🔧 配置说明

### 配置文件
编辑 `config.yaml` 文件：
```yaml
# 数据库配置
database:
  type: sqlite
  path: data/database.db

# API配置
douyin_api:
  app_id: your_app_id
  app_secret: your_app_secret

# 看板配置
dashboard:
  sales_port: 8050
  video_port: 3000
  customer_port: 8501
```

---

## 📈 使用流程

### 日常数据分析流程
1. **数据导入**: 将抖音罗盘导出的数据放入指定目录
2. **数据清洗**: 运行数据清洗脚本
3. **查看看板**: 打开各个分析看板查看数据
4. **导出报告**: 生成PDF或Excel分析报告

### 直播数据分析流程
1. 直播结束后导出直播数据
2. 上传数据到平台
3. 查看直播效果分析
4. 对比历史直播数据
5. 生成优化建议

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交规范
- 使用清晰的提交信息
- 添加必要的测试
- 更新相关文档

---

## 📄 开源协议

本项目采用 MIT 协议开源。

---

## 🙏 致谢

本项目整合了以下优秀的开源项目：

- [Madhav E-Commerce Sales Intelligence Dashboard](https://github.com/amitkr209/Madhav_E-Commerce-Sales_Intelligence_Dashboard)
- [抖音/TikTok 电商短视频数据分析看板](https://github.com/1xbbx)
- [Data Storytelling Dashboard](https://github.com/AmirhosseinHonardoust/Data-Storytelling-Dashboard)

感谢这些项目的作者！

---

## 📞 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。

---

<p align="center">
  Made with ❤️ for Douyin E-commerce Analytics
</p>
