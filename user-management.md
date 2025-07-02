# 用户管理

## 概述

RAGForge 提供完整的用户管理系统，支持用户注册、认证、权限控制和团队协作功能。

## 用户类型

### 1. 超级管理员

- 拥有系统所有权限
- 可以管理所有用户和知识库
- 可以配置系统设置

### 2. 管理员

- 管理指定知识库的用户
- 可以创建和管理用户
- 可以配置知识库设置

### 3. 编辑者

- 可以上传和管理文档
- 可以训练知识库
- 可以查看使用统计

### 4. 查看者

- 只能查看和搜索文档
- 可以进行问答
- 不能修改内容

## 用户管理功能

### 1. 用户注册

#### Web 界面注册

```javascript
// 用户注册
const user = await client.registerUser({
  email: 'user@example.com',
  password: 'secure_password',
  name: '张三',
  role: 'viewer'
});
```

#### 邀请注册

```javascript
// 发送邀请邮件
await client.sendInvitation({
  email: 'newuser@example.com',
  role: 'editor',
  knowledgeBaseId: 'kb_id',
  message: '欢迎加入我们的团队！'
});
```

### 2. 用户认证

#### 登录认证

```javascript
// 用户登录
const session = await client.login({
  email: 'user@example.com',
  password: 'password'
});

console.log('登录成功:', session.userId);
console.log('访问令牌:', session.accessToken);
```

#### 令牌管理

```javascript
// 刷新访问令牌
const newSession = await client.refreshToken({
  refreshToken: session.refreshToken
});

// 验证令牌
const isValid = await client.verifyToken({
  accessToken: session.accessToken
});
```

### 3. 权限管理

#### 角色分配

```javascript
// 分配用户角色
await client.assignRole({
  userId: 'user_id',
  knowledgeBaseId: 'kb_id',
  role: 'editor'
});
```

#### 权限检查

```javascript
// 检查用户权限
const permissions = await client.getUserPermissions({
  userId: 'user_id',
  knowledgeBaseId: 'kb_id'
});

console.log('用户权限:', permissions);
```

### 4. 团队管理

#### 创建团队

```javascript
// 创建团队
const team = await client.createTeam({
  name: '产品团队',
  description: '负责产品文档管理',
  ownerId: 'owner_id'
});
```

#### 团队成员管理

```javascript
// 添加团队成员
await client.addTeamMember({
  teamId: 'team_id',
  userId: 'user_id',
  role: 'member'
});

// 移除团队成员
await client.removeTeamMember({
  teamId: 'team_id',
  userId: 'user_id'
});
```

## 用户配置

### 1. 个人设置

```javascript
// 更新用户信息
await client.updateUser({
  userId: 'user_id',
  name: '新姓名',
  avatar: 'avatar_url',
  preferences: {
    language: 'zh-CN',
    theme: 'dark',
    notifications: true
  }
});
```

### 2. 安全设置

```javascript
// 修改密码
await client.changePassword({
  userId: 'user_id',
  oldPassword: 'old_password',
  newPassword: 'new_password'
});

// 启用双因素认证
await client.enable2FA({
  userId: 'user_id'
});
```

## 用户监控

### 1. 活动日志

```javascript
// 获取用户活动日志
const activities = await client.getUserActivities({
  userId: 'user_id',
  startDate: '2024-01-01',
  endDate: '2024-01-31'
});

console.log('用户活动:', activities);
```

### 2. 使用统计

```javascript
// 获取用户使用统计
const stats = await client.getUserStats({
  userId: 'user_id',
  period: 'last_30_days'
});

console.log('登录次数:', stats.loginCount);
console.log('操作次数:', stats.actionCount);
console.log('最后登录:', stats.lastLogin);
```

## 安全功能

### 1. 访问控制

- **IP 白名单**：限制特定 IP 地址访问
- **时间限制**：设置访问时间窗口
- **设备限制**：限制登录设备数量

### 2. 审计日志

```javascript
// 获取审计日志
const auditLogs = await client.getAuditLogs({
  userId: 'user_id',
  action: 'document_upload',
  startDate: '2024-01-01',
  endDate: '2024-01-31'
});
```

### 3. 异常检测

- **异常登录检测**：检测异常登录行为
- **权限滥用检测**：监控权限使用情况
- **数据泄露检测**：监控敏感数据访问

## 集成选项

### 1. SSO 集成

```javascript
// 配置 SSO
await client.configureSSO({
  provider: 'saml',
  config: {
    entityId: 'your_entity_id',
    ssoUrl: 'https://idp.example.com/sso',
    certificate: 'certificate_content'
  }
});
```

### 2. LDAP 集成

```javascript
// 配置 LDAP
await client.configureLDAP({
  server: 'ldap://ldap.example.com',
  baseDN: 'dc=example,dc=com',
  bindDN: 'cn=admin,dc=example,dc=com',
  bindPassword: 'password'
});
```

### 3. OAuth 集成

```javascript
// 配置 OAuth
await client.configureOAuth({
  provider: 'google',
  clientId: 'your_client_id',
  clientSecret: 'your_client_secret',
  redirectUri: 'https://your-app.com/auth/callback'
});
```

## 最佳实践

### 1. 权限最小化

- 只授予用户必要的权限
- 定期审查权限设置
- 使用角色继承简化管理

### 2. 安全监控

- 定期检查用户活动
- 监控异常行为
- 及时处理安全事件

### 3. 用户培训

- 提供安全培训
- 制定使用规范
- 定期更新安全策略

### 4. 备份恢复

- 定期备份用户数据
- 测试恢复流程
- 制定灾难恢复计划 