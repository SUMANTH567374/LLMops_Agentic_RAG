# Use smaller base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install only curl, remove cache to keep size small
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies without cache
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Now copy all app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "Pipeline.api_6.main:app", "--host", "0.0.0.0", "--port", "8000"]
