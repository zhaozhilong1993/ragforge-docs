# 问答 API

## 概述

RAGForge 问答 API 提供了强大的智能问答功能，支持基于知识库的准确回答生成。

## 基础 URL

```
https://api.ragforge.com/v1
```

## 认证

所有 API 请求都需要在请求头中包含 API 密钥：

```javascript
const headers = {
  'Authorization': 'Bearer your_api_key',
  'Content-Type': 'application/json'
};
```

## 基本问答

### 提问

**POST** `/qa/ask`

向知识库提问并获取回答。

#### 请求参数

```javascript
{
  "question": "如何安装 RAGForge？",
  "knowledgeBaseId": "kb_123456789",
  "options": {
    "topK": 5,
    "similarityThreshold": 0.7,
    "maxTokens": 1000,
    "temperature": 0.3,
    "language": "zh-CN"
  }
}
```

#### 响应

```javascript
{
  "answer": "RAGForge 的安装步骤如下：\n\n1. 确保系统满足要求...",
  "sources": [
    {
      "documentId": "doc_123",
      "title": "安装指南",
      "content": "相关文档片段...",
      "similarity": 0.95,
      "page": 1
    }
  ],
  "metadata": {
    "responseTime": 1.2,
    "tokensUsed": 150,
    "model": "gpt-4"
  }
}
```

### 流式问答

**POST** `/qa/ask/stream`

获取流式回答，实时返回生成的内容。

#### 请求参数

```javascript
{
  "question": "请详细介绍 RAGForge 的功能",
  "knowledgeBaseId": "kb_123456789",
  "stream": true
}
```

#### 响应格式

```
data: {"type": "answer", "content": "RAGForge 是一个强大的企业级 AI 知识库解决方案"}

data: {"type": "answer", "content": "，基于 RAG 技术..."}

data: {"type": "source", "document": {"id": "doc_123", "title": "产品介绍"}}

data: {"type": "done"}
```

## 批量问答

### 批量提问

**POST** `/qa/batch`

批量处理多个问题。

#### 请求参数

```javascript
{
  "questions": [
    {
      "question": "什么是 RAGForge？",
      "knowledgeBaseId": "kb_123456789"
    },
    {
      "question": "如何部署 RAGForge？",
      "knowledgeBaseId": "kb_123456789"
    }
  ],
  "options": {
    "maxTokens": 500,
    "temperature": 0.3
  }
}
```

#### 响应

```javascript
{
  "results": [
    {
      "question": "什么是 RAGForge？",
      "answer": "RAGForge 是一个企业级 AI 知识库解决方案...",
      "sources": [...],
      "metadata": {...}
    },
    {
      "question": "如何部署 RAGForge？",
      "answer": "部署 RAGForge 的步骤如下...",
      "sources": [...],
      "metadata": {...}
    }
  ]
}
```

## 高级功能

### 上下文问答

**POST** `/qa/ask/context`

支持上下文的连续问答。

#### 请求参数

```javascript
{
  "question": "它的价格是多少？",
  "knowledgeBaseId": "kb_123456789",
  "context": {
    "conversationId": "conv_123",
    "history": [
      {
        "question": "什么是 RAGForge？",
        "answer": "RAGForge 是一个企业级 AI 知识库解决方案..."
      }
    ]
  }
}
```

### 多知识库问答

**POST** `/qa/ask/multi`

从多个知识库中检索信息。

#### 请求参数

```javascript
{
  "question": "关于产品功能和定价的信息",
  "knowledgeBaseIds": ["kb_123", "kb_456"],
  "options": {
    "mergeStrategy": "weighted",
    "weights": {
      "kb_123": 0.7,
      "kb_456": 0.3
    }
  }
}
```

## 问答配置

### 获取配置

**GET** `/qa/config/{knowledgeBaseId}`

获取知识库的问答配置。

#### 响应

```javascript
{
  "retrieval": {
    "topK": 5,
    "similarityThreshold": 0.7,
    "rerankEnabled": true,
    "hybridSearch": true
  },
  "generation": {
    "model": "gpt-4",
    "temperature": 0.3,
    "maxTokens": 1000,
    "systemPrompt": "你是一个专业的 AI 助手..."
  }
}
```

### 更新配置

**PUT** `/qa/config/{knowledgeBaseId}`

更新知识库的问答配置。

#### 请求参数

```javascript
{
  "retrieval": {
    "topK": 10,
    "similarityThreshold": 0.8
  },
  "generation": {
    "temperature": 0.5,
    "maxTokens": 1500
  }
}
```

