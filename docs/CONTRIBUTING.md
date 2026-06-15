# Contributing Guide

Thank you for interest in contributing to PDeploy! This document explains how to contribute code, report issues, and suggest improvements.

---

## Code of Conduct

Be respectful, inclusive, and constructive. Treat all contributors with kindness.

---

## Getting Started

### 1. Fork Repository

```bash
# On GitHub, click "Fork" button
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/pdeploy.git
cd pdeploy
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch naming:**
- `feature/add-auth` (new feature)
- `fix/broken-endpoint` (bug fix)
- `docs/api-guide` (documentation)
- `refactor/cleanup-code` (refactoring)

### 3. Setup Development Environment

```bash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r app/requirements.txt
```

### 4. Make Changes

Follow coding standards (see below) and test everything.

### 5. Write Tests

For any new feature or bug fix, add tests:

```python
# app/tests/test_main.py

def test_my_new_feature():
    response = client.get("/new-endpoint")
    assert response.status_code == 200
    assert response.json()["field"] == "expected_value"
```

### 6. Run Tests

```bash
cd app
pytest tests/ -v
```

All tests must pass ✓

### 7. Commit Changes

```bash
git add .
git commit -m "feature: add new feature description"
```

**Commit message format:**
```
type: brief description

Longer description explaining the change (optional)

- Bullet point 1
- Bullet point 2

Fixes #123
```

**Types:**
- `feature:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code restructure
- `test:` Test additions
- `chore:` Maintenance

### 8. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 9. Create Pull Request

On GitHub:
1. Click "Compare & pull request"
2. Fill PR template (if exists)
3. Link related issues
4. Request reviewers
5. Submit!

---

## Coding Standards

### Python Style Guide (PEP 8)

```python
# ✓ Good
def calculate_sentiment_score(text: str) -> float:
    """Calculate sentiment score for input text."""
    if not text:
        raise ValueError("Text cannot be empty")
    
    score = 0.0
    for word in text.split():
        score += get_word_score(word)
    
    return score / len(text.split())

# ✗ Bad
def calculate_sentiment_score(text):
    if not text: raise ValueError("Text cannot be empty")
    s = 0.0
    for w in text.split(): s += get_word_score(w)
    return s / len(text.split())
```

### Key Principles

1. **Type hints** - Always use for functions
   ```python
   def predict(request: PredictRequest) -> PredictResponse:
   ```

2. **Docstrings** - For functions and classes
   ```python
   def health_check():
       """
       Health check endpoint for Kubernetes.
       Returns: status and timestamp
       """
   ```

3. **Constants** - Use UPPER_CASE
   ```python
   MAX_TEXT_LENGTH = 1000
   DEFAULT_CONFIDENCE = 0.5
   ```

4. **Naming** - Descriptive, lowercase with underscores
   ```python
   # ✓ Good
   positive_keywords = ["good", "great"]
   
   # ✗ Bad
   pk = ["good", "great"]
   pos_kw = ["good", "great"]
   ```

5. **Line length** - Max 100 characters
   ```python
   # ✓ Good
   long_variable_name = (
       "value1" + "value2" + "value3"
   )
   
   # ✗ Bad
   long_variable_name = "value1" + "value2" + "value3" + "value4" + "value5"
   ```

### File Organization

```python
# app/main.py
# 1. Imports (stdlib, third-party, local)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

# 2. Constants
MAX_TEXT_LENGTH = 1000
POSITIVE_KEYWORDS = ["good", "great"]

# 3. Models
class PredictRequest(BaseModel):
    text: str

# 4. Main app
app = FastAPI()

# 5. Routes
@app.get("/health")
def health_check():
    pass

# 6. Utility functions (bottom)
def helper_function():
    pass
```

---

## Testing Requirements

### Coverage Minimum

- **Overall:** ≥ 80%
- **Critical paths:** 100%
- **New features:** Must include tests

### Test Structure

```python
# app/tests/test_new_feature.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestNewFeature:
    """Test new feature."""
    
    def test_success_case(self):
        """Test successful execution."""
        response = client.get("/endpoint")
        assert response.status_code == 200
    
    def test_error_case(self):
        """Test error handling."""
        response = client.get("/endpoint?invalid=true")
        assert response.status_code == 400
    
    def test_edge_case(self):
        """Test boundary condition."""
        response = client.get("/endpoint?value=''")
        assert response.status_code == 400
```

### Run Tests Locally

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_main.py::TestHealth

# Run verbose
pytest -v

