# PDeploy Documentation Index

Complete documentation for the PDeploy CI/CD pipeline project.

---

## 📚 Documentation Overview

| Document | Purpose | Audience |
|----------|---------|----------|
| [**API.md**](API.md) | REST API endpoints & usage | Developers, API users |
| [**SETUP.md**](SETUP.md) | Installation & local development | New contributors |
| [**ARCHITECTURE.md**](ARCHITECTURE.md) | System design & components | Architects, DevOps engineers |
| [**DEPLOYMENT.md**](DEPLOYMENT.md) | Production deployment options | DevOps, SREs |
| [**CONTRIBUTING.md**](CONTRIBUTING.md) | How to contribute code | Contributors |
| [**TROUBLESHOOTING.md**](TROUBLESHOOTING.md) | Common issues & solutions | Everyone |

---

## 🚀 Quick Start

### I just cloned the repo, what do I do?

1. Read: [SETUP.md](SETUP.md)
2. Follow steps to install and run locally
3. Access API docs: http://localhost:8000/docs

### I want to deploy to production

1. Read: [DEPLOYMENT.md](DEPLOYMENT.md)
2. Choose deployment platform (Render, DigitalOcean, AWS, etc.)
3. Follow step-by-step guide

### I want to use the API

1. Read: [API.md](API.md)
2. Find your endpoint
3. Use provided examples (cURL, Python, JavaScript)

### I want to contribute code

1. Read: [CONTRIBUTING.md](CONTRIBUTING.md)
2. Setup development environment
3. Make changes, run tests
4. Submit pull request

### Something isn't working

1. Read: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Find your issue
3. Follow solution steps
4. If still stuck, create GitHub issue

---

## 📖 Document Descriptions

### [API.md](API.md)
**Complete REST API documentation**

Covers:
- Endpoint specifications
- Request/response formats
- Error handling
- Code examples (Python, JavaScript, cURL)
- Metrics endpoint
- Performance metrics
- Integration examples
- Troubleshooting for API issues

**Best for:** Using the API, understanding endpoints, writing integrations

---

### [SETUP.md](SETUP.md)
**Installation and development setup**

Covers:
- Prerequisites
- Local development setup (Python venv)
- Docker setup
- Kubernetes setup (Minikube)
- Prometheus & Grafana setup
- Project structure
- Environment variables
- Troubleshooting setup issues

**Best for:** Getting started, setting up locally, running tests

---

### [ARCHITECTURE.md](ARCHITECTURE.md)
**System design and components**

Covers:
- Complete architecture diagram
- CI/CD pipeline flow
- Component details (FastAPI, Docker, K8s, GitHub Actions)
- Data flow
- Scalability considerations
- Security
- Performance characteristics
- Technology stack rationale
- Limitations and future improvements

**Best for:** Understanding how it all fits together, architecture decisions, system design

---

### [DEPLOYMENT.md](DEPLOYMENT.md)
**Production deployment guide**

Covers:
- Quick deploy to Render (already deployed ✓)
- Kubernetes deployment (DigitalOcean, GCP, AWS)
- Advanced deployments (Helm, GitOps, ArgoCD)
- Monitoring and alerting
- SSL/TLS certificates
- Auto-scaling
- Backup & restore
- Troubleshooting deployments
- Cost optimization

**Best for:** Deploying to production, choosing platforms, setting up monitoring

---

### [CONTRIBUTING.md](CONTRIBUTING.md)
**Contribution guidelines**

Covers:
- Code of conduct
- Getting started (fork, branch, setup)
- Coding standards (PEP 8, type hints)
- Testing requirements
- Documentation requirements
- Docker & Kubernetes changes
- GitHub Actions updates
- Review checklist
- Release process
- Recognition

**Best for:** Contributing code, understanding project standards, making PRs

---

### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
**Common issues and solutions**

Covers:
- Application issues (import errors, port conflicts)
- Docker issues (build failures, crashes)
- Kubernetes issues (pod states, service access)
- Render deployment issues
- GitHub Actions issues
- Development environment issues
- Performance and network issues
- How to get help

