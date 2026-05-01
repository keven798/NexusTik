# NexusTik 数据分析平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-5.18+-green.svg" alt="Plotly">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  <b>抖音电商智能分析系统</b> - 整合销售分析、客户分析、抖音分析三大模块的统一数据分析平台
</p>

---

## 功能特性

### 核心模块

| 模块 | 功能描述 | 关键指标 |
|------|---------|---------|
| **销售分析** | 销售趋势、类目分布、渠道分析 | 总销售额、总利润、总订单、总客户、客单价、利润率 |
| **客户分析** | RFM客户分群、留存分析、客户价值评估 | 新客户/活跃客户/高价值客户分布 |
| **抖音分析** | 视频数据分析、直播数据分析 | 播放量、点赞、评论、互动率、GMV、转化率 |

### 特色功能

- **多语言支持**：中文 / English 一键切换
- **主题切换**：活力、海洋、日落三种配色主题
- **CSV数据导入**：支持上传自定义数据进行分析
- **实时筛选**：日期范围、类目、渠道、城市等多维度筛选
- **交互式图表**：Plotly 交互式图表，支持缩放、平移、下载

---

## 项目结构

```
nexustik-analytics/
├── nexus-platform/              # 统一分析平台（主入口）
│   └── app.py                   # Streamlit 主应用
├── sales-intelligence-dashboard/ # 销售智能分析看板
│   └── app.py                   # Dash 销售分析
├── customer-analytics-dashboard/ # 客户分析看板
│   └── app.py                   # Streamlit 客户分析
├── douyin-video-dashboard/       # 抖音视频分析看板
│   ├── src/
│   │   ├── App.jsx              # React 主组件
│   │   └── utils/mockData.js    # 模拟数据
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── nexus-microservices/          # 微服务架构
│   ├── api-gateway/
│   └── deploy/
├── scripts/                      # 启动脚本
│   ├── setup.py
│   └── start_all.py
├── requirements.txt              # Python 依赖
└── README.md                     # 项目说明
```

---

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+ (如需运行 React 看板)

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/nexustik-analytics.git
cd nexustik-analytics

# 安装 Python 依赖
pip install -r requirements.txt
```

### 启动统一分析平台

```bash
cd nexus-platform
streamlit run app.py
```

访问地址：http://localhost:8501

### 启动销售智能看板

```bash
cd sales-intelligence-dashboard
python app.py
```

访问地址：http://localhost:8050

### 启动客户分析看板

```bash
cd customer-analytics-dashboard
streamlit run app.py
```

访问地址：http://localhost:8502

### 启动抖音视频看板

```bash
cd douyin-video-dashboard
npm install
npm run dev
```

访问地址：http://localhost:5173

---

## 数据格式

### 销售数据 CSV 格式

| 列名 | 说明 | 示例 |
|------|------|------|
| 订单日期 | 订单创建日期 | 2024-01-15 |
| 订单金额 | 订单总金额 | 299.00 |
| 订单成本 | 商品成本 | 150.00 |
| 商品数量 | 购买数量 | 2 |
| 商品类目 | 商品分类 | 服装 |
| 商品名称 | 商品名称 | T恤 |
| 客户ID | 客户标识 | CUST001 |
| 城市 | 客户所在城市 | 上海 |
| 渠道 | 销售渠道 | 抖音直播 |

### 客户数据 CSV 格式

| 列名 | 说明 | 示例 |
|------|------|------|
| 订单日期 | 订单创建日期 | 2024-01-15 |
| 客户ID | 客户标识 | CUST001 |
| 订单金额 | 订单金额 | 299.00 |
| 订单成本 | 商品成本 | 150.00 |
| 城市 | 客户所在城市 | 上海 |
| 渠道 | 销售渠道 | 抖音直播 |
| 商品类目 | 商品分类 | 服装 |
| 订单ID | 订单标识 | ORD001 |

---

## 核心算法

### RFM 客户分群

- **R (Recency)**：最近一次购买距今天数
- **F (Frequency)**：购买频率
- **M (Monetary)**：消费金额

客户分群结果：
- 新客户/冷淡客户
- 活跃客户
- 高价值客户

### 留存分析

基于客户首次购买月份进行同期群分析，计算各月份的留存率。

---

## 技术栈

### 后端
- **Python** - 核心编程语言
- **Pandas** - 数据处理与分析
- **NumPy** - 数值计算

### 前端
- **Streamlit** - Python 数据应用框架
- **Dash** - Plotly 数据可视化框架
- **React** - 用户界面库
- **Tailwind CSS** - 样式框架

### 可视化
- **Plotly** - 交互式图表
- **Plotly Express** - 高级图表接口

---

## 截图展示

### 销售分析页面
- 顶部渐变导航栏
- 6个彩色KPI指标卡片
- 销售趋势折线图
- 类目分布柱状图
- 渠道占比饼图

### 客户分析页面
- RFM客户分群柱状图
- 留存分析热力图
- 客户数据表格

### 抖音分析页面
- 视频数据趋势图
- 直播效果散点图
- 视频/直播KPI指标

### 设置页面
- 语言切换（中文/English）
- 主题切换（活力/海洋/日落）

---

## 开发计划

- [x] 销售分析模块
- [x] 客户分析模块
- [x] 抖音分析模块
- [x] 多语言支持
- [x] 主题切换
- [x] CSV数据导入
- [ ] 数据导出功能
- [ ] 用户认证系统
- [ ] 实时数据接入
- [ ] 移动端适配

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至：your-email@example.com

---

<p align="center">
  Made with ❤️ for Douyin E-commerce Analytics
</p>
