# Docker 部署

## 概述

RAGForge 支持使用 Docker 进行快速部署，提供完整的容器化解决方案。

## 系统要求

### 硬件要求

- **CPU**: 4 核心或以上
- **内存**: 8GB 或以上
- **存储**: 50GB 可用空间
- **网络**: 稳定的网络连接

### 软件要求

- **Docker**: 20.10 或更高版本
- **Docker Compose**: 2.0 或更高版本
- **操作系统**: Linux, macOS, Windows

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/ragforge/ragforge.git
cd ragforge
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=postgresql://ragforge:password@postgres:5432/ragforge
POSTGRES_DB=ragforge
POSTGRES_USER=ragforge
POSTGRES_PASSWORD=password

# Redis 配置
REDIS_URL=redis://redis:6379

# 向量数据库配置
VECTOR_DB_URL=http://qdrant:6333

# API 配置
API_KEY=your_api_key_here
JWT_SECRET=your_jwt_secret_here

# 存储配置
STORAGE_TYPE=local
STORAGE_PATH=/app/storage

# AI 模型配置
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# 邮件配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_email_password

# 监控配置
ENABLE_MONITORING=true
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

### 3. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 初始化数据库

```bash
# 运行数据库迁移
docker-compose exec app npm run migrate

# 初始化管理员账户
docker-compose exec app npm run seed
```

### 5. 访问服务

- **Web 界面**: http://localhost:3000
- **API 文档**: http://localhost:3000/api/docs
- **监控面板**: http://localhost:3000/monitoring

## Docker Compose 配置

### 完整的 docker-compose.yml

```yaml
version: '3.8'

services:
  # 主应用服务
  app:
    image: ragforge/app:latest
    container_name: ragforge-app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - VECTOR_DB_URL=${VECTOR_DB_URL}
      - API_KEY=${API_KEY}
      - JWT_SECRET=${JWT_SECRET}
    volumes:
      - ./storage:/app/storage
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
      - qdrant
    restart: unless-stopped
    networks:
      - ragforge-network

  # PostgreSQL 数据库
  postgres:
    image: postgres:15-alpine
    container_name: ragforge-postgres
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - ragforge-network

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: ragforge-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped
    networks:
      - ragforge-network

  # Qdrant 向量数据库
  qdrant:
    image: qdrant/qdrant:latest
    container_name: ragforge-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped
    networks:
      - ragforge-network

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: ragforge-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - ragforge-network

  # Prometheus 监控
  prometheus:
    image: prom/prometheus:latest
    container_name: ragforge-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    restart: unless-stopped
    networks:
      - ragforge-network

  # Grafana 可视化
  grafana:
    image: grafana/grafana:latest
    container_name: ragforge-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    restart: unless-stopped
    networks:
      - ragforge-network

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  prometheus_data:
  grafana_data:

networks:
  ragforge-network:
    driver: bridge
```

## 配置详解

### Nginx 配置

创建 `nginx.conf` 文件：

```nginx
events {
    worker_connections 1024;
}

http {
    upstream ragforge {
        server app:3000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://ragforge;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api {
            proxy_pass http://ragforge;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Prometheus 配置

创建 `prometheus.yml` 文件：

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ragforge'
    static_configs:
      - targets: ['app:3000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

## 部署选项

### 1. 开发环境

```bash
# 使用开发配置
docker-compose -f docker-compose.dev.yml up -d

# 开发环境配置
version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
```

### 2. 生产环境

```bash
# 使用生产配置
docker-compose -f docker-compose.prod.yml up -d

# 启用 SSL
docker-compose -f docker-compose.prod.yml -f docker-compose.ssl.yml up -d
```

### 3. 高可用部署

```bash
# 使用 Swarm 模式
docker swarm init
docker stack deploy -c docker-compose.swarm.yml ragforge
```

## 数据持久化

### 备份数据库

```bash
# 备份 PostgreSQL
docker-compose exec postgres pg_dump -U ragforge ragforge > backup.sql

# 备份 Redis
docker-compose exec redis redis-cli BGSAVE

# 备份向量数据库
docker-compose exec qdrant qdrant backup /qdrant/backup
```

### 恢复数据

```bash
# 恢复 PostgreSQL
docker-compose exec -T postgres psql -U ragforge ragforge < backup.sql

# 恢复 Redis
docker-compose exec redis redis-cli FLUSHALL
# 复制 RDB 文件到容器

# 恢复向量数据库
docker-compose exec qdrant qdrant restore /qdrant/backup
```

## 监控和维护

### 健康检查

```bash
# 检查服务状态
docker-compose ps

# 检查应用健康
curl http://localhost:3000/health

# 检查数据库连接
docker-compose exec app npm run db:check
```

### 日志管理

```bash
# 查看应用日志
docker-compose logs -f app

# 查看数据库日志
docker-compose logs -f postgres

# 查看所有服务日志
docker-compose logs -f
```

### 性能监控

```bash
# 查看资源使用
docker stats

# 访问 Grafana 监控面板
# http://localhost:3001 (用户名: admin, 密码: admin)
```

## 故障排除

### 常见问题

1. **容器启动失败**
   ```bash
   # 检查日志
   docker-compose logs app
   
   # 重新构建镜像
   docker-compose build --no-cache
   ```

2. **数据库连接失败**
   ```bash
   # 检查数据库状态
   docker-compose exec postgres pg_isready
   
   # 重启数据库服务
   docker-compose restart postgres
   ```

3. **内存不足**
   ```bash
   # 增加 Docker 内存限制
   # 在 Docker Desktop 设置中调整内存限制
   ```

4. **端口冲突**
   ```bash
   # 修改端口映射
   # 在 docker-compose.yml 中修改 ports 配置
   ```

### 性能优化

1. **调整资源限制**
   ```yaml
   services:
     app:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

2. **启用缓存**
   ```yaml
   services:
     redis:
       command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
   ```

3. **优化数据库**
   ```yaml
   services:
     postgres:
       command: postgres -c shared_buffers=256MB -c max_connections=100
   ```

## 安全配置

### SSL/TLS 配置

```yaml
# docker-compose.ssl.yml
services:
  nginx:
    volumes:
      - ./ssl/cert.pem:/etc/nginx/ssl/cert.pem
      - ./ssl/key.pem:/etc/nginx/ssl/key.pem
    ports:
      - "443:443"
```

### 网络安全

```yaml
services:
  app:
    networks:
      - internal
    expose:
      - "3000"

networks:
  internal:
    internal: true
  external:
    external: true
```

## 扩展部署

### 水平扩展

```bash
# 扩展应用实例
docker-compose up -d --scale app=3

# 使用负载均衡器
docker-compose -f docker-compose.scale.yml up -d
```

### 多环境部署

```bash
# 开发环境
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 测试环境
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

# 生产环境
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
``` 