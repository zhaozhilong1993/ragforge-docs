# 身份认证

## 概述

RAGForge 提供多种身份认证方式，确保系统安全性和用户访问控制。

## 认证方式

### 1. 用户名密码认证

#### 基本登录

    import { RAGForge } from 'ragforge';
    
    const client = new RAGForge({
      apiKey: 'your_api_key'
    });
    
    // 用户登录
    const session = await client.login({
      email: 'user@example.com',
      password: 'password'
    });
    
    console.log('登录成功:', session.userId);
    console.log('访问令牌:', session.accessToken);
    

#### 密码策略

- **最小长度**：8 个字符
- **复杂度要求**：包含大小写字母、数字和特殊字符
- **定期更换**：建议每 90 天更换一次
- **历史记录**：不能使用最近 5 次用过的密码

### 2. 双因素认证 (2FA)

#### 启用 2FA

    // 启用双因素认证
    const setupResult = await client.setup2FA({
      userId: 'user_id',
      method: 'totp' // 或 'sms', 'email'
    });
    
    console.log('二维码:', setupResult.qrCode);
    console.log('备用码:', setupResult.backupCodes);
    

#### 验证 2FA

    // 验证双因素认证
    const isValid = await client.verify2FA({
      userId: 'user_id',
      code: '123456'
    });
    
    if (isValid) {
      console.log('2FA 验证成功');
    }
    

### 3. OAuth 认证

#### 配置 OAuth 提供商

    // 配置 Google OAuth
    await client.configureOAuth({
      provider: 'google',
      clientId: 'your_google_client_id',
      clientSecret: 'your_google_client_secret',
      redirectUri: 'https://your-app.com/auth/google/callback'
    });
    
    // 配置 GitHub OAuth
    await client.configureOAuth({
      provider: 'github',
      clientId: 'your_github_client_id',
      clientSecret: 'your_github_client_secret',
      redirectUri: 'https://your-app.com/auth/github/callback'
    });
    

#### OAuth 登录流程

    // 获取授权 URL
    const authUrl = await client.getOAuthUrl({
      provider: 'google',
      state: 'random_state_string'
    });
    
    // 处理回调
    const token = await client.handleOAuthCallback({
      provider: 'google',
      code: 'authorization_code',
      state: 'random_state_string'
    });
    

### 4. SAML SSO

#### 配置 SAML

    // 配置 SAML SSO
    await client.configureSAML({
      entityId: 'your_entity_id',
      ssoUrl: 'https://idp.example.com/sso',
      sloUrl: 'https://idp.example.com/slo',
      certificate: 'certificate_content',
      privateKey: 'private_key_content'
    });
    

#### SAML 登录

    // 生成 SAML 请求
    const samlRequest = await client.generateSAMLRequest({
      relayState: 'return_url'
    });
    
    // 处理 SAML 响应
    const userInfo = await client.handleSAMLResponse({
      samlResponse: 'saml_response_content'
    });
    

### 5. LDAP 认证

#### 配置 LDAP

    // 配置 LDAP 连接
    await client.configureLDAP({
      server: 'ldap://ldap.example.com:389',
      baseDN: 'dc=example,dc=com',
      bindDN: 'cn=admin,dc=example,dc=com',
      bindPassword: 'admin_password',
      userSearchBase: 'ou=users,dc=example,dc=com',
      userSearchFilter: '(uid={{username}})'
    });
    

#### LDAP 认证

    // LDAP 用户认证
    const user = await client.authenticateLDAP({
      username: 'user123',
      password: 'password'
    });
    
    if (user) {
      console.log('LDAP 认证成功:', user);
    }
    

## 令牌管理

### 1. 访问令牌

    // 生成访问令牌
    const token = await client.generateAccessToken({
      userId: 'user_id',
      scopes: ['read', 'write'],
      expiresIn: '1h'
    });
    
    // 验证访问令牌
    const payload = await client.verifyAccessToken({
      token: 'access_token'
    });
    
    // 撤销访问令牌
    await client.revokeAccessToken({
      token: 'access_token'
    });
    

