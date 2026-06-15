# Deployment Guide

Deploy PDeploy to production using various platforms.

---

## Quick Deploy (Render.com) ✓ Deployed

**Live URL:** https://pdeploy-w7mg.onrender.com

### Steps

1. **Push code to GitHub** (already done ✓)

2. **Go to Render.com**
   - Sign up: https://render.com
   - Connect GitHub account

3. **Create Web Service**
   - New → Web Service
   - Select `speedprav/pdeploy` repo
   - Configure:
     - **Name:** `pdeploy`
     - **Region:** `Ohio` (or closest)
     - **Branch:** `main`
     - **Build command:** `pip install -r app/requirements.txt`
     - **Start command:** `cd app && uvicorn main:app --host 0.0.0.0 --port 8000`
     - **Plan:** Free

4. **Click Deploy**
   - Takes 2-5 minutes
   - Get public URL automatically

5. **Test**
   ```bash
   curl https://pdeploy-xxxxx.onrender.com/health
   ```

### Pros & Cons

**Pros:**
- ✅ Easiest setup (minutes)
- ✅ Free tier available
- ✅ Auto-deploys on git push
- ✅ HTTPS included
- ✅ Metrics & logs included

**Cons:**
- ❌ Free tier spins down after 15 min idle (slow startup)
- ❌ Limited to ~0.5 vCPU, 512MB RAM
- ❌ No native K8s (if you need it)

---

## Cloud Kubernetes Deployment

### Option 1: DigitalOcean ($6-12/month) ⭐ Recommended

#### Prerequisites
- DigitalOcean account
- `kubectl` installed
- Docker Hub account

#### Steps

1. **Create Kubernetes Cluster**
   - Go to: https://cloud.digitalocean.com
   - Kubernetes → Create Cluster
   - Configure:
     - Version: Latest stable
     - Nodes: 2 (1-node minimum)
     - Datacenter: Closest to you
     - Name: `pdeploy-cluster`
   - Cost: ~$6-12/month

2. **Download kubeconfig**
   ```bash
   # In DigitalOcean dashboard
   Cluster → Config Files → Download
   
   # Save to ~/.kube/config
   ```

3. **Verify connection**
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

4. **Create Docker registry secret**
   ```bash
   kubectl create secret docker-registry regcred \
     --docker-server=docker.io \
     --docker-username=YOUR_DOCKERHUB_USERNAME \
     --docker-password=YOUR_DOCKERHUB_TOKEN \
     --docker-email=your@email.com
   ```

5. **Deploy application**
   ```bash
   # Update image in deployment.yaml
   # Change: image: YOUR_USERNAME/pdeploy:latest
   
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

6. **Get public IP**
   ```bash
   kubectl get svc
   # Copy EXTERNAL-IP
   # Access at: http://EXTERNAL-IP:30080
   ```

7. **(Optional) Setup Ingress**
   ```bash
   # DigitalOcean provides ingress automatically
   # Or use Nginx Ingress Controller
   kubectl apply -f k8s/ingress.yaml
   ```

---

### Option 2: Google Cloud (GKE) - Free Trial

#### Steps

1. **Create GCP Project**
   - Go to: https://console.cloud.google.com
   - Create Project → Name: `pdeploy`

2. **Enable Kubernetes API**
   ```bash
   gcloud services enable container.googleapis.com
   ```

3. **Create GKE Cluster**
   ```bash
   gcloud container clusters create pdeploy-cluster \
     --zone us-central1-a \
     --num-nodes 1 \
     --machine-type n1-standard-1
   ```

4. **Get credentials**
   ```bash
   gcloud container clusters get-credentials pdeploy-cluster \
     --zone us-central1-a
   ```

5. **Deploy**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

6. **Get Load Balancer IP**
   ```bash
   kubectl get svc
   # Use EXTERNAL-IP
   ```

**Costs:**
- Free: $300 credits (12 months)
- After: $0.10-0.30/hour per node

---

### Option 3: AWS EKS - Free Tier Eligible

#### Prerequisites
- AWS Account
- AWS CLI configured
- `kubectl` installed

#### Steps

```bash
# 1. Create EKS cluster
aws eks create-cluster \
  --name pdeploy-cluster \
  --version 1.28 \
  --role-arn arn:aws:iam::ACCOUNT_ID:role/eks-service-role \
  --resources-vpc-config subnetIds=subnet-xxxxx,subnet-xxxxx

# 2. Get kubeconfig
aws eks update-kubeconfig --name pdeploy-cluster --region us-east-1

# 3. Create worker nodes
aws cloudformation create-stack \
  --stack-name pdeploy-nodes \
  --template-url https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-01/amazon-eks-nodegroup.yaml

