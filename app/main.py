from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
def home():
    """Render-friendly landing page for the portfolio API."""
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>AutoDeploy API</title>
        <style>
          :root {
            color-scheme: light;
            --bg: #f6f7f9;
            --panel: #ffffff;
            --ink: #17202a;
            --muted: #64748b;
            --line: #d8dee8;
            --blue: #1455d9;
            --green: #16845b;
            --amber: #a16207;
          }

          * { box-sizing: border-box; }

          body {
            margin: 0;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--ink);
            background:
              linear-gradient(180deg, #eef3ff 0, rgba(238, 243, 255, 0) 360px),
              var(--bg);
            line-height: 1.5;
          }

          main {
            width: min(1120px, calc(100% - 32px));
            margin: 0 auto;
            padding: 34px 0 42px;
          }

          .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 42px;
          }

          .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 800;
            font-size: 1.05rem;
          }

          .mark {
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            border-radius: 8px;
            color: #fff;
            background: #111827;
            font-weight: 900;
          }

          .status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border: 1px solid rgba(22, 132, 91, 0.25);
            border-radius: 999px;
            color: var(--green);
            background: rgba(22, 132, 91, 0.08);
            font-size: 0.92rem;
            font-weight: 700;
          }

          .status::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
          }

          .hero {
            display: grid;
            grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
            gap: 34px;
            align-items: center;
            margin-bottom: 34px;
          }

          h1 {
            margin: 0;
            max-width: 760px;
            font-size: clamp(2.35rem, 6vw, 4.7rem);
            line-height: 0.98;
            letter-spacing: 0;
          }

          .lead {
            max-width: 660px;
            margin: 22px 0 0;
            color: #475569;
            font-size: 1.1rem;
          }

          .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 28px;
          }

          .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 44px;
            padding: 0 16px;
            border-radius: 8px;
            border: 1px solid var(--line);
            color: var(--ink);
            background: #fff;
            text-decoration: none;
            font-weight: 800;
          }

          .button.primary {
            border-color: var(--blue);
            color: #fff;
            background: var(--blue);
          }

          .pipeline {
            padding: 22px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
          }

          .pipeline-title {
            margin: 0 0 18px;
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 900;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }

          .stage {
            display: grid;
            grid-template-columns: 34px 1fr auto;
            gap: 12px;
            align-items: center;
            padding: 13px 0;
            border-top: 1px solid #eef1f5;
          }

          .stage:first-of-type { border-top: 0; }

          .stage-number {
            display: grid;
            place-items: center;
            width: 34px;
            height: 34px;
            border-radius: 8px;
            background: #eef3ff;
            color: var(--blue);
            font-weight: 900;
          }

          .stage strong { display: block; }
          .stage span { color: var(--muted); font-size: 0.92rem; }

          .tag {
            padding: 5px 9px;
            border-radius: 999px;
            color: var(--green);
            background: rgba(22, 132, 91, 0.09);
            font-size: 0.78rem;
            font-weight: 800;
            white-space: nowrap;
          }

          .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
          }

          .tile {
            min-height: 150px;
            padding: 20px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
          }

          .tile h2 {
            margin: 0 0 8px;
            font-size: 1rem;
          }

          .tile p {
            margin: 0 0 16px;
            color: var(--muted);
            font-size: 0.94rem;
          }

          .tile a {
            color: var(--blue);
            font-weight: 850;
            text-decoration: none;
          }

          .stack {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 18px;
          }

          .stack span {
            padding: 7px 10px;
            border: 1px solid #e4e8ef;
            border-radius: 999px;
            color: #334155;
            background: #f9fafb;
            font-size: 0.85rem;
            font-weight: 700;
          }

          @media (max-width: 860px) {
            .hero { grid-template-columns: 1fr; }
            .grid { grid-template-columns: 1fr; }
          }

          @media (max-width: 520px) {
            main { width: min(100% - 24px, 1120px); padding-top: 20px; }
            .topbar { align-items: flex-start; flex-direction: column; margin-bottom: 28px; }
            .pipeline { padding: 16px; }
            .stage { grid-template-columns: 34px 1fr; }
            .tag { grid-column: 2; width: fit-content; }
            .button { width: 100%; }
          }
        </style>
      </head>
      <body>
        <main>
          <header class="topbar">
            <div class="brand">
              <div class="mark">AD</div>
              <span>AutoDeploy</span>
            </div>
            <div class="status">Live on Render</div>
          </header>

          <section class="hero">
            <div>
              <h1>Production CI/CD API, running live.</h1>
              <p class="lead">
                A FastAPI service packaged with Docker and shaped for deployment, health checks,
                monitoring, and repeatable delivery workflows.
              </p>
              <div class="actions">
                <a class="button primary" href="/docs">Open API Docs</a>
                <a class="button" href="/health">Check Health</a>
                <a class="button" href="/info">Project Info</a>
              </div>
              <div class="stack" aria-label="Technology stack">
                <span>FastAPI</span>
                <span>Docker</span>
                <span>Kubernetes</span>
                <span>GitHub Actions</span>
                <span>Prometheus</span>
                <span>Grafana</span>
              </div>
            </div>

            <aside class="pipeline" aria-label="Deployment pipeline">
              <p class="pipeline-title">Delivery Flow</p>
              <div class="stage">
                <div class="stage-number">1</div>
                <div><strong>Test</strong><span>Pytest validates API behavior</span></div>
                <div class="tag">Ready</div>
              </div>
              <div class="stage">
                <div class="stage-number">2</div>
                <div><strong>Build</strong><span>Docker image packages the service</span></div>
                <div class="tag">Ready</div>
              </div>
              <div class="stage">
                <div class="stage-number">3</div>
                <div><strong>Deploy</strong><span>Render runs the production container</span></div>
                <div class="tag">Live</div>
              </div>
              <div class="stage">
                <div class="stage-number">4</div>
                <div><strong>Observe</strong><span>Metrics endpoint supports monitoring</span></div>
                <div class="tag">Active</div>
              </div>
            </aside>
          </section>

          <section class="grid" aria-label="API shortcuts">
            <article class="tile">
              <h2>Health</h2>
              <p>Simple uptime signal for deployment probes and smoke checks.</p>
              <a href="/health">View /health</a>
            </article>
            <article class="tile">
              <h2>API Docs</h2>
              <p>Interactive Swagger documentation generated from FastAPI routes.</p>
              <a href="/docs">View /docs</a>
            </article>
            <article class="tile">
              <h2>Prediction Demo</h2>
              <p>Mock sentiment endpoint for demonstrating request validation and responses.</p>
              <a href="/docs#/default/predict_predict_post">Try /predict</a>
            </article>
          </section>
        </main>
      </body>
    </html>
    """

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
