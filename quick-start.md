# 5分钟快速上手

## 概述

RAGForge 是一个强大的企业级 AI 知识库解决方案，基于 RAG（Retrieval-Augmented Generation）技术，为企业提供智能问答、知识管理、流程自动化的一站式 AI 助手平台。

## 快速开始

### 1. 环境准备

确保您的系统满足以下要求：

- Python 3.8 或更高版本
- Node.js 18.0 或更高版本（用于前端）
- Docker 和 Docker Compose
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 2. 克隆项目

```bash
# 克隆 RAGForge 项目
git clone https://github.com/zhaozhilong1993/ragflow.git
cd ragflow

# 更新子模块
git submodule update --init --recursive
```

### 3. 后端配置

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库等信息
```

### 4. 前端配置

```bash
# 进入前端目录
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 5. 启动服务

```bash
# 启动后端服务
python -m uvicorn app.main:app --reload

# 前端服务已在另一个终端启动
```

## 创建第一个知识库

### 1. 访问系统

打开浏览器访问 `http://localhost:3000`，使用默认账号登录系统。

### 2. 创建知识库

1. 点击"知识库管理"
2. 点击"新建知识库"
3. 填写知识库名称和描述
4. 选择文档处理方式

### 3. 上传文档

1. 在知识库详情页面点击"上传文档"
2. 选择要上传的文档文件
3. 系统会自动解析和处理文档

### 4. 进行问答

1. 点击"智能问答"
2. 在对话框中输入您的问题
3. 系统会基于知识库内容给出准确答案

## API 使用示例

### 1. 认证

```python
import requests

# 获取访问令牌
response = requests.post('http://localhost:8000/api/auth/login', json={
    'username': 'your_username',
    'password': 'your_password'
})

token = response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
```

### 2. 上传文档

```python
# 上传文档到知识库
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {'knowledge_base_id': 'your_kb_id'}
    response = requests.post(
        'http://localhost:8000/api/knowledge/upload',
        files=files,
        data=data,
        headers=headers
    )
```

### 3. 问答

```python
# 进行问答
response = requests.post('http://localhost:8000/api/chat/ask', json={
    'question': '您的问题',
    'knowledge_base_id': 'your_kb_id'
}, headers=headers)

answer = response.json()['answer']
```

## 下一步

- 查看 [知识库管理](/docs/knowledge-base) 了解如何管理您的知识库
- 学习 [API 参考](/docs/api-reference) 进行深度集成
- 探索 [部署指南](/docs/docker-deployment) 进行生产环境部署

## 常见问题

### Q: 支持哪些文档格式？
A: RAGForge 支持 PDF、Word、Excel、PowerPoint、TXT、Markdown 等多种格式。

### Q: 如何处理大文件？
A: 系统会自动分块处理大文件，确保处理效率和准确性。

### Q: 是否支持多语言？
A: 是的，RAGForge 支持中文、英文等多种语言的文档和问答。

### Q: 如何配置数据库？
A: 系统默认使用 SQLite，生产环境建议使用 PostgreSQL。详细配置请参考部署文档。 