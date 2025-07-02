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

### 1. 安装 Python 3.8+
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip

# macOS
brew install python3
```

### 2. 安装 Node.js 18+
```bash
# 使用 nvm 安装
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### 3. 安装 Docker（可选）
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

## 开发环境部署

### 1. 克隆项目
```bash
git clone https://github.com/zhaozhilong1993/ragflow.git
cd ragflow

# 更新子模块
git submodule update --init --recursive
```

### 2. 后端配置
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库、API密钥等
```

### 3. 前端配置
```bash
# 进入前端目录
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 启动后端服务
```bash
# 在项目根目录
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 验证安装
访问 http://localhost:3000 查看管理界面

## 生产环境部署

### 1. 使用 Docker Compose
```bash
# 使用生产环境配置
docker-compose -f docker-compose.prod.yml up -d
```

### 2. 使用 Docker Swarm
```bash
# 初始化 Swarm
docker swarm init

# 部署服务
docker stack deploy -c docker-compose.prod.yml ragforge
```

### 3. 使用 Kubernetes
```bash
# 应用 Kubernetes 配置
kubectl apply -f k8s/
```

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

## 监控和维护

### 1. 日志查看
```bash
# 开发环境查看日志
tail -f logs/app.log

# Docker 环境查看日志
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
   - 检查 3000、8000、5432、6379 端口是否被占用
   - 修改配置文件中的端口设置

2. **内存不足**
   - 增加系统内存
   - 调整 Python 和 Node.js 内存限制

3. **磁盘空间不足**
   - 清理临时文件和日志
   - 扩展磁盘空间

4. **依赖安装失败**
   - 检查 Python 和 Node.js 版本
   - 使用国内镜像源加速下载

### 获取帮助
- 查看日志: `tail -f logs/app.log`
- 技术支持: support@ragforge.com
- 社区论坛: [forum.ragforge.com](https://forum.ragforge.com) 