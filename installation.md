# 安装部署指南

## 系统要求

### 最低配置
- CPU: 4 核
- 内存: 8GB RAM
- 存储: 50GB 可用空间
- 操作系统: Ubuntu 20.04+ / CentOS 8+ / macOS 10.15+

### 推荐配置
- CPU: 8 核
- 内存: 16GB RAM
- 存储: 100GB SSD
- 操作系统: Ubuntu 22.04 LTS

## 环境准备

### 1. 安装 Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# CentOS/RHEL
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 安装 Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## 快速部署

### 1. 下载安装包
```bash
git clone https://github.com/ragforge/ragforge.git
cd ragforge
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库、API密钥等
```

### 3. 启动服务
```bash
docker-compose up -d
```

### 4. 验证安装
访问 http://localhost:3000 查看管理界面

## 配置说明

### 数据库配置
```env
# PostgreSQL 配置
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ragforge
POSTGRES_USER=ragforge
POSTGRES_PASSWORD=your_password

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```

### AI 模型配置
```env
# OpenAI 配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

# 向量数据库配置
VECTOR_DB_HOST=localhost
VECTOR_DB_PORT=19530
```

## 生产环境部署

### 1. 使用 Docker Swarm
```bash
# 初始化 Swarm
docker swarm init

# 部署服务
docker stack deploy -c docker-compose.prod.yml ragforge
```

### 2. 使用 Kubernetes
```bash
# 应用 Kubernetes 配置
kubectl apply -f k8s/
```

## 监控和维护

### 1. 日志查看
```bash
# 查看服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f app
```

### 2. 数据备份
```bash
# 备份数据库
docker-compose exec postgres pg_dump -U ragforge ragforge > backup.sql

# 备份文件存储
tar -czf files_backup.tar.gz ./uploads/
```

### 3. 性能监控
- 使用 Prometheus + Grafana 监控系统性能
- 配置告警规则，及时发现问题

## 故障排除

### 常见问题

1. **端口冲突**
   - 检查 3000、5432、6379 端口是否被占用
   - 修改 docker-compose.yml 中的端口映射

2. **内存不足**
   - 增加系统内存
   - 调整 Docker 内存限制

3. **磁盘空间不足**
   - 清理 Docker 镜像和容器
   - 扩展磁盘空间

### 获取帮助
- 查看日志: `docker-compose logs`
- 技术支持: support@ragforge.com
- 社区论坛: [forum.ragforge.com](https://forum.ragforge.com) 