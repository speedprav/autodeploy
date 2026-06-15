# Troubleshooting Guide

Common issues and solutions for PDeploy.

---

## Application Issues

### API Not Responding

**Symptom:** `curl: (7) Failed to connect to localhost:8000: Connection refused`

**Solutions:**

1. Check if server is running
   ```bash
   ps aux | grep uvicorn
   ```

2. Start the server
   ```bash
   cd app
   uvicorn main:app --reload --port 8000
   ```

3. Check port is available
   ```bash
   # macOS/Linux
   lsof -i :8000
   
   # Windows
   netstat -ano | findstr :8000
   ```

4. Kill process using port
   ```bash
   # macOS/Linux
   kill -9 <PID>
   
   # Windows
   taskkill /PID <PID> /F
   ```

---

### ModuleNotFoundError

**Symptom:** `ModuleNotFoundError: No module named 'fastapi'`

**Solutions:**

1. Verify virtual environment is activated
   ```bash
   # Should show (.venv) prefix
   python --version
   ```

2. Activate virtual environment
   ```bash
   # macOS/Linux
   source .venv/bin/activate
   
   # Windows
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies
   ```bash
   pip install -r app/requirements.txt
   ```

4. Verify installation
   ```bash
   pip list | grep fastapi
   ```

---

### Import Errors

**Symptom:** `ImportError: cannot import name 'X' from 'Y'`

**Solutions:**

1. Check Python version (need 3.11+)
   ```bash
   python --version
   ```

2. Reinstall dependencies
   ```bash
   pip uninstall -r app/requirements.txt -y
   pip install -r app/requirements.txt
   ```

3. Check for typos in imports
   ```python
   # ✓ Correct
   from fastapi import FastAPI
   
   # ✗ Wrong
   from fastapi import fastapi
   ```

---

### Tests Failing

**Symptom:** `FAILED tests/test_main.py::test_something`

**Solutions:**

1. Run tests with verbose output
   ```bash
   pytest tests/ -v
   ```

2. Run specific failing test
   ```bash
   pytest tests/test_main.py::test_name -v
   ```

3. Check test dependencies
   ```bash
   pip install pytest httpx
   ```

4. Run test in isolated mode
   ```bash
   pytest tests/test_main.py --tb=short
   ```

5. Clear pytest cache
   ```bash
   rm -rf .pytest_cache
   pytest tests/
   ```

---

### Port 8000 Already in Use

**Symptom:** `Address already in use`

**Solutions:**

1. Use different port
   ```bash
   uvicorn main:app --port 8001
   ```

2. Kill existing process
   ```bash
   # macOS/Linux
   lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
   
   # Windows PowerShell
   Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
   ```

3. Restart computer (last resort)

---

### JSON Decode Error

**Symptom:** `json.decoder.JSONDecodeError`

**Solutions:**

1. Verify JSON format
   ```bash
   # ✓ Valid
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"text":"hello"}'
   
   # ✗ Invalid (single quotes in JSON)
   -d "{'text':'hello'}"
   ```

2. Use JSON formatter to validate
   ```bash
   echo '{"text":"hello"}' | python -m json.tool
   ```

---

### Empty Text Error

**Symptom:** `"detail": "Text field cannot be empty"`

**Solutions:**

1. Check text field is not empty
   ```bash
   # ✓ Correct
   curl -X POST http://localhost:8000/predict \
     -d '{"text":"non-empty text"}'
   
   # ✗ Empty
   curl -X POST http://localhost:8000/predict \
     -d '{"text":""}'
   ```

2. Strip whitespace
   ```python
   request.text.strip()  # Removes leading/trailing spaces
   ```

---

## Docker Issues

### Docker Image Build Fails

**Symptom:** `ERROR [stage 0 1/5] FROM python:3.11-slim`

**Solutions:**

1. Check Docker daemon running
   ```bash
   docker ps
   ```

2. Start Docker Desktop (or daemon)

3. Pull base image
   ```bash
   docker pull python:3.11-slim
   ```

4. Check internet connection

---

### Docker Container Crashes

**Symptom:** `docker run ... Exit Code 1`

**Solutions:**

1. Check logs
   ```bash
   docker run pdeploy:latest
   # View error output
   ```

2. Run interactively
   ```bash
   docker run -it pdeploy:latest bash
   python app/main.py
   ```

3. Verify Dockerfile
   ```bash
   docker build --no-cache -t pdeploy .
   ```

---

### Port Binding Error

**Symptom:** `bind: address already in use`

**Solutions:**

1. Use different port
   ```bash
   docker run -p 8001:8000 pdeploy:latest
   ```

2. Remove stopped containers
   ```bash
   docker container prune
   ```

3. Kill existing container
   ```bash
   docker stop <container_id>
   docker rm <container_id>
   ```

---

### Permission Denied

**Symptom:** `permission denied while trying to connect to Docker daemon`

**Solutions:**

1. Add user to docker group (Linux)
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. Run with sudo
   ```bash
   sudo docker build -t pdeploy .
   ```

---

## Kubernetes Issues

### Minikube Won't Start

**Symptom:** `Failed to start cluster`

**Solutions:**

1. Check virtualization enabled (BIOS)

2. Try different driver
   ```bash
   minikube start --driver=docker
   minikube start --driver=virtualbox
   minikube start --driver=hyperv  # Windows
   ```

3. Reset Minikube
   ```bash
   minikube delete
   minikube start
   ```

4. Check resources
   ```bash
   minikube status
   minikube top nodes
   ```

---

### Pods Stuck in Pending

**Symptom:** `STATUS: Pending`

**Solutions:**

1. Describe pod for details
   ```bash
   kubectl describe pod <pod-name>
   ```

2. Check node capacity
   ```bash
   kubectl describe nodes
   ```

3. Check resource requests
   ```bash
   kubectl get pod <pod-name> -o yaml | grep -A 5 resources
   ```

4. Reduce resource requests
   ```yaml
   resources:
     requests:
       memory: "64Mi"      # Reduced from 128Mi
       cpu: "50m"         # Reduced from 100m
   ```

---

### Pods Stuck in CrashLoopBackOff

**Symptom:** `STATUS: CrashLoopBackOff`

**Solutions:**

1. Check crash logs
   ```bash
   kubectl logs <pod-name>
   kubectl logs <pod-name> --previous
   ```

2. Debug with shell
   ```bash
   kubectl exec -it <pod-name> -- /bin/bash
   ```

3. Check image exists
   ```bash
   docker images
   kubectl describe pod <pod-name> | grep Image
   ```

4. Increase startup time
   ```yaml
   livenessProbe:
     initialDelaySeconds: 30  # Increased from 10
   ```

---

### ImagePullBackOff

**Symptom:** `STATUS: ImagePullBackOff`

**Solutions:**

1. Check image name
   ```bash
   kubectl describe pod <pod-name> | grep Image
   ```

2. Verify image exists locally
   ```bash
   docker images | grep pdeploy
   ```

3. Push to Docker Hub
   ```bash
   docker tag pdeploy:latest username/pdeploy:latest
   docker push username/pdeploy:latest
   ```

4. Create image pull secret
   ```bash
   kubectl create secret docker-registry regcred \
     --docker-server=docker.io \
     --docker-username=YOUR_USERNAME \
     --docker-password=YOUR_TOKEN
   ```

---

### Can't Access Service

**Symptom:** `curl: (7) Failed to connect`

**Solutions:**

1. Check service running
   ```bash
   kubectl get svc
   kubectl describe svc pdeploy-service
   ```

2. Get external IP
   ```bash
   kubectl get svc
   ```

3. Port forward for testing
   ```bash
   kubectl port-forward svc/pdeploy-service 8000:80
   curl http://localhost:8000/health
   ```

4. Check service selector matches pod labels
   ```bash
   kubectl get pods --show-labels
   kubectl get svc pdeploy-service -o yaml | grep selector
   ```

---

### kubectl Commands Not Found

**Symptom:** `kubectl: command not found`

**Solutions:**

1. Install kubectl
   ```bash
   # macOS
   brew install kubectl
   
   # Windows
   choco install kubernetes-cli
   
   # Or download: https://kubernetes.io/docs/tasks/tools/
   ```

2. Verify installation
   ```bash
   kubectl version --client
   ```

---

## Render Deployment Issues

### Deployment Stuck Building

**Symptom:** "Application loading" for > 10 minutes

**Solutions:**

1. Check Render dashboard logs
   - Go to: https://dashboard.render.com
   - Select service → Logs tab
   - Look for error messages

2. Common issues:
   - Missing dependencies (pip install failure)
   - Long build time on free tier
   - Network issues

3. Redeploy manually
   - Dashboard → Manual Deploy

4. Check start command
   ```bash
   # Should be exactly:
   cd app && uvicorn main:app --host 0.0.0.0 --port 8000
   ```

---

### Service Returns 503

**Symptom:** "Service Unavailable"

**Solutions:**

1. App might still be starting (free tier is slow)
   - Wait 1-2 minutes and retry

2. Check logs in Render dashboard

3. Verify health endpoint works locally
   ```bash
   curl http://localhost:8000/health
   ```

4. Check environment variables
   - Dashboard → Environment
   - Ensure PORT is set to 8000

---

### Deployment Rejected

**Symptom:** "Failed to decode Dockerfile"

**Solutions:**

1. Ensure Dockerfile exists
   ```bash
   git ls-files | grep Dockerfile
   ```

2. Add to git
   ```bash
   git add -f Dockerfile
   git commit -m "Add Dockerfile"
   git push origin main
   ```

3. Check Render build settings
   - Dashboard → Build & Deploy
   - Build command: `docker build`
   - Or specify custom Dockerfile path

---

## GitHub Actions Issues

### Workflow Not Triggering

**Symptom:** Push to main but no action runs

**Solutions:**

1. Check workflow file syntax
   ```bash
   # Validate YAML
   python -m yaml .github/workflows/deploy.yml
   ```

2. Verify trigger event
   ```yaml
   on:
     push:
       branches: [ main ]  # Must match branch name
   ```

3. Check branch protection rules (if enabled)
   - Settings → Branches → Branch protection rules

4. Manually trigger
   ```bash
   git push origin main --force
   ```

---

### Tests Failing in GitHub Actions

**Symptom:** Green locally, red on GitHub

**Solutions:**

1. Check Python version matches
   ```yaml
   - uses: actions/setup-python@v4
     with:
       python-version: '3.11'  # Verify version
   ```

2. Install test dependencies
   ```yaml
   - run: pip install -r app/requirements.txt pytest
   ```

3. Run tests with same command
   ```yaml
   - run: pytest tests/ -v
   ```

4. Check working directory
   ```yaml
   - run: cd app && pytest tests/ -v
   ```

---

### Deploy Job Failing

**Symptom:** "Deploy job does not have a runner"

**Solutions:**

1. Ensure self-hosted runner registered
   - Repository → Settings → Actions → Runners
   - Runner must be online

2. For Render/cloud deploy, remove self-hosted requirement
   ```yaml
   runs-on: ubuntu-latest  # Use cloud runner
   ```

3. Verify runner labels match job
   ```yaml
   runs-on: self-hosted  # Must have this runner configured
   ```

---

## Development Environment Issues

### Virtual Environment Won't Activate

**Symptom:** `(.venv) prefix not appearing`

**Solutions:**

1. Check script exists
   ```bash
   ls .venv/bin/activate  # macOS/Linux
   ls .venv\Scripts\Activate.ps1  # Windows
   ```

2. Recreate venv
   ```bash
   rm -rf .venv
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Use python -m instead
   ```bash
   python -m pip install -r app/requirements.txt
   ```

