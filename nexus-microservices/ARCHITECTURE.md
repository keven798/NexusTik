# NexusTik 微服务架构设计

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        客户端层 (Frontend)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Web App   │  │  Mobile App │  │   Desktop   │             │
│  │   (React)   │  │  (Optional) │  │  (Optional) │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
└─────────┼────────────────┼────────────────┼─────────────────────┘
          │                │                │
          └────────────────┴────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    API 网关层 (API Gateway)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - 路由转发                                                │   │
│  │  - 认证授权                                                │   │
│  │  - 限流熔断                                                │   │
│  │  - 负载均衡                                                │   │
│  │  - 统一日志                                                │   │
│  └────────────────────┬────────────────────────────────────┘   │
└───────────────────────┼─────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│ 销售分析服务  │ │ 客户分析服务 │ │TikTok服务   │
│  (Port:8001) │ │ (Port:8002) │ │(Port:8003)  │
├──────────────┤ ├─────────────┤ ├─────────────┤
│ - Dash App   │ │ - Streamlit │ │ - Streamlit │
│ - REST API   │ │ - REST API  │ │ - REST API  │
│ - 销售数据    │ │ - 客户数据   │ │ - 视频数据   │
│ - 商品分析    │ │ - RFM分析    │ │ - 直播数据   │
└───────┬──────┘ └──────┬──────┘ └──────┬──────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                      数据层 (Data Layer)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  PostgreSQL │  │    Redis    │  │   MinIO     │             │
│  │  (主数据库)  │  │   (缓存)    │  │  (文件存储)  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## 服务说明

### 1. API 网关 (api-gateway)
- **端口**: 8080
- **技术**: FastAPI + Nginx
- **职责**:
  - 统一入口点
  - JWT认证
  - 请求路由
  - 限流熔断
  - 日志记录

### 2. 销售分析服务 (sales-service)
- **端口**: 8001
- **技术**: Python + Dash + Flask REST API
- **数据来源**: Madhav Dashboard
- **功能**:
  - 销售数据API
  - 商品分析API
  - 趋势分析API
  - Dash可视化

### 3. 客户分析服务 (customer-service)
- **端口**: 8002
- **技术**: Python + Streamlit + FastAPI
- **数据来源**: Data Storytelling Dashboard
- **功能**:
  - 客户数据API
  - RFM分析API
  - 留存分析API
  - Streamlit可视化

### 4. TikTok分析服务 (tiktok-service)
- **端口**: 8003
- **技术**: Python + Streamlit + FastAPI
- **数据来源**: TikTok Analytics
- **功能**:
  - TikTok数据API
  - 视频分析API
  - 直播数据API
  - Streamlit可视化

### 5. 前端应用 (frontend)
- **端口**: 3000
- **技术**: React + Ant Design
- **功能**:
  - 统一登录界面
  - 服务导航
  - 数据展示
  - 图表集成

## API 设计规范

### 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 错误码定义
- 200: 成功
- 400: 请求参数错误
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器内部错误
- 503: 服务不可用

### 服务端点

#### 销售分析服务 (/api/v1/sales)
- `GET /health` - 健康检查
- `GET /dashboard` - 获取Dash看板
- `GET /api/overview` - 销售概览数据
- `GET /api/trends` - 销售趋势数据
- `GET /api/products` - 商品分析数据
- `GET /api/categories` - 类别分析数据

#### 客户分析服务 (/api/v1/customers)
- `GET /health` - 健康检查
- `GET /dashboard` - 获取Streamlit看板
- `GET /api/overview` - 客户概览数据
- `GET /api/rfm` - RFM分析数据
- `GET /api/retention` - 留存分析数据
- `GET /api/segments` - 客户分层数据

#### TikTok分析服务 (/api/v1/tiktok)
- `GET /health` - 健康检查
- `GET /dashboard` - 获取Streamlit看板
- `GET /api/overview` - TikTok概览数据
- `GET /api/videos` - 视频分析数据
- `GET /api/live` - 直播数据分析
- `GET /api/trends` - 趋势分析数据

## 服务间通信

### 同步通信 (REST API)
- 服务间通过HTTP/REST API通信
- 使用API Gateway统一路由
- 服务注册与发现

### 异步通信 (消息队列)
- 使用Redis作为消息队列
- 数据同步事件
- 日志收集

## 数据流

```
1. 用户请求 → API Gateway
2. API Gateway → 认证服务
3. API Gateway → 具体服务
4. 服务 → 数据库
5. 服务 → 返回数据
6. API Gateway → 前端
```

## 部署架构

### Docker Compose (开发环境)
```yaml
services:
  - api-gateway
  - sales-service
  - customer-service
  - tiktok-service
  - frontend
  - postgres
  - redis
```

### Kubernetes (生产环境)
- 每个服务独立Deployment
- Service暴露端口
- Ingress统一入口
- ConfigMap配置管理
- Secret密钥管理

## 监控与日志

### 监控
- Prometheus + Grafana
- 服务健康检查
- 性能指标收集

### 日志
- ELK Stack (Elasticsearch + Logstash + Kibana)
- 统一日志格式
- 分布式追踪

## 安全

- HTTPS通信
- JWT认证
- API限流
- 数据加密
- 访问控制