**Best for:** Fixing problems, debugging, resolving errors

---

## 🗺️ Learning Paths

### Path 1: User (Just want to use the API)
1. Start: [API.md](API.md)
2. Try: http://localhost:8000/docs (local) or https://pdeploy-w7mg.onrender.com/docs (live)
3. Reference: Code examples in [API.md](API.md)

### Path 2: Developer (Setup locally)
1. Start: [SETUP.md](SETUP.md)
2. Follow: Development environment setup
3. Reference: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if issues
4. Explore: [API.md](API.md) to understand endpoints

### Path 3: DevOps Engineer
1. Start: [ARCHITECTURE.md](ARCHITECTURE.md) - understand design
2. Follow: [DEPLOYMENT.md](DEPLOYMENT.md) - deploy to production
3. Reference: [ARCHITECTURE.md](ARCHITECTURE.md) - scaling, monitoring
4. Troubleshoot: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Path 4: Contributor
1. Start: [CONTRIBUTING.md](CONTRIBUTING.md)
2. Setup: [SETUP.md](SETUP.md) - development environment
3. Understand: [ARCHITECTURE.md](ARCHITECTURE.md) - how it works
4. Reference: [API.md](API.md), [CONTRIBUTING.md](CONTRIBUTING.md)

### Path 5: Architect/Decision Maker
1. Start: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Review: [DEPLOYMENT.md](DEPLOYMENT.md) - hosting options
3. Reference: [API.md](API.md) - capabilities

---

## 🔍 Find Info By Topic

### I want to know about...

**Endpoints**
- See: [API.md](API.md) - Endpoints section

**Installation**
- See: [SETUP.md](SETUP.md) - Local Development Setup

**Docker**
- See: [SETUP.md](SETUP.md) - Docker Setup
- Advanced: [DEPLOYMENT.md](DEPLOYMENT.md) - Docker Hub

**Kubernetes**
- See: [SETUP.md](SETUP.md) - Kubernetes Setup
- Advanced: [DEPLOYMENT.md](DEPLOYMENT.md) - Cloud Kubernetes

**Testing**
- See: [SETUP.md](SETUP.md) - Run Tests
- Details: [CONTRIBUTING.md](CONTRIBUTING.md) - Testing Requirements

**Monitoring**
- See: [SETUP.md](SETUP.md) - Prometheus & Grafana Setup
- Advanced: [DEPLOYMENT.md](DEPLOYMENT.md) - Production Monitoring

**Performance**
- See: [ARCHITECTURE.md](ARCHITECTURE.md) - Performance Characteristics
- Debug: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Performance Issues

**Deployment**
- Quick: [DEPLOYMENT.md](DEPLOYMENT.md) - Quick Deploy (Render)
- Production: [DEPLOYMENT.md](DEPLOYMENT.md) - Cloud Kubernetes

**Contributing**
- See: [CONTRIBUTING.md](CONTRIBUTING.md) - All sections

**Problems**
- See: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Architecture**
- See: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 📚 Related Files

In the main project directory:

| File | Purpose |
|------|---------|
| [README.md](../README.md) | Project overview |
| [Dockerfile](../Dockerfile) | Container image definition |
| [docker-compose.yml](../docker-compose.yml) | Local dev environment |
| [.github/workflows/deploy.yml](../.github/workflows/deploy.yml) | CI/CD pipeline |
| [k8s/](../k8s/) | Kubernetes manifests |
| [app/main.py](../app/main.py) | Application code |
| [app/requirements.txt](../app/requirements.txt) | Python dependencies |
| [app/tests/](../app/tests/) | Test suite |

---

## 🎯 Common Tasks

### Setup and Run Locally
```bash
# Follow these sections in order:
# 1. SETUP.md - Local Development Setup
# 2. SETUP.md - Run Tests
# 3. SETUP.md - Start the Development Server
```

