# Kubernetes 部署

## 概述

RAGForge 支持在 Kubernetes 集群中进行生产级部署，提供高可用性、可扩展性和自动化管理。

## 系统要求

### 集群要求

- **Kubernetes**: 1.24 或更高版本
- **节点数量**: 至少 3 个节点
- **CPU**: 每个节点至少 4 核心
- **内存**: 每个节点至少 8GB
- **存储**: 支持动态卷供应

### 必需组件

- **Ingress Controller**: Nginx, Traefik 或 Istio
- **Storage Class**: 支持 ReadWriteMany
- **Load Balancer**: 云提供商负载均衡器
- **Cert Manager**: 用于 SSL 证书管理

## 快速开始

### 1. 创建命名空间

```bash
kubectl create namespace ragforge
kubectl config set-context --current --namespace=ragforge
```

### 2. 创建 ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ragforge-config
data:
  DATABASE_URL: "postgresql://ragforge:password@ragforge-postgres:5432/ragforge"
  REDIS_URL: "redis://ragforge-redis:6379"
  VECTOR_DB_URL: "http://ragforge-qdrant:6333"
  STORAGE_TYPE: "local"
  STORAGE_PATH: "/app/storage"
  NODE_ENV: "production"
```

```bash
kubectl apply -f configmap.yaml
```

### 3. 创建 Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ragforge-secrets
type: Opaque
data:
  API_KEY: <base64-encoded-api-key>
  JWT_SECRET: <base64-encoded-jwt-secret>
  OPENAI_API_KEY: <base64-encoded-openai-key>
  ANTHROPIC_API_KEY: <base64-encoded-anthropic-key>
  POSTGRES_PASSWORD: <base64-encoded-password>
```

```bash
kubectl apply -f secret.yaml
```

### 4. 部署数据库

```yaml
# postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ragforge-postgres
spec:
  serviceName: ragforge-postgres
  replicas: 1
  selector:
    matchLabels:
      app: ragforge-postgres
  template:
    metadata:
      labels:
        app: ragforge-postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "ragforge"
        - name: POSTGRES_USER
          value: "ragforge"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: ragforge-secrets
              key: POSTGRES_PASSWORD
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: ragforge-postgres
spec:
  selector:
    app: ragforge-postgres
  ports:
  - port: 5432
    targetPort: 5432
  clusterIP: None
```

### 5. 部署 Redis

```yaml
# redis.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ragforge-redis
spec:
  serviceName: ragforge-redis
  replicas: 1
  selector:
    matchLabels:
      app: ragforge-redis
  template:
    metadata:
      labels:
        app: ragforge-redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        command: ["redis-server", "--appendonly", "yes"]
        volumeMounts:
        - name: redis-storage
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: redis-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 5Gi
---
apiVersion: v1
kind: Service
metadata:
  name: ragforge-redis
spec:
  selector:
    app: ragforge-redis
  ports:
  - port: 6379
    targetPort: 6379
  clusterIP: None
```

### 6. 部署 Qdrant

```yaml
# qdrant.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ragforge-qdrant
spec:
  serviceName: ragforge-qdrant
  replicas: 1
  selector:
    matchLabels:
      app: ragforge-qdrant
  template:
    metadata:
      labels:
        app: ragforge-qdrant
    spec:
      containers:
      - name: qdrant
        image: qdrant/qdrant:latest
        ports:
        - containerPort: 6333
        - containerPort: 6334
        volumeMounts:
        - name: qdrant-storage
          mountPath: /qdrant/storage
  volumeClaimTemplates:
  - metadata:
      name: qdrant-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: ragforge-qdrant
spec:
  selector:
    app: ragforge-qdrant
  ports:
  - port: 6333
    targetPort: 6333
  - port: 6334
    targetPort: 6334
  clusterIP: None
```

### 7. 部署主应用

```yaml
# app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ragforge-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ragforge-app
  template:
    metadata:
      labels:
        app: ragforge-app
    spec:
      containers:
      - name: app
        image: ragforge/app:latest
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: ragforge-config
        - secretRef:
            name: ragforge-secrets
        volumeMounts:
        - name: app-storage
          mountPath: /app/storage
        - name: app-logs
          mountPath: /app/logs
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: app-storage
        persistentVolumeClaim:
          claimName: ragforge-storage
      - name: app-logs
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: ragforge-app
spec:
  selector:
    app: ragforge-app
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ragforge-storage
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 20Gi
```

### 8. 部署 Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ragforge-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - ragforge.example.com
    secretName: ragforge-tls
  rules:
  - host: ragforge.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ragforge-app
            port:
              number: 80
