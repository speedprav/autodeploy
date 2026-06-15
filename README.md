# PDeploy — Production CI/CD Pipeline

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Automated-brightgreen)](https://github.com/YOUR_USERNAME/pdeploy/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://hub.docker.com/r/YOUR_USERNAME/pdeploy)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-326CE5?logo=kubernetes)](https://kubernetes.io)
[![Python](https://img.shields.io/badge/Python-3.11-green?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> A production-grade CI/CD pipeline that automatically tests, builds, and deploys
> a Python FastAPI app to Kubernetes on every git push — with live monitoring.

---

## Architecture

```
GitHub Push
    ↓
┌─────────────────────────────────────────────────────────┐
│        GitHub Actions Pipeline                          │
│  ┌──────────┐  ┌───────┐  ┌──────┐  ┌────────────┐    │
│  │  TEST    │→ │ BUILD │→ │ PUSH │→ │  DEPLOY   │    │
│  │ pytest   │  │Docker │  │Hub   │  │ kubectl   │    │
│  └──────────┘  └───────┘  └──────┘  └────────────┘    │
└─────────────────────────────────────────────────────────┘
    ↓
┌──────────────────────────┐
│    Minikube K8s          │
│    2x Replicas           │
│    PDeploy            │
└──────────────────────────┘
    ↓        ↓
┌──────────────────┐  ┌──────────────────┐
│  Prometheus      │  │    Grafana       │
│  (Metrics)       │  │   (Dashboard)    │
└──────────────────┘  └──────────────────┘
```

## Features

- **Automated CI/CD**: 4-stage pipeline runs on every git push
- **Zero-downtime deploys**: Kubernetes rolling updates with instant rollback
- **Containerized**: Docker multi-stage build for minimal image size
- **Self-healing**: K8s liveness probes auto-restart failed pods
- **Live monitoring**: Prometheus + Grafana dashboard with alerting
- **Fully free**: No cloud costs — runs entirely on local Minikube

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python FastAPI | REST API web application |
| Docker | Container build & packaging |
| Docker Hub | Container image registry |
| Minikube | Local Kubernetes cluster |
| GitHub Actions | CI/CD pipeline automation |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/pdeploy.git && cd pdeploy

# 2. Start Minikube
minikube start --driver=docker --cpus=2 --memory=4096

# 3. Deploy to Kubernetes
kubectl apply -f k8s/

# 4. Get the app URL
minikube service pdeploy-service --url

# 5. Open in browser and test
# Navigate to: [URL from step 4]/health
```

## How the Pipeline Works

1. **Push** code to the `main` branch on GitHub
2. **Test** job runs `pytest` — pipeline stops if any test fails
3. **Build** job creates a Docker image tagged with git commit SHA
4. **Push** job uploads image to Docker Hub (`:latest` and `:[SHA]` tags)
5. **Deploy** job runs `kubectl set image` to update the K8s deployment
6. Kubernetes performs a **rolling update** — zero downtime

## Monitoring

Access the Grafana dashboard:

```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open: http://localhost:3000 (admin / pdeploy-admin)
```

Dashboard panels: HTTP request rate, P95 latency, pod CPU, pod memory.

## Project Structure

```
pdeploy/
├── app/                          # FastAPI application
│   ├── main.py                   # Main application code
│   ├── requirements.txt           # Python dependencies
│   └── tests/
│       └── test_main.py           # Pytest test suite
├── k8s/                          # Kubernetes manifests
│   ├── deployment.yaml            # Pod deployment with 2 replicas
│   ├── service.yaml               # NodePort service
│   ├── ingress.yaml               # Ingress configuration
│   └── servicemonitor.yaml        # Prometheus scrape config
├── monitoring/                   # Prometheus + Grafana config
│   └── prometheus-values.yaml    # Helm values
├── .github/workflows/            # CI/CD pipeline
│   └── deploy.yml                # 4-job GitHub Actions workflow
├── Dockerfile                    # Multi-stage Docker build
├── docker-compose.yml            # Local development setup
├── .dockerignore                 # Docker build exclusions
└── README.md                     # This file
```

## Prerequisites

- Python 3.10+
- Docker Desktop (with Docker Engine running)
- Minikube 1.32+
- kubectl 1.29+
- Helm 3.x
- Git
- GitHub account with a public repository

## Installation Guide

See [SETUP.md](SETUP.md) for detailed step-by-step installation instructions.

## API Endpoints

- **GET /health** - Health check endpoint (used by Kubernetes probes)
- **GET /info** - Application metadata
- **POST /predict** - Mock NLP sentiment analysis
- **GET /metrics** - Prometheus metrics endpoint

## Kubernetes Commands Reference

```bash
# Watch deployment rollout
kubectl rollout status deployment/pdeploy

# View deployment history
kubectl rollout history deployment/pdeploy

# Rollback to previous version
kubectl rollout undo deployment/pdeploy

# Scale replicas
kubectl scale deployment pdeploy --replicas=4

# View pod logs
kubectl logs POD_NAME -f

# Shell into pod
kubectl exec -it POD_NAME -- /bin/bash

# Port-forward to pod
kubectl port-forward POD_NAME 8000:8000
```

## Troubleshooting

### ImagePullBackOff
Kubernetes cannot download the image from Docker Hub
- Verify image exists on Docker Hub and is public
- Check spelling of username in `k8s/deployment.yaml`

### CrashLoopBackOff
Pod starts then immediately crashes
- Run: `kubectl logs POD_NAME --previous`
- Usually caused by missing Python dependencies
- Test locally: `docker run YOUR_IMAGE`

### Connection refused
Service not exposed correctly
- Run: `minikube service pdeploy-service --url`
- Verify pods are Running: `kubectl get pods`

## Author

**Pravinkumar Choudhary**
- GitHub: [@speedprav](https://github.com/speedprav)
- LinkedIn: [pravin-choudhary](https://www.linkedin.com/in/pravin-choudhary-427ab9233)
- BCA · Cloud Computing · Parul University

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