### Deploy to Production
```bash
# For Render (easiest):
# Follow: DEPLOYMENT.md - Quick Deploy (Render.com)

# For Kubernetes:
# Follow: DEPLOYMENT.md - Cloud Kubernetes
```

### Debug an Issue
```bash
# Check TROUBLESHOOTING.md for your issue
# Common categories:
# - Application Issues
# - Docker Issues
# - Kubernetes Issues
# - Render Deployment Issues
```

### Contribute Code
```bash
# Follow sections in CONTRIBUTING.md:
# 1. Getting Started
# 2. Coding Standards
# 3. Testing Requirements
# 4. Review Checklist
```

### Use the API
```bash
# Go to API.md and find your endpoint:
# - /health (Health Check)
# - /info (Project Info)
# - /predict (Sentiment Analysis)
```

---

## 🤝 Support

### Getting Help

1. **Search Documentation**
   - Use browser find (Ctrl+F) to search within docs

2. **GitHub Issues**
   - https://github.com/speedprav/pdeploy/issues
   - Search existing issues first

3. **Troubleshooting**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - Common solutions for known issues

4. **API Testing**
   - http://localhost:8000/docs (local)
   - https://pdeploy-w7mg.onrender.com/docs (live)
   - Interactive Swagger UI

---

## 📊 Documentation Statistics

| Document | Lines | Topics | Examples |
|----------|-------|--------|----------|
| API.md | 500+ | 15 | 20+ |
| SETUP.md | 400+ | 12 | 25+ |
| ARCHITECTURE.md | 450+ | 16 | Diagrams |
| DEPLOYMENT.md | 550+ | 18 | 30+ |
| CONTRIBUTING.md | 400+ | 14 | 15+ |
| TROUBLESHOOTING.md | 550+ | 40+ | 50+ |

**Total:** 2,850+ lines of documentation

---

## 🎓 Learning Resources

### External Links

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/)
- [Docker Guide](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Prometheus Docs](https://prometheus.io/docs/)

### Video Resources

- FastAPI: https://www.youtube.com/results?search_query=fastapi+tutorial
- Kubernetes: https://www.youtube.com/results?search_query=kubernetes+tutorial
- Docker: https://www.youtube.com/results?search_query=docker+tutorial
- CI/CD: https://www.youtube.com/results?search_query=github+actions+tutorial

---

## ✅ Checklist

### Before Deploying
- [ ] Read [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Follow [SETUP.md](SETUP.md) - all tests passing
- [ ] Review [DEPLOYMENT.md](DEPLOYMENT.md)
- [ ] Choose deployment platform
- [ ] Follow platform-specific guide

### Before Contributing
- [ ] Read [CONTRIBUTING.md](CONTRIBUTING.md)
- [ ] Follow [SETUP.md](SETUP.md)
- [ ] Understand [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Follow coding standards
- [ ] All tests pass
- [ ] Documentation updated

### Before Using API
- [ ] Read [API.md](API.md) - Endpoints section
- [ ] Review [API.md](API.md) - Code examples
- [ ] Test with interactive docs (http://localhost:8000/docs)
- [ ] Check error handling ([API.md](API.md) - Error Handling)

---

## 📝 Version & Updates

**Documentation Version:** 1.0.0  
**Last Updated:** 2026-06-15  
**Project Version:** 1.0.0

### Keeping Documentation Current

When making changes:
1. Update relevant documentation files
2. Update version numbers if breaking changes
3. Add entry to changelog (if exists)
4. Reference related files if needed

---

## 🏆 Documentation Quality

This documentation aims to be:
- ✅ **Complete** - Covers all major topics
- ✅ **Accurate** - Tested and verified
- ✅ **Clear** - Easy to understand
- ✅ **Actionable** - Contains step-by-step guides
- ✅ **Up-to-date** - Regularly maintained
- ✅ **Well-organized** - Logical structure

---

Start with the [README.md](../README.md) for overview, then pick a document based on your role or task!

Happy coding! 🚀
