# SDK 示例

## 概述

RAGForge 提供了多种编程语言的 SDK，方便开发者快速集成和使用。

## JavaScript/TypeScript SDK

### 安装

```bash
npm install ragforge
# 或
yarn add ragforge
```

### 基本使用

```javascript
import { RAGForge } from 'ragforge';

// 初始化客户端
const client = new RAGForge({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.ragforge.com/v1' // 可选
});

// 创建知识库
const knowledgeBase = await client.createKnowledgeBase({
  name: '产品文档库',
  description: '包含所有产品相关的文档',
  category: 'product'
});

console.log('知识库 ID:', knowledgeBase.id);
```

### 文档管理

```javascript
// 上传文档
const document = await client.uploadDocument({
  knowledgeBaseId: knowledgeBase.id,
  file: fileObject, // File 对象
  metadata: {
    title: '产品手册',
    description: '详细的产品使用说明',
    category: 'manual',
    author: '产品团队',
    version: '1.0',
    tags: ['产品', '手册', '指南']
  }
});

// 获取文档列表
const documents = await client.listDocuments({
  knowledgeBaseId: knowledgeBase.id,
  page: 1,
  limit: 20
});

console.log('文档列表:', documents.items);

// 更新文档
await client.updateDocument({
  documentId: document.id,
  metadata: {
    title: '更新后的标题',
    description: '更新后的描述'
  }
});

// 删除文档
await client.deleteDocument({
  documentId: document.id
});
```

### 知识库训练

```javascript
// 开始训练
const trainingJob = await client.trainKnowledgeBase({
  knowledgeBaseId: knowledgeBase.id,
  options: {
    model: 'gpt-4',
    chunkSize: 1000,
    overlap: 200,
    rerankEnabled: true
  }
});

// 检查训练状态
const status = await client.getTrainingStatus({
  jobId: trainingJob.id
});

console.log('训练进度:', status.progress + '%');
```

### 智能问答

```javascript
// 基本问答
const response = await client.ask({
  question: '如何安装 RAGForge？',
  knowledgeBaseId: knowledgeBase.id
});

console.log('回答:', response.answer);
console.log('来源:', response.sources);

// 带参数的问答
const response2 = await client.ask({
  question: 'RAGForge 支持哪些文件格式？',
  knowledgeBaseId: knowledgeBase.id,
  options: {
    topK: 5,
    similarityThreshold: 0.7,
    maxTokens: 1000,
    temperature: 0.3,
    language: 'zh-CN'
  }
});

// 流式问答
const stream = await client.askStream({
  question: '请详细介绍 RAGForge 的功能',
  knowledgeBaseId: knowledgeBase.id
});

for await (const chunk of stream) {
  if (chunk.type === 'answer') {
    process.stdout.write(chunk.content);
  } else if (chunk.type === 'source') {
    console.log('\n来源:', chunk.document);
  }
}
```

### 批量操作

```javascript
// 批量上传文档
const files = [file1, file2, file3];
const uploadPromises = files.map(file => 
  client.uploadDocument({
    knowledgeBaseId: knowledgeBase.id,
    file: file,
    metadata: {
      category: 'batch_upload',
      batchId: 'batch_001'
    }
  })
);

const results = await Promise.all(uploadPromises);
console.log('批量上传完成:', results.length, '个文件');

// 批量问答
const questions = [
  '什么是 RAGForge？',
  '如何部署 RAGForge？',
  'RAGForge 的定价如何？'
];

const responses = await Promise.all(
  questions.map(q => 
    client.ask({
      question: q,
      knowledgeBaseId: knowledgeBase.id
    })
  )
);

responses.forEach((response, index) => {
  console.log(`问题 ${index + 1}:`, questions[index]);
  console.log(`回答:`, response.answer);
  console.log('---');
});
```

### 错误处理

```javascript
try {
  const response = await client.ask({
    question: '测试问题',
    knowledgeBaseId: 'invalid_id'
  });
} catch (error) {
  if (error.code === 'KNOWLEDGE_BASE_NOT_FOUND') {
    console.log('知识库不存在');
  } else if (error.code === 'RATE_LIMITED') {
    console.log('请求频率超限，请稍后重试');
  } else {
    console.log('未知错误:', error.message);
  }
}
```

## Python SDK

### 安装

```bash
pip install ragforge
```

### 基本使用

```python
from ragforge import RAGForge

# 初始化客户端
client = RAGForge(api_key='your_api_key')

# 创建知识库
knowledge_base = client.create_knowledge_base(
    name='产品文档库',
    description='包含所有产品相关的文档',
    category='product'
)

print('知识库 ID:', knowledge_base.id)
```

### 文档管理

```python
# 上传文档
with open('document.pdf', 'rb') as f:
    document = client.upload_document(
        knowledge_base_id=knowledge_base.id,
        file=f,
        metadata={
            'title': '产品手册',
            'description': '详细的产品使用说明',
            'category': 'manual',
            'author': '产品团队',
            'version': '1.0',
            'tags': ['产品', '手册', '指南']
        }
    )

# 获取文档列表
documents = client.list_documents(
    knowledge_base_id=knowledge_base.id,
    page=1,
    limit=20
)

print('文档列表:', documents.items)

# 更新文档
client.update_document(
    document_id=document.id,
    metadata={
        'title': '更新后的标题',
        'description': '更新后的描述'
    }
)

# 删除文档
client.delete_document(document_id=document.id)
```

### 智能问答