# 4. Deploy
kubectl apply -f k8s/deployment.yaml
```

**Costs:**
- Cluster: $0.10/hour
- Nodes: $0.096/hour (t3.micro in free tier)
- Free tier: 1 year for t2.micro

---

## Advanced Deployments

### Helm Chart Deployment

1. **Create Helm chart**
   ```bash
   helm create pdeploy-chart
   ```

2. **Update values**
   ```bash
   # Edit pdeploy-chart/values.yaml
   image:
     repository: speedprav/pdeploy
     tag: latest
   replicas: 2
   ```

3. **Deploy**
   ```bash
   helm install pdeploy ./pdeploy-chart
   ```

4. **Upgrade**
   ```bash
   helm upgrade pdeploy ./pdeploy-chart
   ```

---

### GitOps (ArgoCD)

1. **Install ArgoCD**
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. **Create application**
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: pdeploy
     namespace: argocd
   spec:
     project: default
     source:
       repoURL: https://github.com/speedprav/pdeploy
       targetRevision: main
       path: k8s
     destination:
       server: https://kubernetes.default.svc
       namespace: default
   EOF
   ```

3. **Auto-syncs on git push!**

---

## Monitoring Production

### Prometheus on DigitalOcean

```bash
# Add Prometheus repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Install monitoring
helm install prometheus prometheus-community/kube-prometheus-stack \
  --values monitoring/prometheus-values.yaml
```

### Setup Alerting

```yaml
# monitoring/alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: pdeploy-alerts
spec:
  groups:
  - name: pdeploy
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
      for: 5m
      annotations:
        summary: High error rate detected
```

### Application Performance Monitoring (APM)

**Options:**
- New Relic (paid)
- DataDog (paid)
- Jaeger (open source, self-hosted)
- Elastic APM (open source)

---

## SSL/TLS Certificates

### Using Let's Encrypt (Free)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your@email.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Update Ingress
kubectl annotate ingress pdeploy-ingress cert-manager.io/cluster-issuer=letsencrypt-prod
```

---

## Auto-Scaling

### Horizontal Pod Autoscaling (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pdeploy-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pdeploy
  minReplicas: 2
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

```bash
kubectl apply -f k8s/hpa.yaml
kubectl get hpa --watch
```

---

## Backup & Restore

### Backup K8s Resources

```bash
# Backup everything
kubectl get all --all-namespaces -o yaml > cluster-backup.yaml

# Backup specific resource
kubectl get deployment pdeploy -o yaml > deployment-backup.yaml
```

### Restore

```bash
kubectl apply -f cluster-backup.yaml
```

### Persistent Data Backup

```bash
# Create PersistentVolumeClaim
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pdeploy-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
EOF

# Mount in deployment
volumes:
- name: data
  persistentVolumeClaim:
    claimName: pdeploy-data
```

---

## Troubleshooting Deployments

### Check Pod Status

```bash
# List pods
kubectl get pods

# Describe pod
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Stream logs
kubectl logs -f <pod-name>
```

### Common Issues

**Pods stuck in Pending**
```bash
# Check node capacity
kubectl describe nodes

# Check resource requests
kubectl describe pod <pod-name>
```

**CrashLoopBackOff**
```bash
# View crash logs
kubectl logs <pod-name> --previous

# Check probe configuration
kubectl get deployment pdeploy -o yaml | grep -A 10 livenessProbe
```

**ImagePullBackOff**
```bash
# Verify secret exists
kubectl get secret

# Check image pull secret
kubectl describe pod <pod-name> | grep Image
```

---

## Disaster Recovery Plan

### RTO/RPO Targets
- RTO (Recovery Time Objective): < 5 minutes
- RPO (Recovery Point Objective): < 1 minute (git history)

### DR Procedures

1. **Code recovery**: git clone from GitHub
2. **Container recovery**: Docker Hub registry
3. **K8s recovery**: kubectl apply from git repo
4. **Data recovery**: N/A (stateless app)

### Failover Procedure

```bash
# 1. Verify failed cluster
kubectl get nodes

# 2. Switch to backup cluster
kubectl config use-context <backup-cluster>

# 3. Deploy application
kubectl apply -f k8s/

# 4. Verify
kubectl get pods
curl https://backup-url/health
```

---

## Performance Tuning

### Load Testing

```bash
# Install Apache Bench
apt-get install apache2-utils

# Run load test (1000 requests, 10 concurrent)
ab -n 1000 -c 10 https://pdeploy-w7mg.onrender.com/health
```

### Resource Optimization

```bash
# Check current usage
kubectl top pods
kubectl top nodes

# Adjust resource limits if needed
kubectl set resources deployment pdeploy --limits=cpu=500m,memory=512Mi
```

---

## Cost Optimization

| Platform | Monthly Cost | Notes |
|----------|------------|-------|
| Render Free | $0 | Spins down after idle |
| DigitalOcean | $6-12 | Recommended |
| AWS Free Tier | $0-30 | After free year |
| GCP Free Trial | $0 | For 12 months |
| Azure | $15-30 | - |

### Cost Reduction Tips
1. Use spot/preemptible instances (70% cheaper)
2. Set resource limits properly
3. Auto-scale down when idle
4. Use free tier services
5. Monitor costs regularly

---

## Next Steps

- [ ] Deploy to DigitalOcean ($6/month)
- [ ] Setup SSL/TLS certificate
- [ ] Configure monitoring & alerting
- [ ] Setup auto-scaling
- [ ] Test disaster recovery
- [ ] Document runbooks
- [ ] Setup on-call rotation