### 2. 刷新令牌

    // 刷新访问令牌
    const newSession = await client.refreshToken({
      refreshToken: 'refresh_token'
    });
    
    // 撤销刷新令牌
    await client.revokeRefreshToken({
      refreshToken: 'refresh_token'
    });
    

### 3. API 密钥

    // 生成 API 密钥
    const apiKey = await client.generateAPIKey({
      userId: 'user_id',
      name: 'My API Key',
      scopes: ['read', 'write'],
      expiresAt: '2024-12-31'
    });
    
    // 验证 API 密钥
    const keyInfo = await client.verifyAPIKey({
      apiKey: 'api_key'
    });
    
    // 撤销 API 密钥
    await client.revokeAPIKey({
      apiKeyId: 'key_id'
    });
    

## 会话管理

### 1. 会话创建

    // 创建用户会话
    const session = await client.createSession({
      userId: 'user_id',
      deviceInfo: {
        userAgent: 'Mozilla/5.0...',
        ipAddress: '192.168.1.1',
        deviceId: 'device_123'
      },
      expiresIn: '24h'
    });
    

### 2. 会话验证

    // 验证会话
    const sessionInfo = await client.verifySession({
      sessionId: 'session_id'
    });
    
    if (sessionInfo.valid) {
      console.log('会话有效:', sessionInfo.userId);
    } else {
      console.log('会话已过期');
    }
    

### 3. 会话管理

    // 获取用户会话列表
    const sessions = await client.getUserSessions({
      userId: 'user_id'
    });
    
    // 终止指定会话
    await client.terminateSession({
      sessionId: 'session_id'
    });
    
    // 终止所有会话
    await client.terminateAllSessions({
      userId: 'user_id'
    });
    

## 安全功能

### 1. 密码安全

    // 密码强度检查
    const strength = await client.checkPasswordStrength({
      password: 'password'
    });
    
    console.log('密码强度:', strength.score); // 0-4
    console.log('建议:', strength.suggestions);
    
    // 密码重置
    await client.resetPassword({
      email: 'user@example.com',
      resetToken: 'reset_token',
      newPassword: 'new_password'
    });
    

### 2. 登录保护

    // 检查登录尝试
    const attempts = await client.getLoginAttempts({
      email: 'user@example.com',
      timeWindow: '1h'
    });
    
    if (attempts.count > 5) {
      console.log('账户已被锁定');
    }
    
    // 解锁账户
    await client.unlockAccount({
      email: 'user@example.com'
    });
    

### 3. 设备管理

    // 获取用户设备列表
    const devices = await client.getUserDevices({
      userId: 'user_id'
    });
    
    // 撤销设备访问
    await client.revokeDevice({
      deviceId: 'device_id'
    });
    
    // 标记设备为受信任
    await client.trustDevice({
      deviceId: 'device_id',
      userId: 'user_id'
    });
    

## 审计日志

### 1. 认证日志

    // 获取认证日志
    const authLogs = await client.getAuthLogs({
      userId: 'user_id',
      startDate: '2024-01-01',
      endDate: '2024-01-31',
      action: 'login'
    });
    
    console.log('认证记录:', authLogs);
    

### 2. 安全事件

    // 获取安全事件
    const securityEvents = await client.getSecurityEvents({
      userId: 'user_id',
      eventType: 'failed_login',
      severity: 'high'
    });
    
    console.log('安全事件:', securityEvents);
    

## 最佳实践

### 1. 密码安全

- 使用强密码策略
- 定期更换密码
- 启用双因素认证
- 监控异常登录

### 2. 令牌管理

- 设置合理的过期时间
- 定期轮换 API 密钥
- 及时撤销不需要的令牌
- 使用 HTTPS 传输

### 3. 访问控制

- 实施最小权限原则
- 定期审查访问权限
- 监控异常访问行为
- 记录所有访问日志

### 4. 安全监控

- 实时监控安全事件
- 设置告警机制
- 定期安全审计
- 及时响应安全威胁 