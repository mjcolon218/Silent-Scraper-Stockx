# --- Stage 1: Build ---
    FROM mcr.microsoft.com/playwright/python:v1.43.1 AS builder
    WORKDIR /app
    
    # Install system packages needed by Playwright (already included in base image)
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # --- Stage 2: Final image ---
    FROM mcr.microsoft.com/playwright/python:v1.43.1
    WORKDIR /app
    
    COPY --from=builder /usr/local /usr/local
    COPY . /app
    
    CMD ["python", "lambda_fn/pricetracker.py"]
    