---

### Permission Denied (Linux/macOS)

**Symptom:** `Permission denied`

**Solutions:**

1. Make script executable
   ```bash
   chmod +x .venv/bin/activate
   ```

2. Use bash explicitly
   ```bash
   bash .venv/bin/activate
   ```

3. Use python -m
   ```bash
   python -m pip install -r app/requirements.txt
   ```

---

## Performance Issues

### API Responding Slowly

**Symptom:** Requests taking > 100ms

**Solutions:**

1. Profile the code
   ```bash
   pip install py-spy
   py-spy record -o profile.svg -- uvicorn main:app
   ```

2. Check resource usage
   ```bash
   top  # macOS/Linux
   tasklist  # Windows
   ```

3. Reduce sentiment keywords
   - Smaller sets = faster matching

4. Add caching
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def get_sentiment(text):
       pass
   ```

---

### High Memory Usage

**Symptom:** Memory grows over time

**Solutions:**

1. Check for memory leaks
   ```bash
   pip install memory_profiler
   python -m memory_profiler app/main.py
   ```

2. Limit container memory
   ```bash
   docker run -m 256m pdeploy:latest
   ```

3. Restart periodically (if needed)
   ```bash
   # In Kubernetes:
   kubectl set env deployment/pdeploy RESTART_COUNTER=<random>
   ```

---

## Network Issues

### CORS Errors

**Symptom:** `No 'Access-Control-Allow-Origin' header`

**Solutions:**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Timeout Errors

**Symptom:** `timeout: timed out after 30 seconds`

**Solutions:**

1. Increase timeout in client code
2. Optimize slow queries
3. Increase deployment timeout
   ```bash
   kubectl rollout status deployment/pdeploy --timeout=5m
   ```

---

## Getting Help

If issue persists:

1. Check logs
   ```bash
   # Local
   tail -f app.log
   
   # K8s
   kubectl logs deployment/pdeploy
   
   # Docker
   docker logs <container-id>
   ```

2. Search GitHub issues: https://github.com/speedprav/pdeploy/issues

3. Create new issue with:
   - Error message
   - Steps to reproduce
   - Environment (OS, Python version, etc.)
   - Logs/stack traces

4. Ask for help
   - GitHub discussions (if available)
   - Stack Overflow tag: `fastapi` `kubernetes`

---

Good luck! 🎉
