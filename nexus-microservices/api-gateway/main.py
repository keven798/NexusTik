"""
NexusTik API Gateway
统一入口网关服务
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import time
from typing import Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI(
    title="NexusTik API Gateway",
    description="抖音电商数据分析平台统一API网关",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 服务配置
SERVICES = {
    "sales": {
        "name": "销售分析服务",
        "url": "http://localhost:8001",
        "health_endpoint": "/health",
        "enabled": True
    },
    "customers": {
        "name": "客户分析服务", 
        "url": "http://localhost:8002",
        "health_endpoint": "/health",
        "enabled": True
    },
    "tiktok": {
        "name": "TikTok分析服务",
        "url": "http://localhost:8003", 
        "health_endpoint": "/health",
        "enabled": True
    }
}

# JWT配置
JWT_SECRET = "nexustik-secret-key"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 24  # 小时

# 请求计数器（限流用）
request_counts = {}
RATE_LIMIT = 100  # 每分钟请求数

def create_token(user_id: str) -> str:
    """创建JWT令牌"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """验证JWT令牌"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def check_rate_limit(client_ip: str) -> bool:
    """检查限流"""
    now = time.time()
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    # 清理过期的请求记录
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip] 
        if now - req_time < 60
    ]
    
    # 检查是否超过限流
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        return False
    
    request_counts[client_ip].append(now)
    return True

async def forward_request(service_name: str, path: str, method: str = "GET", data: dict = None):
    """转发请求到具体服务"""
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"服务 {service_name} 不存在")
    
    service = SERVICES[service_name]
    if not service["enabled"]:
        raise HTTPException(status_code=503, detail=f"服务 {service_name} 当前不可用")
    
    url = f"{service['url']}{path}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, json=data, timeout=30.0)
            else:
                raise HTTPException(status_code=405, detail="不支持的HTTP方法")
            
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"服务请求失败: {str(e)}")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加处理时间头"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 健康检查
@app.get("/health")
async def health_check():
    """网关健康检查"""
    health_status = {
        "gateway": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    async with httpx.AsyncClient() as client:
        for service_name, service_config in SERVICES.items():
            try:
                response = await client.get(
                    f"{service_config['url']}{service_config['health_endpoint']}",
                    timeout=5.0
                )
                health_status["services"][service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time": response.elapsed.total_seconds()
                }
            except:
                health_status["services"][service_name] = {
                    "status": "unreachable",
                    "response_time": None
                }
    
    return health_status

# 服务状态
@app.get("/services")
async def list_services():
    """列出所有服务状态"""
    return {
        "services": [
            {
                "name": name,
                "description": config["name"],
                "url": config["url"],
                "enabled": config["enabled"]
            }
            for name, config in SERVICES.items()
        ]
    }

# 销售分析服务路由
@app.get("/api/v1/sales/{path:path}")
@app.post("/api/v1/sales/{path:path}")
async def sales_proxy(request: Request, path: str):
    """销售分析服务代理"""
    client_ip = request.client.host
    if not await check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="请求过于频繁")
    
    method = request.method
    data = await request.json() if method == "POST" else None
    
    return await forward_request("sales", f"/api/{path}", method, data)

# 客户分析服务路由
@app.get("/api/v1/customers/{path:path}")
@app.post("/api/v1/customers/{path:path}")
async def customers_proxy(request: Request, path: str):
    """客户分析服务代理"""
    client_ip = request.client.host
    if not await check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="请求过于频繁")
    
    method = request.method
    data = await request.json() if method == "POST" else None
    
    return await forward_request("customers", f"/api/{path}", method, data)

# TikTok分析服务路由
@app.get("/api/v1/tiktok/{path:path}")
@app.post("/api/v1/tiktok/{path:path}")
async def tiktok_proxy(request: Request, path: str):
    """TikTok分析服务代理"""
    client_ip = request.client.host
    if not await check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="请求过于频繁")
    
    method = request.method
    data = await request.json() if method == "POST" else None
    
    return await forward_request("tiktok", f"/api/{path}", method, data)

# 看板路由
@app.get("/dashboard/{service}")
async def dashboard_redirect(service: str):
    """重定向到各服务看板"""
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="服务不存在")
    
    service_url = SERVICES[service]["url"]
    return {
        "redirect_url": f"{service_url}/dashboard",
        "service": service,
        "message": f"请访问 {service_url} 查看看板"
    }

# 统一数据查询接口
@app.get("/api/v1/unified/overview")
async def unified_overview():
    """获取统一概览数据"""
    overview = {
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    async with httpx.AsyncClient() as client:
        # 并行请求所有服务的概览数据
        tasks = []
        for service_name, service_config in SERVICES.items():
            if service_config["enabled"]:
                try:
                    response = await client.get(
                        f"{service_config['url']}/api/overview",
                        timeout=10.0
                    )
                    overview["services"][service_name] = response.json()
                except:
                    overview["services"][service_name] = {"error": "服务不可用"}
    
    return overview

if __name__ == "__main__":
    import uvicorn
    print("🚀 NexusTik API Gateway 启动中...")
    print("📍 访问地址: http://localhost:8080")
    print("📖 API文档: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080)
