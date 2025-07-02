# 文档上传

## 概述

RAGForge 提供了强大的文档上传功能，支持多种文件格式，并能够自动处理文档的预处理、分块和向量化。

## 支持的文件格式

### 文档格式

- **PDF 文档** (.pdf) - 支持文本和图像 PDF
- **Word 文档** (.docx, .doc) - Microsoft Word 格式
- **Excel 表格** (.xlsx, .xls) - 包含表格数据
- **PowerPoint 演示文稿** (.pptx, .ppt) - 演示文稿文件
- **文本文件** (.txt) - 纯文本文件
- **Markdown 文件** (.md) - Markdown 格式文档
- **HTML 文件** (.html) - 网页文件

### 文件大小限制

- 单个文件最大：100MB
- 批量上传最大：1GB
- 支持的文件数量：无限制

## 上传方式

### 1. Web 界面上传

#### 单文件上传

1. 登录 RAGForge 管理后台
2. 选择目标知识库
3. 点击"上传文档"按钮
4. 选择要上传的文件
5. 填写文档元数据（可选）
6. 点击"开始上传"

#### 批量上传

1. 点击"批量上传"按钮
2. 选择多个文件（支持拖拽）
3. 设置批量元数据
4. 点击"开始上传"

### 2. API 上传

#### 单文件上传

```javascript
import { RAGForge } from 'ragforge';

const client = new RAGForge({
  apiKey: 'your_api_key'
});

// 上传单个文件
const result = await client.uploadDocument({
  file: fileObject,
  knowledgeBaseId: 'your_kb_id',
  metadata: {
    title: '文档标题',
    description: '文档描述',
    category: 'manual',
    author: '作者姓名',
    version: '1.0',
    tags: ['标签1', '标签2']
  }
});

console.log('上传成功:', result.documentId);
```

#### 批量上传

```javascript
// 批量上传多个文件
const files = [file1, file2, file3];
const uploadPromises = files.map(file => 
  client.uploadDocument({
    file: file,
    knowledgeBaseId: 'your_kb_id',
    metadata: {
      category: 'batch_upload',
      batchId: 'batch_001'
    }
  })
);

const results = await Promise.all(uploadPromises);
console.log('批量上传完成:', results.length, '个文件');
```

### 3. 命令行工具

```bash
# 安装命令行工具
npm install -g ragforge-cli

# 上传单个文件
ragforge upload --file document.pdf --kb your_kb_id

# 批量上传目录
ragforge upload --dir ./documents --kb your_kb_id

# 带元数据上传
ragforge upload --file document.pdf --kb your_kb_id --title "文档标题" --category "manual"
```

## 文档预处理

### 自动处理流程

上传的文档会自动经过以下处理步骤：

1. **文件验证**
   - 检查文件格式是否支持
   - 验证文件完整性
   - 检查文件大小限制

2. **文本提取**
   - 从各种格式中提取纯文本
   - 处理表格和图表数据
   - 保留文档结构信息

3. **内容清理**
   - 移除无用的格式标记
   - 标准化文本格式
   - 处理特殊字符

4. **分块处理**
   - 将长文档分割成小块
   - 保持语义完整性
   - 设置重叠区域

5. **向量化**
   - 将文本转换为向量表示
   - 建立检索索引
   - 优化存储结构

### 自定义预处理

```javascript
// 自定义分块参数
await client.uploadDocument({
  file: fileObject,
  knowledgeBaseId: 'your_kb_id',
  preprocessing: {
    chunkSize: 1000,        // 分块大小
    chunkOverlap: 200,      // 重叠大小
    minChunkSize: 100,      // 最小分块大小
    splitBy: 'paragraph'    // 分块方式：paragraph, sentence, token
  }
});
```

## 上传进度监控

### 实时进度

```javascript
// 监听上传进度
const uploadJob = await client.uploadDocument({
  file: fileObject,
  knowledgeBaseId: 'your_kb_id',
  onProgress: (progress) => {
    console.log(`上传进度: ${progress.percentage}%`);
    console.log(`已处理: ${progress.processedBytes}/${progress.totalBytes}`);
  }
});
```

### 批量上传状态

```javascript
// 获取批量上传状态
const batchStatus = await client.getBatchUploadStatus({
  batchId: 'batch_001'
});

console.log('总文件数:', batchStatus.totalFiles);
console.log('已完成:', batchStatus.completedFiles);
console.log('失败数:', batchStatus.failedFiles);
console.log('进度:', batchStatus.progress);
```

## 错误处理

### 常见错误

1. **文件格式不支持**
   ```javascript
   try {
     await client.uploadDocument({ file, knowledgeBaseId });
   } catch (error) {
     if (error.code === 'UNSUPPORTED_FORMAT') {
       console.log('文件格式不支持，请检查文件类型');
     }
   }
   ```

2. **文件大小超限**
   ```javascript
   if (file.size > 100 * 1024 * 1024) {
     console.log('文件大小超过 100MB 限制');
   }
   ```

3. **网络错误**
   ```javascript
   try {
     await client.uploadDocument({ file, knowledgeBaseId });
   } catch (error) {
     if (error.code === 'NETWORK_ERROR') {
       console.log('网络错误，请检查网络连接');
     }
   }
   ```

### 重试机制

```javascript
// 自动重试上传
const uploadWithRetry = async (file, knowledgeBaseId, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await client.uploadDocument({ file, knowledgeBaseId });
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      console.log(`上传失败，${i + 1}秒后重试...`);
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
};
```

## 最佳实践

### 1. 文件准备

- 确保文档内容清晰、完整
- 使用标准的文件格式
- 避免使用过大的文件

### 2. 元数据管理

- 为文档添加有意义的标题和描述
- 使用标签进行分类
- 记录文档版本信息

### 3. 批量上传

- 合理组织文件结构
- 使用批量上传提高效率
- 监控上传进度和错误

### 4. 质量控制

- 定期检查上传的文档
- 验证文档处理结果
- 及时处理错误和异常 