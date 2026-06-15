# AutoDeploy API Documentation

## Overview

AutoDeploy is a production-grade REST API built with **FastAPI** that demonstrates a complete CI/CD pipeline with sentiment analysis capabilities. The API is instrumented with Prometheus metrics for monitoring.

**Base URL:** `http://localhost:8000` (local) or `https://autodeploy-w7mg.onrender.com` (live)

---

## Quick Start

### Run Locally
```bash
# Install dependencies
pip install -r app/requirements.txt

# Start the server (port 8000)
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## Endpoints

### 1. Health Check
**Purpose:** Kubernetes uses this to verify the app is alive and responding.

```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-06-15T07:44:25.753334",
  "service": "autodeploy-api"
}
```

**Use Cases:**
- Kubernetes liveness probes
- Load balancer health checks
- Uptime monitoring

---

### 2. Get Project Info
**Purpose:** Returns metadata about the project and tech stack.

```http
GET /info
```

**Response (200 OK):**
```json
{
  "project": "AutoDeploy",
  "version": "1.0.0",
  "author": "Pravinkumar Choudhary",
  "github": "github.com/speedprav",
  "description": "Production CI/CD pipeline demo",
  "tech_stack": [
    "FastAPI",
    "Docker",
    "Kubernetes",
    "GitHub Actions",
    "Prometheus",
    "Grafana"
  ]
}
```

**Use Cases:**
- About page
- Version verification
- Tech stack display

---

### 3. Predict Sentiment
**Purpose:** Analyzes sentiment of input text (mock ML endpoint).

```http
POST /predict
Content-Type: application/json

{
  "text": "I absolutely love this amazing project!"
}
```

**Request Body:**
```json
{
  "text": "string (required, non-empty)"
}
```

**Response (200 OK):**
```json
{
  "input_text": "I absolutely love this amazing project!",
  "word_count": 6,
  "sentiment": "positive",
  "confidence": 0.87,
  "processed_at": "2026-06-15T07:44:30.123456"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Text field cannot be empty"
}
```

**Request Examples:**

**Positive Sentiment:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Great work! This is excellent!"}'
```

**Negative Sentiment:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"This is terrible and awful!"}'
```

**Neutral Sentiment:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"The weather is cloudy today"}'
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `input_text` | string | Original input text |
| `word_count` | integer | Number of words in the text |
| `sentiment` | string | Classification: "positive", "negative", or "neutral" |
| `confidence` | float | Confidence score (0.0 - 1.0) |
| `processed_at` | string | ISO 8601 timestamp when processed |

---

## Sentiment Classification Logic

The sentiment analysis uses keyword matching:

**Positive Keywords:** good, great, excellent, happy, love, best, amazing, wonderful, fantastic

**Negative Keywords:** bad, terrible, awful, hate, worst, horrible, poor, disappointing

**Algorithm:**
1. Count positive keyword matches
2. Count negative keyword matches
3. Compare counts to determine sentiment
4. Assign confidence based on classification

---

## Error Handling

### HTTP Status Codes

| Code | Scenario |
|------|----------|
| 200 | Request successful |
| 400 | Invalid input (empty text) |
| 422 | Validation error (missing required field) |
| 500 | Internal server error |

### Error Response Format
```json
{
  "detail": "Error message describing the problem"
}
```

---

## Request/Response Examples

### Python (requests library)
```python
import requests

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Predict sentiment
data = {"text": "This is amazing!"}
response = requests.post('http://localhost:8000/predict', json=data)
result = response.json()
print(f"Sentiment: {result['sentiment']} ({result['confidence']*100:.0f}% confident)")
```

### JavaScript (fetch API)
```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(res => res.json())
  .then(data => console.log(data));

// Predict sentiment
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'This is amazing!' })
})
.then(res => res.json())
.then(data => console.log(`${data.sentiment}: ${data.confidence * 100}%`));
```

### cURL
```bash
# Health check
curl http://localhost:8000/health

# Predict sentiment
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"I love this!"}'

# Get project info
curl http://localhost:8000/info
```

---

## Metrics Endpoint

The API exposes Prometheus metrics for monitoring:

```http
GET /metrics
```

**Metrics Collected:**
- `http_requests_total` — Total HTTP requests
- `http_request_duration_seconds` — Request latency
- `http_requests_in_progress` — Concurrent requests
- `http_exceptions_total` — Exception count by type

**Example Usage:**
```bash
# View metrics
curl http://localhost:8000/metrics

# Scrape with Prometheus
curl http://localhost:8000/metrics | grep http_requests_total
```

---

## Rate Limiting & Throttling

Currently **no rate limiting** is enforced. In production, consider adding:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("100/minute")
def predict(request: PredictRequest):
    # ...
```

---

## CORS Configuration

The API allows requests from all origins. For production, restrict CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance

**Response Times (typical):**
- Health check: < 1ms
- Info endpoint: < 1ms  
- Predict endpoint: 5-10ms

**Throughput:**
- ~1000 requests/second on standard hardware

---

## Live Deployment

**Public API:** https://autodeploy-w7mg.onrender.com

```bash
# Test live API
curl https://autodeploy-w7mg.onrender.com/health
curl https://autodeploy-w7mg.onrender.com/info
```

---

## Integration Examples

### JavaScript Frontend
```html
<button onclick="predictSentiment()">Analyze</button>

<script>
async function predictSentiment() {
  const text = document.getElementById('input').value;
  const response = await fetch('https://autodeploy-w7mg.onrender.com/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  const result = await response.json();
  console.log(result);
}
</script>
```

### Health Check Monitoring
```bash
#!/bin/bash
# Check if API is healthy
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
  echo "✓ API is healthy"
else
  echo "✗ API is down"
  # Send alert/restart
fi
```

---

## Troubleshooting

### API not responding
```bash
# Check if server is running
curl -v http://localhost:8000/health

# View server logs
tail -f logs/uvicorn.log
```

### Empty text error
Make sure the `text` field is not empty or whitespace:
```bash
# ✓ Correct
curl -X POST http://localhost:8000/predict \
  -d '{"text":"Hello world"}'

# ✗ Wrong (empty)
curl -X POST http://localhost:8000/predict \
  -d '{"text":""}'
```

### Validation error
Ensure JSON is valid and all required fields are included:
```bash
# ✓ Valid JSON
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"test"}'

# ✗ Invalid JSON
curl -X POST http://localhost:8000/predict \
  -d '{text:test}'
```

---

## API Changelog

### v1.0.0 (Current)
- ✅ GET /health endpoint
- ✅ GET /info endpoint
- ✅ POST /predict with sentiment analysis
- ✅ Prometheus metrics integration
- ✅ Comprehensive error handling

---

## Support

- **Issues:** https://github.com/speedprav/autodeploy/issues
- **Docs:** https://autodeploy-w7mg.onrender.com/docs
- **Author:** Pravinkumar Choudhary