```

### 9. 应用所有配置

```bash
# 按顺序部署
kubectl apply -f postgres.yaml
kubectl apply -f redis.yaml
kubectl apply -f qdrant.yaml
kubectl apply -f app.yaml
kubectl apply -f ingress.yaml

# 等待所有 Pod 就绪
kubectl wait --for=condition=ready pod -l app=ragforge-app --timeout=300s
```

## 高可用部署

### 1. 多副本部署

```yaml
# 修改 Deployment 的 replicas
spec:
  replicas: 5
```

### 2. 水平 Pod 自动扩缩容 (HPA)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ragforge-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ragforge-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 3. 垂直 Pod 自动扩缩容 (VPA)

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ragforge-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ragforge-app
  updatePolicy:
    updateMode: "Auto"
```

## 监控和日志

### 1. Prometheus 监控

```yaml
# prometheus.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: prometheus-config
          mountPath: /etc/prometheus
        - name: prometheus-storage
          mountPath: /prometheus
      volumes:
      - name: prometheus-config
        configMap:
          name: prometheus-config
      - name: prometheus-storage
        persistentVolumeClaim:
          claimName: prometheus-storage
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
```

### 2. Grafana 可视化

```yaml
# grafana.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          value: "admin"
        volumeMounts:
        - name: grafana-storage
          mountPath: /var/lib/grafana
      volumes:
      - name: grafana-storage
        persistentVolumeClaim:
          claimName: grafana-storage
---
apiVersion: v1
kind: Service
metadata:
  name: grafana
spec:
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
```

### 3. 日志收集

```yaml
# fluentd.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## 备份和恢复

### 1. 数据库备份

```yaml
# backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
spec:
  schedule: "0 2 * * *"  # 每天凌晨 2 点
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - |
              pg_dump -h ragforge-postgres -U ragforge -d ragforge > /backup/backup-$(date +%Y%m%d).sql
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: ragforge-secrets
                  key: POSTGRES_PASSWORD
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-storage
          restartPolicy: OnFailure
```

### 2. 数据恢复

```yaml
# restore-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: postgres-restore
spec:
  template:
    spec:
      containers:
      - name: restore
        image: postgres:15-alpine
        command:
        - /bin/sh
        - -c
        - |
          psql -h ragforge-postgres -U ragforge -d ragforge < /backup/backup-20240101.sql
        env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: ragforge-secrets
              key: POSTGRES_PASSWORD
        volumeMounts:
        - name: backup-storage
          mountPath: /backup
      volumes:
      - name: backup-storage
        persistentVolumeClaim:
          claimName: backup-storage
      restartPolicy: Never
```

## 安全配置

### 1. 网络策略

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ragforge-network-policy
spec:
  podSelector:
    matchLabels:
      app: ragforge-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: ragforge-postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: ragforge-redis
    ports:
    - protocol: TCP
      port: 6379
  - to:
    - podSelector:
        matchLabels:
          app: ragforge-qdrant
    ports:
    - protocol: TCP
      port: 6333
```

### 2. RBAC 配置

```yaml
# rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ragforge-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ragforge-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "endpoints"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ragforge-rolebinding
subjects:
- kind: ServiceAccount
  name: ragforge-sa
  namespace: ragforge
roleRef:
  kind: Role
  name: ragforge-role
  apiGroup: rbac.authorization.k8s.io
```

## 故障排除

### 1. 检查 Pod 状态

```bash
# 查看所有 Pod
kubectl get pods

# 查看 Pod 详情
kubectl describe pod <pod-name>

# 查看 Pod 日志
kubectl logs <pod-name>
```

### 2. 检查服务状态

```bash
# 查看所有服务
kubectl get services

# 测试服务连接
kubectl port-forward svc/ragforge-app 8080:80
```

### 3. 检查存储

```bash
# 查看 PVC
kubectl get pvc

# 查看 PV
kubectl get pv
```

### 4. 常见问题解决

```bash
# Pod 一直处于 Pending 状态
kubectl describe pod <pod-name>
# 检查资源是否足够

# Pod 一直处于 CrashLoopBackOff 状态
kubectl logs <pod-name>
# 检查应用配置和依赖

# 服务无法访问
kubectl get endpoints
# 检查服务选择器是否正确
```

## 性能优化

### 1. 资源限制

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

### 2. 节点亲和性

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/arch
          operator: In
          values:
          - amd64
```

### 3. Pod 反亲和性

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - ragforge-app
        topologyKey: kubernetes.io/hostname
``` 