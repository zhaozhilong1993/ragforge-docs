# API 参考文档

## 概述

RAGForge 提供完整的 RESTful API 接口，支持知识库管理、文档上传、智能问答等功能。所有 API 都支持 JSON 格式的请求和响应。

## 认证

### API Key 认证
所有 API 请求都需要在请求头中包含 API Key：

    Authorization: Bearer your_api_key_here
    

### 获取 API Key
1. 登录 RAGForge 管理界面
2. 进入"设置" > "API 管理"
3. 创建新的 API Key

## 基础 URL
    https://api.ragforge.com/v1
    

## 知识库管理

### 创建知识库
    POST /knowledge-bases
    

**请求体：**
    {
      "name": "企业文档库",
      "description": "存储企业重要文档",
      "visibility": "private",
      "tags": ["企业", "文档"]
    }
    

**响应：**
    {
      "id": "kb_123456789",
      "name": "企业文档库",
      "description": "存储企业重要文档",
      "visibility": "private",
      "tags": ["企业", "文档"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
    

### 获取知识库列表
    GET /knowledge-bases
    

**查询参数：**
- `page`: 页码（默认 1）
- `limit`: 每页数量（默认 20）
- `visibility`: 可见性筛选（public/private）

### 获取知识库详情
    GET /knowledge-bases/{kb_id}
    

### 更新知识库
    PUT /knowledge-bases/{kb_id}
    

### 删除知识库
    DELETE /knowledge-bases/{kb_id}
    

## 文档管理

### 上传文档
    POST /knowledge-bases/{kb_id}/documents
    Content-Type: multipart/form-data
    

**请求体：**
- `file`: 文档文件
- `title`: 文档标题（可选）
- `description`: 文档描述（可选）
- `tags`: 标签数组（可选）

**响应：**
    {
      "id": "doc_123456789",
      "title": "产品手册.pdf",
      "filename": "产品手册.pdf",
      "size": 1024000,
      "status": "processing",
      "created_at": "2024-01-01T00:00:00Z"
    }
    

### 获取文档列表
    GET /knowledge-bases/{kb_id}/documents
    

**查询参数：**
- `page`: 页码
- `limit`: 每页数量
- `status`: 状态筛选（processing/completed/failed）

### 获取文档详情
    GET /knowledge-bases/{kb_id}/documents/{doc_id}
    

### 删除文档
    DELETE /knowledge-bases/{kb_id}/documents/{doc_id}
    

## 智能问答

### 提交问题
    POST /knowledge-bases/{kb_id}/questions
    

**请求体：**
    {
      "question": "什么是我们的产品策略？",
      "context": "请基于最新的产品文档回答",
      "max_tokens": 1000,
      "temperature": 0.7
    }
    

**响应：**
    {
      "id": "q_123456789",
      "question": "什么是我们的产品策略？",
      "answer": "根据我们的产品文档，我们的产品策略主要包括...",
      "sources": [
        {
          "document_id": "doc_123456789",
          "title": "产品手册.pdf",
          "page": 15,
          "content": "相关文档片段..."
        }
      ],
      "confidence": 0.95,
      "created_at": "2024-01-01T00:00:00Z"
    }
    

### 获取问答历史
    GET /knowledge-bases/{kb_id}/questions
    

### 获取问答详情
    GET /knowledge-bases/{kb_id}/questions/{question_id}
    

## 用户管理

### 获取用户信息
    GET /user/profile
    

### 更新用户信息
    PUT /user/profile
    

### 获取用户统计
    GET /user/stats
    

## 错误处理

### 错误响应格式
    {
      "error": {
        "code": "INVALID_REQUEST",
        "message": "请求参数无效",
        "details": {
          "field": "name",
          "reason": "知识库名称不能为空"
        }
      }
    }
    

### 常见错误码
- `400`: 请求参数错误
- `401`: 认证失败
- `403`: 权限不足
- `404`: 资源不存在
- `429`: 请求频率超限
- `500`: 服务器内部错误

## 速率限制

- 免费版：每分钟 60 次请求
- 专业版：每分钟 300 次请求
- 企业版：每分钟 1000 次请求

## SDK 示例

### Python SDK
    from ragforge import RAGForge
    
    client = RAGForge(api_key="your_api_key")
    
    # 创建知识库
    kb = client.create_knowledge_base(
        name="企业文档库",
        description="存储企业重要文档"
    )
    
    # 上传文档
    client.upload_document(
        kb_id=kb.id,
        file_path="document.pdf"
    )
    
    # 智能问答
    response = client.ask_question(
        kb_id=kb.id,
        question="什么是我们的产品策略？"
    )
    
    print(response.answer)
    

### JavaScript SDK
    import { RAGForge } from '@ragforge/sdk';
    
    const client = new RAGForge({
      apiKey: 'your_api_key'
    });
    
    // 创建知识库
    const kb = await client.createKnowledgeBase({
      name: '企业文档库',
      description: '存储企业重要文档'
    });
    
    // 上传文档
    await client.uploadDocument({
      kbId: kb.id,
      file: documentFile
    });
    
    // 智能问答
    const response = await client.askQuestion({
      kbId: kb.id,
      question: '什么是我们的产品策略？'
    });
    
    console.log(response.answer);
    

## 更多资源

- [SDK 下载](https://github.com/ragforge/sdk)
- [示例代码](https://github.com/ragforge/examples)
- [社区论坛](https://forum.ragforge.com)
- [技术支持](mailto:support@ragforge.com) 