# Run and stop on first failure
pytest -x
```

---

## Documentation

### Update These Files

1. **README.md** - If user-facing changes
   ```markdown
   ## New Feature Name
   
   Brief description of what it does.
   
   Usage:
   ```bash
   endpoint /new-endpoint
   ```
   ```

2. **docs/API.md** - If API changes
   ```markdown
   ### New Endpoint
   
   Description, request, response examples
   ```

3. **docs/ARCHITECTURE.md** - If system design changes

4. **Code comments** - For non-obvious logic
   ```python
   # This uses exponential backoff (not linear) to be
   # more gentle on the server during high load
   wait_time = 2 ** retry_count
   ```

---

## Docker & Kubernetes

### If Changing Dockerfile

1. Build locally:
   ```bash
   docker build -t pdeploy:test .
   docker run -p 8000:8000 pdeploy:test
   ```

2. Test container:
   ```bash
   curl http://localhost:8000/health
   ```

3. Update documentation

### If Changing K8s Manifests

1. Update locally:
   ```bash
   kubectl apply -f k8s/ --dry-run=client
   ```

2. Test deployment:
   ```bash
   minikube start
   kubectl apply -f k8s/
   kubectl get pods
   ```

3. Document changes in PR

---

## GitHub Actions Workflows

When updating `.github/workflows/deploy.yml`:

1. Test locally with [act](https://github.com/nektos/act):
   ```bash
   act -j test
   act -j build
   ```

2. Create detailed commit message explaining changes

3. Request review from maintainer

---

## Performance Considerations

For any code changes:

```python
# ✓ Efficient
positive_keywords_set = {"good", "great", "excellent"}
for word in text.split():
    if word in positive_keywords_set:  # O(1) lookup
        count += 1

# ✗ Inefficient
positive_keywords_list = ["good", "great", "excellent"]
for word in text.split():
    if word in positive_keywords_list:  # O(n) lookup
        count += 1
```

---

## Security Best Practices

- [ ] No hardcoded secrets
- [ ] Input validation (use Pydantic)
- [ ] Error messages don't leak info
- [ ] No SQL injection (we don't use SQL, but principle applies)
- [ ] Validate file uploads (if applicable)
- [ ] Rate limiting for public endpoints

---

## Issue Templates

### Bug Report

```
## Description
Clear description of the bug

## Steps to Reproduce
1. ...
2. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 20.04
- Python: 3.11
- FastAPI: 0.104.1

## Error Logs
```

### Feature Request

```
## Description
What feature would you like?

## Problem It Solves
Why is this needed?

## Proposed Solution
How should it work?

## Alternatives Considered
What else could solve this?

## Additional Context
Any other info
```

---

## Release Process

1. Update version in `app/main.py`
   ```python
   app = FastAPI(version="1.1.0")
   ```

2. Update CHANGELOG (if exists)

3. Create git tag
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

4. GitHub Actions builds & pushes image

5. Create release notes on GitHub

---

## Review Checklist

Before submitting PR, ensure:

- [ ] Tests pass: `pytest -v`
- [ ] Coverage maintained: `pytest --cov`
- [ ] Code follows PEP 8: Check with `black` or `flake8`
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] No hardcoded values
- [ ] Documentation updated
- [ ] Commit messages clear
- [ ] No merge conflicts
- [ ] PR description detailed

---

## Getting Help

- **Discussion:** GitHub Discussions (if enabled)
- **Issues:** Search existing issues first
- **Questions:** Can comment on related issues
- **Contact:** Look for MAINTAINERS.md

---

## Maintainer Notes

- PRs typically reviewed within 2-7 days
- Constructive feedback provided
- Request changes if needed
- Merge when approved & CI passes
- Thanks for contributing!

---

## Examples of Good Contributions

1. **Bug fix** with test case
2. **Performance improvement** with benchmarks
3. **New feature** with docs
4. **Test coverage** for uncovered code
5. **Documentation** improvements
6. **Code refactoring** for readability
7. **Error message** improvements
8. **Dependency** updates
9. **GitHub Actions** improvements
10. **Type hints** for untyped code

---

## Tips for Success

1. **Start small** - Fix typos or add tests first
2. **Ask questions** - Comment before starting big changes
3. **Keep focused** - One feature/fix per PR
4. **Test thoroughly** - Expect high standards
5. **Be patient** - Maintainers have other commitments
6. **Be respectful** - Treat feedback as learning opportunity
7. **Iterate** - Be willing to make changes
8. **Document** - Explain your changes clearly
9. **Reference** - Link related issues/PRs
10. **Follow up** - Check CI results and respond to comments

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (coming soon)
- Credited in release notes
- Thanked sincerely!

---

Thank you for making PDeploy better! 🎉
