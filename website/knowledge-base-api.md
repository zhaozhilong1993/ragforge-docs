# 知识库 API

RAGForge 后台启动后，可通过访问 [http://localhost:9380/apidocs](http://localhost:9380/apidocs) 查看所有可用 API 接口的详细文档和在线调试。

## 示例：创建知识库

    POST /knowledge-bases

请求体示例：

    {
      "name": "企业文档库",
      "description": "存储企业重要文档"
    }

## 概述

RAGForge 知识库 API 提供了完整的知识库管理功能，包括创建、配置、文档管理和训练等操作。

## 认证

所有 API 请求都需要在请求头中包含 API 密钥：

    const headers = {
      'Authorization': 'Bearer your_api_key',
      'Content-Type': 'application/json'
    };
    

## 基础 URL

    https://api.ragforge.com/v1
    

## 知识库管理

### 创建知识库

**POST** `/knowledge-bases`

创建一个新的知识库。

#### 请求参数

    {
      "name": "产品文档库",
      "description": "包含所有产品相关的文档和说明",
      "category": "product",
      "permissions": {
        "read": ["user1", "user2"],
        "write": ["admin"],
        "admin": ["admin"]
      },
      "config": {
        "retrieval": {
          "topK": 5,
          "similarityThreshold": 0.7
        },
        "generation": {
          "model": "gpt-4",
          "temperature": 0.3
        }
      }
    }
    

#### 响应

    {
      "id": "kb_123456789",
      "name": "产品文档库",
      "description": "包含所有产品相关的文档和说明",
      "category": "product",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "status": "active"
    }
    

### 获取知识库列表

**GET** `/knowledge-bases`

获取用户有权限访问的知识库列表。

#### 查询参数

- `page` (number): 页码，默认为 1
- `limit` (number): 每页数量，默认为 20
- `category` (string): 按分类过滤
- `status` (string): 按状态过滤

#### 响应

    {
      "items": [
        {
          "id": "kb_123456789",
          "name": "产品文档库",
          "description": "包含所有产品相关的文档和说明",
          "category": "product",
          "documentCount": 150,
          "createdAt": "2024-01-01T00:00:00Z",
          "updatedAt": "2024-01-01T00:00:00Z",
          "status": "active"
        }
      ],
      "total": 1,
      "page": 1,
      "limit": 20
    }
    

### 获取知识库详情

**GET** `/knowledge-bases/{id}`

获取指定知识库的详细信息。

#### 响应

    {
      "id": "kb_123456789",
      "name": "产品文档库",
      "description": "包含所有产品相关的文档和说明",
      "category": "product",
      "permissions": {
        "read": ["user1", "user2"],
        "write": ["admin"],
        "admin": ["admin"]
      },
      "config": {
        "retrieval": {
          "topK": 5,
          "similarityThreshold": 0.7,
          "rerankEnabled": true
        },
        "generation": {
          "model": "gpt-4",
          "temperature": 0.3,
          "maxTokens": 1000
        }
      },
      "stats": {
        "documentCount": 150,
        "totalSize": 1024000,
        "lastTrainingAt": "2024-01-01T00:00:00Z",
        "trainingStatus": "completed"
      },
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "status": "active"
    }
    

### 更新知识库

**PUT** `/knowledge-bases/{id}`

更新知识库的基本信息和配置。

#### 请求参数

    {
      "name": "更新后的名称",
      "description": "更新后的描述",
      "config": {
        "retrieval": {
          "topK": 10,
          "similarityThreshold": 0.8
        }
      }
    }
    

### 删除知识库

**DELETE** `/knowledge-bases/{id}`

删除指定的知识库及其所有文档。

## 文档管理

### 上传文档

**POST** `/knowledge-bases/{id}/documents`

向知识库上传新文档。

#### 请求参数

    // 使用 FormData
    const formData = new FormData();
    formData.append('file', fileObject);
    formData.append('metadata', JSON.stringify({
      title: '文档标题',
      description: '文档描述',
      category: 'manual',
      author: '作者姓名',
      version: '1.0',
      tags: ['标签1', '标签2']
    }));
    

#### 响应

    {
      "id": "doc_123456789",
      "name": "document.pdf",
      "title": "文档标题",
      "size": 1024000,
      "status": "processing",
      "uploadedAt": "2024-01-01T00:00:00Z"
    }
    

### 获取文档列表

**GET** `/knowledge-bases/{id}/documents`

获取知识库中的文档列表。

#### 查询参数

- `page` (number): 页码
- `limit` (number): 每页数量
- `category` (string): 按分类过滤
- `status` (string): 按状态过滤
- `search` (string): 搜索关键词

#### 响应

    {
      "items": [
        {
          "id": "doc_123456789",
          "name": "document.pdf",
          "title": "文档标题",
          "description": "文档描述",
          "category": "manual",
          "size": 1024000,
          "status": "processed",
          "uploadedAt": "2024-01-01T00:00:00Z",
          "processedAt": "2024-01-01T00:01:00Z"
        }
      ],
      "total": 1,
      "page": 1,
      "limit": 20
    }
    

### 获取文档详情

**GET** `/knowledge-bases/{id}/documents/{documentId}`

获取指定文档的详细信息。

#### 响应

    {
      "id": "doc_123456789",
      "name": "document.pdf",
      "title": "文档标题",
      "description": "文档描述",
      "category": "manual",
      "author": "作者姓名",
      "version": "1.0",
      "tags": ["标签1", "标签2"],
      "size": 1024000,
      "status": "processed",
      "metadata": {
        "pageCount": 10,
        "wordCount": 5000,
        "language": "zh-CN"
      },
      "uploadedAt": "2024-01-01T00:00:00Z",
      "processedAt": "2024-01-01T00:01:00Z"
    }
    

### 更新文档

**PUT** `/knowledge-bases/{id}/documents/{documentId}`

更新文档的元数据。

#### 请求参数

    {
      "title": "更新后的标题",
      "description": "更新后的描述",
      "category": "updated_category",
      "tags": ["新标签1", "新标签2"]
    }
    

### 删除文档

**DELETE** `/knowledge-bases/{id}/documents/{documentId}`

删除指定的文档。

### 批量删除文档

**DELETE** `/knowledge-bases/{id}/documents`

批量删除多个文档。

#### 请求参数

    {
      "documentIds": ["doc1", "doc2", "doc3"]
    }
    

## 知识库训练

### 开始训练

**POST** `/knowledge-bases/{id}/train`

开始训练知识库。

#### 请求参数

    {
      "options": {
        "model": "gpt-4",
        "chunkSize": 1000,
        "overlap": 200,
        "rerankEnabled": true
      }
    }
    

#### 响应

    {
      "jobId": "train_123456789",
      "status": "started",
      "startedAt": "2024-01-01T00:00:00Z"
    }
    

### 获取训练状态

**GET** `/knowledge-bases/{id}/train/{jobId}`

获取训练任务的当前状态。

#### 响应

    {
      "jobId": "train_123456789",
      "status": "running",
      "progress": 75,
      "startedAt": "2024-01-01T00:00:00Z",
      "estimatedCompletion": "2024-01-01T00:30:00Z",
      "processedDocuments": 100,
      "totalDocuments": 150
    }
    

### 取消训练

**DELETE** `/knowledge-bases/{id}/train/{jobId}`

取消正在进行的训练任务。

## 权限管理

### 更新权限

**PUT** `/knowledge-bases/{id}/permissions`

更新知识库的访问权限。

#### 请求参数

    {
      "permissions": {
        "read": ["user1", "user2", "group1"],
        "write": ["admin", "editor"],
        "admin": ["admin"]
      }
    }
    

### 获取权限

**GET** `/knowledge-bases/{id}/permissions`

获取知识库的当前权限设置。

## 统计信息

### 获取统计

**GET** `/knowledge-bases/{id}/stats`

获取知识库的使用统计信息。

#### 查询参数

- `period` (string): 统计周期，如 "last_7_days", "last_30_days"

#### 响应

    {
      "documentCount": 150,
      "totalSize": 1024000,
      "queryCount": 1000,
      "avgResponseTime": 1.5,
      "satisfactionRate": 0.95,
      "lastTrainingAt": "2024-01-01T00:00:00Z",
      "trainingStatus": "completed"
    }
    

## 错误处理

### 错误响应格式

    {
      "error": {
        "code": "INVALID_REQUEST",
        "message": "请求参数无效",
        "details": {
          "field": "name",
          "reason": "名称不能为空"
        }
      }
    }
    

### 常见错误码

- `INVALID_REQUEST`: 请求参数无效
- `UNAUTHORIZED`: 未授权访问
- `FORBIDDEN`: 权限不足
- `NOT_FOUND`: 资源不存在
- `CONFLICT`: 资源冲突
- `RATE_LIMITED`: 请求频率超限
- `INTERNAL_ERROR`: 服务器内部错误

## 速率限制

API 请求受到速率限制：

- 普通用户：100 请求/分钟
- 高级用户：1000 请求/分钟
- 企业用户：10000 请求/分钟

响应头中包含速率限制信息：

    X-RateLimit-Limit: 100
    X-RateLimit-Remaining: 95
    X-RateLimit-Reset: 1640995200
    

## SDK 示例

### JavaScript SDK

    import { RAGForge } from 'ragforge';
    
    const client = new RAGForge({
      apiKey: 'your_api_key'
    });
    
    // 创建知识库
    const kb = await client.createKnowledgeBase({
      name: '产品文档库',
      description: '产品相关文档',
      category: 'product'
    });
    
    // 上传文档
    const doc = await client.uploadDocument({
      knowledgeBaseId: kb.id,
      file: fileObject,
      metadata: {
        title: '产品手册',
        category: 'manual'
      }
    });
    
    // 开始训练
    const training = await client.trainKnowledgeBase({
      knowledgeBaseId: kb.id
    });
    

### Python SDK

    from ragforge import RAGForge
    
    client = RAGForge(api_key='your_api_key')
    
    # 创建知识库
    kb = client.create_knowledge_base(
        name='产品文档库',
        description='产品相关文档',
        category='product'
    )
    
    # 上传文档
    doc = client.upload_document(
        knowledge_base_id=kb.id,
        file=file_object,
        metadata={
            'title': '产品手册',
            'category': 'manual'
        }
    )
    
    # 开始训练
    training = client.train_knowledge_base(
        knowledge_base_id=kb.id
    )
     