from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import random
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize the FastAPI application
app = FastAPI(
    title="PDeploy API",
    description="Production CI/CD demo app for DevOps portfolio",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
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

def wants_html(request: Request) -> bool:
    """Return polished pages in browsers while keeping JSON for API clients."""
    accept = request.headers.get("accept", "")
    return "text/html" in accept and "application/json" not in accept


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{title}</title>
        <style>
          :root {{
            color-scheme: light;
            --bg: #f5f7fb;
            --panel: #ffffff;
            --ink: #162033;
            --muted: #64748b;
            --line: #d9e1ec;
            --blue: #1557d8;
            --green: #17835d;
            --violet: #6d45c7;
          }}
          * {{ box-sizing: border-box; }}
          body {{
            margin: 0;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--ink);
            background:
              linear-gradient(180deg, #edf4ff 0, rgba(237, 244, 255, 0) 360px),
              var(--bg);
            line-height: 1.5;
          }}
          a {{ color: inherit; }}
          main {{
            width: min(1120px, calc(100% - 32px));
            margin: 0 auto;
            padding: 30px 0 44px;
          }}
          .nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 34px;
          }}
          .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 900;
          }}
          .mark {{
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            border-radius: 8px;
            color: #fff;
            background: #111827;
          }}
          .links {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
          }}
          .links a, .button {{
            min-height: 40px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0 13px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            text-decoration: none;
            font-weight: 800;
          }}
          .hero {{
            display: grid;
            grid-template-columns: minmax(0, 1.1fr) minmax(280px, 0.9fr);
            gap: 26px;
            align-items: stretch;
          }}
          .hero-copy {{
            padding: 30px 0;
          }}
          .eyebrow {{
            margin: 0 0 12px;
            color: var(--blue);
            font-size: 0.8rem;
            font-weight: 900;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }}
          h1 {{
            margin: 0;
            font-size: clamp(2.25rem, 6vw, 4.6rem);
            line-height: 0.98;
            letter-spacing: 0;
          }}
          .lead {{
            margin: 20px 0 0;
            max-width: 650px;
            color: #475569;
            font-size: 1.08rem;
          }}
          .panel {{
            padding: 22px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            box-shadow: 0 18px 48px rgba(15, 23, 42, 0.08);
          }}
          .grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 26px;
          }}
          .tile {{
            padding: 20px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
          }}
          .tile h2, .panel h2 {{
            margin: 0 0 8px;
            font-size: 1rem;
          }}
          .tile p, .panel p {{
            margin: 0;
            color: var(--muted);
          }}
          .metric {{
            display: flex;
            justify-content: space-between;
            gap: 18px;
            padding: 14px 0;
            border-top: 1px solid #edf1f6;
          }}
          .metric:first-of-type {{ border-top: 0; }}
          .metric strong {{ font-size: 0.92rem; }}
          .metric span {{ color: var(--muted); text-align: right; overflow-wrap: anywhere; }}
          .ok {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 11px;
            border-radius: 999px;
            color: var(--green);
            background: rgba(23, 131, 93, 0.09);
            font-weight: 900;
          }}
          .ok::before {{
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
          }}
          pre {{
            margin: 16px 0 0;
            padding: 16px;
            border-radius: 8px;
            overflow: auto;
            color: #dbeafe;
            background: #111827;
          }}
          @media (max-width: 820px) {{
            .hero, .grid {{ grid-template-columns: 1fr; }}
            .nav {{ align-items: flex-start; flex-direction: column; }}
          }}
        </style>
      </head>
      <body>
        <main>
          <nav class="nav" aria-label="Primary navigation">
            <a class="brand" href="/">
              <span class="mark">PD</span>
              <span>PDeploy</span>
            </a>
            <div class="links">
              <a href="/health">Health</a>
              <a href="/info">Info</a>
              <a href="/docs">Docs</a>
            </div>
          </nav>
          <section class="hero">
            <div class="hero-copy">
              <p class="eyebrow">{eyebrow}</p>
              <h1>{title}</h1>
            </div>
            <aside class="panel">
              {body}
            </aside>
          </section>
        </main>
      </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
def home():
    """Render-friendly landing page for the portfolio API."""
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>PDeploy API</title>
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
              <div class="mark">PD</div>
              <span>PDeploy</span>
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
def health_check(request: Request):
    """
    Health check endpoint — Kubernetes uses this to verify the app is alive.
    Returns: status and current UTC timestamp
    """
    data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "pdeploy-api"
    }

    if wants_html(request):
        return HTMLResponse(page_shell(
            "PDeploy Health",
            "Runtime status",
            f"""
              <h2>Service Check</h2>
              <p class="ok">Healthy</p>
              <div style="margin-top: 18px">
                <div class="metric"><strong>Status</strong><span>{data["status"]}</span></div>
                <div class="metric"><strong>Service</strong><span>{data["service"]}</span></div>
                <div class="metric"><strong>Timestamp</strong><span>{data["timestamp"]}</span></div>
              </div>
              <pre>{data}</pre>
            """
        ))

    return data

