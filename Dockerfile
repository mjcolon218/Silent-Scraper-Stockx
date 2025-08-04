# --- Base image with Python + Playwright + Browsers ---
    FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

    # Set working directory
    WORKDIR /app
    
    # Copy requirements first to leverage Docker caching
    COPY requirements.txt .
    
    # Install Python packages
    RUN pip install --no-cache-dir -r requirements.txt && rm -rf ~/.cache/pip
    
    # Install Playwright browsers (optional — image already includes them, but this ensures latest)
    RUN playwright install --with-deps
    
    # Copy source code
    COPY . .
    
    # Run the main script
    CMD ["python", "lambda_fn/pricetracker.py"]
    