## 问答历史

### 获取历史记录

**GET** `/qa/history`

获取用户的问答历史记录。

#### 查询参数

- `knowledgeBaseId` (string): 知识库 ID
- `page` (number): 页码
- `limit` (number): 每页数量
- `startDate` (string): 开始日期
- `endDate` (string): 结束日期

#### 响应

```javascript
{
  "items": [
    {
      "id": "qa_123",
      "question": "如何安装 RAGForge？",
      "answer": "安装步骤如下...",
      "knowledgeBaseId": "kb_123",
      "askedAt": "2024-01-01T00:00:00Z",
      "responseTime": 1.2,
      "satisfaction": 5
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

### 删除历史记录

**DELETE** `/qa/history/{historyId}`

删除指定的问答历史记录。

### 清空历史记录

**DELETE** `/qa/history`

清空用户的所有问答历史记录。

## 问答分析

### 获取统计

**GET** `/qa/stats`

获取问答使用统计。

#### 查询参数

- `knowledgeBaseId` (string): 知识库 ID
- `period` (string): 统计周期

#### 响应

```javascript
{
  "totalQuestions": 1000,
  "avgResponseTime": 1.5,
  "satisfactionRate": 0.95,
  "popularQuestions": [
    {
      "question": "如何安装 RAGForge？",
      "count": 50
    }
  ],
  "dailyStats": [
    {
      "date": "2024-01-01",
      "questions": 25,
      "avgResponseTime": 1.3
    }
  ]
}
```

### 获取热门问题

**GET** `/qa/popular`

获取热门问题列表。

#### 响应

```javascript
{
  "questions": [
    {
      "question": "如何安装 RAGForge？",
      "count": 50,
      "lastAsked": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## 反馈功能

### 提交反馈

**POST** `/qa/feedback`

提交问答质量反馈。

#### 请求参数

```javascript
{
  "historyId": "qa_123",
  "rating": 5,
  "comment": "回答很准确，很有帮助",
  "category": "positive"
}
```

### 获取反馈

**GET** `/qa/feedback`

获取问答反馈列表。

## 错误处理

### 错误响应格式

```javascript
{
  "error": {
    "code": "INVALID_QUESTION",
    "message": "问题不能为空",
    "details": {
      "field": "question",
      "reason": "问题内容为空"
    }
  }
}
```

### 常见错误码

- `INVALID_QUESTION`: 问题格式无效
- `KNOWLEDGE_BASE_NOT_FOUND`: 知识库不存在
- `KNOWLEDGE_BASE_NOT_TRAINED`: 知识库未训练
- `RATE_LIMITED`: 请求频率超限
- `MODEL_ERROR`: 模型生成错误

## 速率限制

问答 API 的速率限制：

- 普通用户：60 请求/分钟
- 高级用户：600 请求/分钟
- 企业用户：6000 请求/分钟

## SDK 示例

### JavaScript SDK

```javascript
import { RAGForge } from 'ragforge';

const client = new RAGForge({
  apiKey: 'your_api_key'
});

// 基本问答
const response = await client.ask({
  question: '如何安装 RAGForge？',
  knowledgeBaseId: 'kb_123'
});

console.log('回答:', response.answer);
console.log('来源:', response.sources);

// 流式问答
const stream = await client.askStream({
  question: '请详细介绍 RAGForge',
  knowledgeBaseId: 'kb_123'
});

for await (const chunk of stream) {
  if (chunk.type === 'answer') {
    process.stdout.write(chunk.content);
  }
}
```

### Python SDK

```python
from ragforge import RAGForge

client = RAGForge(api_key='your_api_key')

# 基本问答
response = client.ask(
    question='如何安装 RAGForge？',
    knowledge_base_id='kb_123'
)

print('回答:', response.answer)
print('来源:', response.sources)

# 流式问答
stream = client.ask_stream(
    question='请详细介绍 RAGForge',
    knowledge_base_id='kb_123'
)

for chunk in stream:
    if chunk.type == 'answer':
        print(chunk.content, end='')
```

## 最佳实践

### 1. 问题优化

- 使用清晰、具体的问题描述
- 包含相关的关键词
- 提供必要的上下文信息

### 2. 配置调优

- 根据需求调整检索参数
- 选择合适的 AI 模型
- 优化系统提示词

### 3. 错误处理

- 实现重试机制
- 处理网络错误
- 监控 API 限制

### 4. 性能优化

- 使用流式回答提高用户体验
- 实现客户端缓存
- 批量处理多个问题 