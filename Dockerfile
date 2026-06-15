# ■■ Stage 1: Builder ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# Use slim Python image to keep the final image small
FROM python:3.11-slim as builder

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (Docker caches this layer if requirements don't change)
# This makes subsequent builds much faster
COPY app/requirements.txt .

# Install dependencies into a separate folder for copying later
RUN pip install --user --no-cache-dir -r requirements.txt

# ■■ Stage 2: Production image ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
FROM python:3.11-slim

# Create a non-root user for security (never run production apps as root)
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app/ .

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local Python packages to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port 8000 for local Docker runs. Hosted platforms like Render inject PORT.
EXPOSE 8000

# Health check — Docker will run this every 30s to verify the container is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://localhost:%s/health' % os.environ.get('PORT', '8000'))"

# Start the application
# --host 0.0.0.0 makes it accessible from outside the container
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
