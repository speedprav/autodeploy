# Installation & Setup Guide

## Prerequisites

- **Python 3.11+** — [Download](https://python.org)
- **Git** — [Download](https://git-scm.com)
- **Docker** (optional) — [Download](https://docker.com)
- **Minikube** (optional, for K8s) — [Download](https://minikube.sigs.k8s.io)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/speedprav/pdeploy.git
cd pdeploy
```

### 2. Create Virtual Environment

#### On macOS/Linux:
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

#### On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### On Windows (CMD):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r app/requirements.txt
```

**What's installed:**
- **fastapi** (0.104.1) — Web framework
- **uvicorn** (0.24.0) — ASGI server
- **pydantic** (2.5.0) — Data validation
- **pytest** (7.4.3) — Testing
- **prometheus-fastapi-instrumentator** (6.1.0) — Metrics

### 4. Run Tests

```bash
cd app
pytest tests/ -v
```

**Expected output:**
```
tests/test_main.py::test_health_returns_200 PASSED
tests/test_main.py::test_health_returns_healthy_status PASSED
tests/test_main.py::test_health_has_timestamp PASSED
tests/test_main.py::test_info_returns_200 PASSED
tests/test_main.py::test_info_has_required_fields PASSED
tests/test_main.py::test_info_correct_project_name PASSED
tests/test_main.py::test_predict_returns_200 PASSED
tests/test_main.py::test_predict_positive_sentiment PASSED
tests/test_main.py::test_predict_negative_sentiment PASSED
tests/test_main.py::test_predict_returns_word_count PASSED
tests/test_main.py::test_predict_empty_text_returns_400 PASSED
tests/test_main.py::test_predict_has_confidence_score PASSED

============================== 12 passed ==============================
```

### 5. Start the Development Server

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 6. Access the API

- **API Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **Metrics:** http://localhost:8000/metrics

---

## Docker Setup

### Build Docker Image

```bash
# From project root directory
docker build -t pdeploy:latest .
```

### Run Docker Container

```bash
docker run -p 8000:8000 pdeploy:latest
```

**Or with environment variable:**
```bash
docker run -p 8000:8000 -e ENV=production pdeploy:latest
```

### Using Docker Compose

```bash
docker-compose up
```

**Access at:** http://localhost:8000/docs

**Stop container:**
```bash
docker-compose down
```

---

## Kubernetes Setup (Local)

### Prerequisites

1. **Install Minikube**
   ```bash
   # macOS with Homebrew
   brew install minikube

   # Windows with Chocolatey
   choco install minikube

   # Or download from: https://minikube.sigs.k8s.io/docs/start/
   ```

2. **Install kubectl**
   ```bash
   # macOS
   brew install kubectl

   # Windows (with Chocolatey)
   choco install kubernetes-cli

   # Or: https://kubernetes.io/docs/tasks/tools/
   ```

### Start Minikube

```bash
minikube start --driver=docker --cpus=2 --memory=4096
```

**Verify it's running:**
```bash
kubectl get nodes
```

### Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f k8s/deployment.yaml

# Apply service
kubectl apply -f k8s/service.yaml

# Apply ingress
kubectl apply -f k8s/ingress.yaml
```

### Verify Deployment

```bash
# Check pods
kubectl get pods --watch

# Check services
kubectl get svc

# View pod logs
kubectl logs -f deployment/pdeploy
```

### Access the App

**Get the service URL:**
```bash
minikube service pdeploy-service --url
```

**Or manually:**
```bash
kubectl port-forward svc/pdeploy-service 8000:80
# Now access at http://localhost:8000
```

---

## Prometheus & Grafana Setup

### Install with Helm

1. **Add Prometheus Helm repository**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. **Create monitoring namespace**
   ```bash
   kubectl create namespace monitoring
   ```

3. **Install kube-prometheus-stack**
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack \
     --namespace monitoring \
     --values monitoring/prometheus-values.yaml
   ```

4. **Verify installation**
   ```bash
   kubectl get all -n monitoring
   ```

### Access Grafana Dashboard

```bash
# Port forward to Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

**Access at:** http://localhost:3000

**Default credentials:**
- Username: `admin`
- Password: `pdeploy-admin`

### Access Prometheus UI

```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

**Access at:** http://localhost:9090

---

## Environment Variables

Create `.env` file (optional):

```env
ENV=production
LOG_LEVEL=INFO
PORT=8000
HOST=0.0.0.0
```

**Usage in Python:**
```python
import os
env = os.getenv("ENV", "development")
```

---

## Project Structure

```
pdeploy/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   └── tests/
│       ├── __init__.py
│       └── test_main.py        # Test suite (12 tests)
├── k8s/
│   ├── deployment.yaml         # K8s deployment (2 replicas)
│   ├── service.yaml            # K8s service (NodePort)
│   ├── ingress.yaml            # Ingress configuration
│   └── servicemonitor.yaml     # Prometheus integration
├── monitoring/
│   └── prometheus-values.yaml  # Helm values for monitoring
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Local dev environment
├── .dockerignore               # Docker exclusions
├── .gitignore                  # Git exclusions
├── README.md                   # Project overview
└── docs/                       # Documentation
    ├── API.md                  # API documentation
    ├── SETUP.md                # This file
    ├── ARCHITECTURE.md         # Architecture details
    ├── DEPLOYMENT.md           # Deployment guide
    └── CONTRIBUTING.md         # Contributing guidelines
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Virtual Environment Issues

```bash
# Deactivate current venv
deactivate

# Remove old venv
rm -rf .venv  # macOS/Linux
rmdir /s .venv  # Windows

# Create fresh venv
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
```

### Docker Issues

```bash
# Remove dangling images
docker image prune -a

# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t pdeploy:latest .
```

### Minikube Issues

```bash
# Reset Minikube
minikube delete
minikube start --driver=docker

# Check Minikube status
minikube status

# View Minikube logs
minikube logs
```

---

## Next Steps

- Read [API Documentation](API.md) for endpoint details
- Check [Architecture Guide](ARCHITECTURE.md) for system design
- See [Deployment Guide](DEPLOYMENT.md) for cloud deployment
- Review [Contributing Guidelines](CONTRIBUTING.md) to contribute

---

## Getting Help

- **GitHub Issues:** https://github.com/speedprav/pdeploy/issues
- **Documentation:** See other files in `/docs`
- **API Docs:** Run app and visit http://localhost:8000/docs
