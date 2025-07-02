# 知识库管理

## 概述

知识库是 RAGForge 的核心功能，它允许您上传、管理和组织各种类型的文档，并通过 AI 技术提供智能问答服务。

## 创建知识库

### 1. 通过 Web 界面创建

1. 登录 RAGForge 管理后台
2. 点击"创建知识库"按钮
3. 填写知识库基本信息：
   - 名称：知识库的显示名称
   - 描述：知识库的详细描述
   - 分类：选择知识库所属分类
   - 权限：设置访问权限

### 2. 通过 API 创建

```javascript
import { RAGForge } from 'ragforge';

const client = new RAGForge({
  apiKey: 'your_api_key'
});

// 创建知识库
const knowledgeBase = await client.createKnowledgeBase({
  name: '产品文档库',
  description: '包含所有产品相关的文档和说明',
  category: 'product',
  permissions: {
    read: ['user1', 'user2'],
    write: ['admin']
  }
});

console.log('知识库 ID:', knowledgeBase.id);
```

## 上传文档

### 支持的文档格式

- **PDF 文档** (.pdf)
- **Word 文档** (.docx, .doc)
- **Excel 表格** (.xlsx, .xls)
- **PowerPoint 演示文稿** (.pptx, .ppt)
- **文本文件** (.txt)
- **Markdown 文件** (.md)
- **HTML 文件** (.html)

### 批量上传

```javascript
// 批量上传多个文档
const files = [file1, file2, file3];

for (const file of files) {
  await client.uploadDocument({
    file: file,
    knowledgeBaseId: 'your_kb_id',
    metadata: {
      category: 'manual',
      author: 'John Doe',
      version: '1.0'
    }
  });
}
```

### 文档预处理

系统会自动对上传的文档进行以下处理：

1. **文本提取**：从各种格式中提取纯文本内容
2. **分块处理**：将长文档分割成适合 AI 处理的小块
3. **向量化**：将文本转换为向量表示
4. **索引建立**：建立高效的检索索引

## 文档管理

### 查看文档列表

```javascript
// 获取知识库中的所有文档
const documents = await client.listDocuments({
  knowledgeBaseId: 'your_kb_id',
  page: 1,
  limit: 20
});

console.log('文档列表:', documents.items);
```

### 更新文档

```javascript
// 更新文档元数据
await client.updateDocument({
  documentId: 'doc_id',
  metadata: {
    title: '更新后的标题',
    description: '更新后的描述',
    tags: ['tag1', 'tag2']
  }
});
```

### 删除文档

```javascript
// 删除单个文档
await client.deleteDocument({
  documentId: 'doc_id'
});

// 批量删除文档
await client.deleteDocuments({
  documentIds: ['doc1', 'doc2', 'doc3']
});
```

## 知识库训练

### 手动训练

```javascript
// 开始训练知识库
const trainingJob = await client.trainKnowledgeBase({
  knowledgeBaseId: 'your_kb_id',
  options: {
    model: 'gpt-4',
    chunkSize: 1000,
    overlap: 200
  }
});

// 检查训练状态
const status = await client.getTrainingStatus({
  jobId: trainingJob.id
});
```

### 自动训练

您可以设置自动训练规则：

```javascript
// 设置自动训练
await client.setAutoTraining({
  knowledgeBaseId: 'your_kb_id',
  enabled: true,
  schedule: {
    frequency: 'daily',
    time: '02:00'
  }
});
```

## 知识库配置

### 检索设置

```javascript
// 配置检索参数
await client.updateKnowledgeBaseConfig({
  knowledgeBaseId: 'your_kb_id',
  retrieval: {
    topK: 5,
    similarityThreshold: 0.7,
    rerankEnabled: true
  }
});
```

### 权限管理

```javascript
// 设置知识库权限
await client.updateKnowledgeBasePermissions({
  knowledgeBaseId: 'your_kb_id',
  permissions: {
    read: ['user1', 'user2', 'group1'],
    write: ['admin', 'editor'],
    admin: ['admin']
  }
});
```

## 监控和分析

### 使用统计

```javascript
// 获取知识库使用统计
const stats = await client.getKnowledgeBaseStats({
  knowledgeBaseId: 'your_kb_id',
  period: 'last_30_days'
});

console.log('文档数量:', stats.documentCount);
console.log('查询次数:', stats.queryCount);
console.log('平均响应时间:', stats.avgResponseTime);
```

### 性能监控

系统提供以下监控指标：

- **文档处理时间**：文档上传和处理的耗时
- **查询响应时间**：问答请求的响应时间
- **准确率统计**：问答结果的准确性
- **用户满意度**：用户对回答的评分

## 最佳实践

### 1. 文档组织

- 按主题或功能对文档进行分类
- 使用清晰的命名规范
- 定期清理过期文档

### 2. 内容质量

- 确保文档内容准确、完整
- 避免重复或冗余信息
- 保持文档的时效性

### 3. 权限控制

- 根据用户角色设置适当的访问权限
- 定期审查权限设置
- 记录权限变更日志

### 4. 性能优化

- 合理设置文档分块大小
- 定期进行知识库训练
- 监控系统资源使用情况 