# Dockerfile for Service Selector Dashboard
# Optimized for OpenShift Container Platform (OCP) deployment

FROM python:3.12 

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_flask.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_flask.txt

# Copy application files
COPY app.py .
COPY service_selector.html .
COPY chart_data.js .

# Copy any additional static files (copy all at once to avoid errors)
COPY . .

# Create non-root user for security (OCP requirement)
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER 1001

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "2", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

# Made with Bob
