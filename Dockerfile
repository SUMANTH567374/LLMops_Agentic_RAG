# ----------------------------
# Stage 1: Builder
# ----------------------------
FROM python:3.10-slim AS builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --default-timeout=100 --retries=10 --no-cache-dir -r requirements.txt

# ----------------------------
# Stage 2: Final Image
# ----------------------------
FROM python:3.10-slim

WORKDIR /app

# Copy Python libraries from builder
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

# Copy your code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI app using correct path
CMD ["python", "-m", "uvicorn", "Pipeline.api_6.main:app", "--host", "0.0.0.0", "--port", "8000"]