@app.get("/info")
def get_info(request: Request):
    """
    Application metadata endpoint.
    Returns: project details and author information
    """
    data = {
        "project": "PDeploy",
        "version": "1.0.0",
        "author": "Pravinkumar Choudhary",
        "github": "github.com/speedprav",
        "description": "Production CI/CD pipeline demo",
        "tech_stack": [
            "FastAPI", "Docker", "Kubernetes",
            "GitHub Actions", "Prometheus", "Grafana"
        ]
    }

    if wants_html(request):
        tech = "".join(f"<span>{item}</span>" for item in data["tech_stack"])
        return HTMLResponse(page_shell(
            "PDeploy Info",
            "Project profile",
            f"""
              <h2>{data["project"]}</h2>
              <p>{data["description"]}</p>
              <div style="margin-top: 18px">
                <div class="metric"><strong>Version</strong><span>{data["version"]}</span></div>
                <div class="metric"><strong>Author</strong><span>{data["author"]}</span></div>
                <div class="metric"><strong>GitHub</strong><span>{data["github"]}</span></div>
              </div>
              <div class="grid" style="grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 18px">
                <div class="tile"><h2>Delivery</h2><p>Container build, deploy workflow, and health probes.</p></div>
                <div class="tile"><h2>Monitoring</h2><p>Prometheus metrics endpoint for operational visibility.</p></div>
              </div>
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px">{tech}</div>
            """
        ))

    return data

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    return HTMLResponse(f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>PDeploy API Docs</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <style>
          body {{
            margin: 0;
            background: #f5f7fb;
            color: #162033;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          }}
          .docs-header {{
            padding: 24px min(32px, 5vw);
            border-bottom: 1px solid #d9e1ec;
            background: linear-gradient(135deg, #ffffff 0, #edf4ff 100%);
          }}
          .docs-nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            max-width: 1180px;
            margin: 0 auto 24px;
          }}
          .brand {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            color: #162033;
            text-decoration: none;
            font-weight: 900;
          }}
          .mark {{
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            border-radius: 8px;
            color: #fff;
            background: #111827;
          }}
          .links {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
          }}
          .links a {{
            min-height: 40px;
            display: inline-flex;
            align-items: center;
            padding: 0 13px;
            border: 1px solid #d9e1ec;
            border-radius: 8px;
            color: #162033;
            background: #fff;
            text-decoration: none;
            font-weight: 800;
          }}
          .docs-hero {{
            max-width: 1180px;
            margin: 0 auto;
          }}
          .docs-hero p {{
            max-width: 680px;
            margin: 14px 0 0;
            color: #64748b;
            font-size: 1.05rem;
          }}
          h1 {{
            margin: 0;
            font-size: clamp(2rem, 5vw, 4.4rem);
            line-height: 1;
            letter-spacing: 0;
          }}
          #swagger-ui {{
            max-width: 1180px;
            margin: 24px auto 44px;
            padding: 0 min(20px, 4vw);
          }}
          .swagger-ui .topbar {{ display: none; }}
          .swagger-ui .scheme-container,
          .swagger-ui .opblock,
          .swagger-ui .info {{
            border-radius: 8px;
            box-shadow: none;
          }}
          .swagger-ui .info {{ margin: 24px 0; }}
          .swagger-ui .info .title {{ color: #162033; }}
          @media (max-width: 700px) {{
            .docs-nav {{ align-items: flex-start; flex-direction: column; }}
          }}
        </style>
      </head>
      <body>
        <header class="docs-header">
          <nav class="docs-nav">
            <a class="brand" href="/">
              <span class="mark">PD</span>
              <span>PDeploy</span>
            </a>
            <div class="links">
              <a href="/">Home</a>
              <a href="/health">Health</a>
              <a href="/info">Info</a>
            </div>
          </nav>
          <div class="docs-hero">
            <h1>PDeploy API Docs</h1>
            <p>Explore the production API contract, test requests, inspect schemas, and validate responses from one clean developer surface.</p>
          </div>
        </header>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
          window.ui = SwaggerUIBundle({{
            url: "{app.openapi_url}",
            dom_id: "#swagger-ui",
            deepLinking: true,
            displayRequestDuration: true,
            filter: true,
            defaultModelsExpandDepth: -1,
            presets: [SwaggerUIBundle.presets.apis],
            layout: "BaseLayout"
          }});
        </script>
      </body>
    </html>
    """)

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
