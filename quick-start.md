# 5分钟快速上手

## 概述

RAGForge 是一个强大的企业级 AI 知识库解决方案，基于 RAG（Retrieval-Augmented Generation）技术，为企业提供智能问答、知识管理、流程自动化的一站式 AI 助手平台。

## 快速开始

### 1. 环境准备

确保您的系统满足以下要求：

- Node.js 18.0 或更高版本
- npm 或 yarn 包管理器
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 2. 安装 RAGForge

```bash
# 使用 npm 安装
npm install ragforge

# 或使用 yarn 安装
yarn add ragforge
```

### 3. 初始化项目

```bash
# 创建新的 RAGForge 项目
npx ragforge init my-knowledge-base

# 进入项目目录
cd my-knowledge-base
```

### 4. 配置环境变量

创建 `.env` 文件并配置必要的环境变量：

```env
# 数据库配置
DATABASE_URL=your_database_url

# API 密钥
API_KEY=your_api_key

# 向量数据库配置
VECTOR_DB_URL=your_vector_db_url
```

### 5. 启动服务

```bash
# 启动开发服务器
npm run dev

# 或启动生产服务器
npm start
```

## 创建第一个知识库

### 1. 上传文档

通过 Web 界面或 API 上传您的文档：

```javascript
import { RAGForge } from 'ragforge';

const client = new RAGForge({
  apiKey: 'your_api_key'
});

// 上传文档
await client.uploadDocument({
  file: documentFile,
  knowledgeBaseId: 'your_kb_id'
});
```

### 2. 训练知识库

```javascript
// 开始训练
await client.trainKnowledgeBase({
  knowledgeBaseId: 'your_kb_id'
});
```

### 3. 进行问答

```javascript
// 提问
const response = await client.ask({
  question: '您的问题',
  knowledgeBaseId: 'your_kb_id'
});

console.log(response.answer);
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