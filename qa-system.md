# 智能问答

## 概述

RAGForge 的智能问答系统基于先进的 RAG（Retrieval-Augmented Generation）技术，能够从您的知识库中检索相关信息并生成准确、有用的回答。

## 核心特性

### 1. 智能检索

- **语义搜索**：基于向量相似度的语义检索
- **混合检索**：结合关键词和语义搜索
- **上下文理解**：理解问题的上下文和意图
- **多文档检索**：从多个相关文档中获取信息

### 2. 高质量回答

- **准确回答**：基于知识库内容生成准确回答
- **引用来源**：提供回答的文档来源
- **多语言支持**：支持中文、英文等多种语言
- **格式保持**：保持原始文档的格式和结构

### 3. 实时处理

- **快速响应**：毫秒级的检索和回答生成
- **并发处理**：支持多用户同时提问
- **缓存机制**：智能缓存提高响应速度

## 使用方法

### 1. Web 界面问答

#### 基本问答

1. 登录 RAGForge 管理后台
2. 选择目标知识库
3. 在问答界面输入问题
4. 点击"提问"按钮
5. 查看生成的回答和来源

#### 高级设置

- **检索数量**：设置检索的相关文档数量
- **相似度阈值**：设置文档相似度过滤阈值
- **回答长度**：控制回答的详细程度
- **语言设置**：选择回答的语言

### 2. API 问答

#### 基本问答

```javascript
import { RAGForge } from 'ragforge';

const client = new RAGForge({
  apiKey: 'your_api_key'
});

// 基本问答
const response = await client.ask({
  question: '如何安装 RAGForge？',
  knowledgeBaseId: 'your_kb_id'
});

console.log('回答:', response.answer);
console.log('来源:', response.sources);
```

#### 高级问答

```javascript
// 带参数的问答
const response = await client.ask({
  question: 'RAGForge 支持哪些文件格式？',
  knowledgeBaseId: 'your_kb_id',
  options: {
    topK: 5,                    // 检索文档数量
    similarityThreshold: 0.7,   // 相似度阈值
    maxTokens: 1000,            // 最大回答长度
    temperature: 0.3,           // 创造性参数
    language: 'zh-CN'           // 回答语言
  }
});
```

#### 流式回答

```javascript
// 流式回答（实时显示）
const stream = await client.askStream({
  question: '请详细介绍 RAGForge 的功能',
  knowledgeBaseId: 'your_kb_id'
});

for await (const chunk of stream) {
  if (chunk.type === 'answer') {
    process.stdout.write(chunk.content);
  } else if (chunk.type === 'source') {
    console.log('\n来源:', chunk.document);
  }
}
```

### 3. 批量问答

```javascript
// 批量处理多个问题
const questions = [
  '什么是 RAGForge？',
  '如何部署 RAGForge？',
  'RAGForge 的定价如何？'
];

const responses = await Promise.all(
  questions.map(q => 
    client.ask({
      question: q,
      knowledgeBaseId: 'your_kb_id'
    })
  )
);

responses.forEach((response, index) => {
  console.log(`问题 ${index + 1}:`, questions[index]);
  console.log(`回答:`, response.answer);
  console.log('---');
});
```

## 问答配置

### 检索配置

```javascript
// 配置检索参数
await client.updateKnowledgeBaseConfig({
  knowledgeBaseId: 'your_kb_id',
  retrieval: {
    topK: 5,                    // 检索文档数量
    similarityThreshold: 0.7,   // 相似度阈值
    rerankEnabled: true,        // 启用重排序
    hybridSearch: true,         // 启用混合搜索
    maxContextLength: 4000      // 最大上下文长度
  }
});
```

### 回答配置

```javascript
// 配置回答生成参数
await client.updateKnowledgeBaseConfig({
  knowledgeBaseId: 'your_kb_id',
  generation: {
    model: 'gpt-4',             // 使用的模型
    temperature: 0.3,           // 创造性参数
    maxTokens: 1000,            // 最大回答长度
    systemPrompt: '你是一个专业的 AI 助手...', // 系统提示
    includeSources: true        // 包含来源信息
  }
});
```

## 问答历史

### 查看历史记录

```javascript
// 获取问答历史
const history = await client.getQaHistory({
  knowledgeBaseId: 'your_kb_id',
  userId: 'user_id',
  page: 1,
  limit: 20
});

console.log('历史记录:', history.items);
```

### 历史记录管理

```javascript
// 删除历史记录
await client.deleteQaHistory({
  historyId: 'history_id'
});

// 清空用户历史
await client.clearQaHistory({
  userId: 'user_id',
  knowledgeBaseId: 'your_kb_id'
});
```

## 问答分析

### 使用统计

```javascript
// 获取问答统计
const stats = await client.getQaStats({
  knowledgeBaseId: 'your_kb_id',
  period: 'last_30_days'
});

console.log('总提问数:', stats.totalQuestions);
console.log('平均响应时间:', stats.avgResponseTime);
console.log('用户满意度:', stats.satisfactionRate);
```

### 热门问题

```javascript
// 获取热门问题
const popularQuestions = await client.getPopularQuestions({
  knowledgeBaseId: 'your_kb_id',
  period: 'last_7_days',
  limit: 10
});

console.log('热门问题:', popularQuestions);
```

## 问答优化

### 1. 问题优化

- **明确问题**：使用清晰、具体的问题描述
- **关键词使用**：包含相关的关键词
- **上下文提供**：提供必要的背景信息

### 2. 知识库优化

- **文档质量**：确保知识库文档准确、完整
- **文档组织**：合理组织文档结构
- **定期更新**：保持知识库内容的最新性

### 3. 配置调优

- **检索参数**：根据实际需求调整检索参数
- **模型选择**：选择合适的 AI 模型
- **缓存策略**：优化缓存配置

## 常见问题

### Q: 为什么回答不准确？
A: 可能的原因包括：
- 知识库中缺少相关信息
- 检索参数设置不当
- 问题描述不够清晰

### Q: 如何提高回答质量？
A: 建议：
- 优化知识库文档质量
- 调整检索和生成参数
- 提供更详细的问题描述

### Q: 支持哪些语言？
A: RAGForge 支持中文、英文等多种语言，可以根据需要设置回答语言。

### Q: 如何处理敏感信息？
A: 系统提供敏感信息过滤功能，可以配置关键词过滤和内容审核规则。 