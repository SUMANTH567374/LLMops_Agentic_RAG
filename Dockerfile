FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "Pipeline.api_6.main:app", "--host", "0.0.0.0", "--port", "8000"]