```python
# 基本问答
response = client.ask(
    question='如何安装 RAGForge？',
    knowledge_base_id=knowledge_base.id
)

print('回答:', response.answer)
print('来源:', response.sources)

# 流式问答
stream = client.ask_stream(
    question='请详细介绍 RAGForge 的功能',
    knowledge_base_id=knowledge_base.id
)

for chunk in stream:
    if chunk.type == 'answer':
        print(chunk.content, end='')
    elif chunk.type == 'source':
        print('\n来源:', chunk.document)
```

## Java SDK

### 安装

```xml
<dependency>
    <groupId>com.ragforge</groupId>
    <artifactId>ragforge-java</artifactId>
    <version>1.0.0</version>
</dependency>
```

### 基本使用

```java
import com.ragforge.RAGForge;
import com.ragforge.RAGForgeClient;

// 初始化客户端
RAGForgeClient client = RAGForge.builder()
    .apiKey("your_api_key")
    .build();

// 创建知识库
KnowledgeBase knowledgeBase = client.createKnowledgeBase(
    CreateKnowledgeBaseRequest.builder()
        .name("产品文档库")
        .description("包含所有产品相关的文档")
        .category("product")
        .build()
);

System.out.println("知识库 ID: " + knowledgeBase.getId());
```

### 文档管理

```java
// 上传文档
File file = new File("document.pdf");
Document document = client.uploadDocument(
    UploadDocumentRequest.builder()
        .knowledgeBaseId(knowledgeBase.getId())
        .file(file)
        .metadata(DocumentMetadata.builder()
            .title("产品手册")
            .description("详细的产品使用说明")
            .category("manual")
            .author("产品团队")
            .version("1.0")
            .tags(Arrays.asList("产品", "手册", "指南"))
            .build())
        .build()
);

// 获取文档列表
DocumentList documents = client.listDocuments(
    ListDocumentsRequest.builder()
        .knowledgeBaseId(knowledgeBase.getId())
        .page(1)
        .limit(20)
        .build()
);

System.out.println("文档列表: " + documents.getItems());
```

### 智能问答

```java
// 基本问答
QAResponse response = client.ask(
    AskRequest.builder()
        .question("如何安装 RAGForge？")
        .knowledgeBaseId(knowledgeBase.getId())
        .build()
);

System.out.println("回答: " + response.getAnswer());
System.out.println("来源: " + response.getSources());
```

## Go SDK

### 安装

```bash
go get github.com/ragforge/ragforge-go
```

### 基本使用

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/ragforge/ragforge-go"
)

func main() {
    // 初始化客户端
    client := ragforge.NewClient("your_api_key")
    
    // 创建知识库
    kb, err := client.CreateKnowledgeBase(&ragforge.CreateKnowledgeBaseRequest{
        Name:        "产品文档库",
        Description: "包含所有产品相关的文档",
        Category:    "product",
    })
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("知识库 ID: %s\n", kb.ID)
}
```

### 文档管理

```go
// 上传文档
file, err := os.Open("document.pdf")
if err != nil {
    log.Fatal(err)
}
defer file.Close()

doc, err := client.UploadDocument(&ragforge.UploadDocumentRequest{
    KnowledgeBaseID: kb.ID,
    File:            file,
    Metadata: &ragforge.DocumentMetadata{
        Title:       "产品手册",
        Description: "详细的产品使用说明",
        Category:    "manual",
        Author:      "产品团队",
        Version:     "1.0",
        Tags:        []string{"产品", "手册", "指南"},
    },
})
if err != nil {
    log.Fatal(err)
}

fmt.Printf("文档 ID: %s\n", doc.ID)
```

### 智能问答

```go
// 基本问答
response, err := client.Ask(&ragforge.AskRequest{
    Question:        "如何安装 RAGForge？",
    KnowledgeBaseID: kb.ID,
})
if err != nil {
    log.Fatal(err)
}

fmt.Printf("回答: %s\n", response.Answer)
fmt.Printf("来源: %+v\n", response.Sources)
```

## 配置选项

### 客户端配置

```javascript
const client = new RAGForge({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.ragforge.com/v1',
  timeout: 30000, // 30 秒
  retries: 3,
  retryDelay: 1000, // 1 秒
  userAgent: 'MyApp/1.0.0'
});
```

### 请求配置

```javascript
// 自定义请求头
const response = await client.ask({
  question: '测试问题',
  knowledgeBaseId: 'kb_id'
}, {
  headers: {
    'X-Custom-Header': 'custom_value'
  }
});

// 设置超时
const response = await client.ask({
  question: '测试问题',
  knowledgeBaseId: 'kb_id'
}, {
  timeout: 60000 // 60 秒
});
```

## 最佳实践

### 1. 错误处理

```javascript
// 实现重试机制
const askWithRetry = async (question, knowledgeBaseId, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await client.ask({ question, knowledgeBaseId });
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      if (error.code === 'RATE_LIMITED') {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
      }
    }
  }
};
```

### 2. 批量处理

```javascript
// 批量处理带进度
const batchProcess = async (items, processor, batchSize = 10) => {
  const results = [];
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(item => processor(item))
    );
    results.push(...batchResults);
    console.log(`进度: ${Math.min(i + batchSize, items.length)}/${items.length}`);
  }
  return results;
};
```

### 3. 缓存机制

```javascript
// 简单的内存缓存
const cache = new Map();

const askWithCache = async (question, knowledgeBaseId) => {
  const key = `${question}:${knowledgeBaseId}`;
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const response = await client.ask({ question, knowledgeBaseId });
  cache.set(key, response);
  return response;
};
```

### 4. 监控和日志

```javascript
// 添加请求日志
const clientWithLogging = new RAGForge({
  apiKey: 'your_api_key',
  onRequest: (request) => {
    console.log('请求:', request.method, request.url);
  },
  onResponse: (response) => {
    console.log('响应:', response.status, response.url);
  }
});
``` 