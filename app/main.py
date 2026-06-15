from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import random
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize the FastAPI application
app = FastAPI(
    title="AutoDeploy API",
    description="Production CI/CD demo app for DevOps portfolio",
    version="1.0.0"
)

# Add Prometheus metrics collection
# This adds automatic HTTP metrics collection to every endpoint
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    inprogress_name="http_requests_inprogress",
    inprogress_labels=True,
)
instrumentator.instrument(app).expose(app)
# This automatically adds a GET /metrics endpoint that Prometheus scrapes
# Metrics included: request count, request duration, in-progress requests

# ■■ Data Models ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
class PredictRequest(BaseModel):
    """Request body for the /predict endpoint"""
    text: str

class PredictResponse(BaseModel):
    """Response body for the /predict endpoint"""
    input_text: str
    word_count: int
    sentiment: str
    confidence: float
    processed_at: str

# ■■ Endpoints ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

@app.get("/health")
def health_check():
    """
    Health check endpoint — Kubernetes uses this to verify the app is alive.
    Returns: status and current UTC timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "autodeploy-api"
    }

@app.get("/info")
def get_info():
    """
    Application metadata endpoint.
    Returns: project details and author information
    """
    return {
        "project": "AutoDeploy",
        "version": "1.0.0",
        "author": "Pravinkumar Choudhary",
        "github": "github.com/speedprav",
        "description": "Production CI/CD pipeline demo",
        "tech_stack": [
            "FastAPI", "Docker", "Kubernetes",
            "GitHub Actions", "Prometheus", "Grafana"
        ]
    }

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Mock NLP prediction endpoint.
    Accepts text input and returns a simple sentiment analysis result.
    In a real app, this would call an ML model.
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text field cannot be empty"
        )
    
    # Count words in the input text
    word_count = len(request.text.split())
    
    # Simple mock sentiment: positive words trigger positive sentiment
    positive_words = ["good", "great", "excellent", "happy", "love",
                      "best", "amazing", "wonderful", "fantastic"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst",
                      "horrible", "poor", "disappointing"]
    
    text_lower = request.text.lower()
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    
    if pos_count > neg_count:
        sentiment = "positive"
        confidence = round(random.uniform(0.75, 0.95), 2)
    elif neg_count > pos_count:
        sentiment = "negative"
        confidence = round(random.uniform(0.70, 0.90), 2)
    else:
        sentiment = "neutral"
        confidence = round(random.uniform(0.60, 0.80), 2)
    
    return PredictResponse(
        input_text=request.text,
        word_count=word_count,
        sentiment=sentiment,
        confidence=confidence,
        processed_at=datetime.utcnow().isoformat()
    )

# ■■ Run locally ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
