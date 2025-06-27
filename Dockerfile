# Use Python 3.10 image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Optional: build vector store inside image (not needed if done externally)
# RUN PYTHONPATH=. python Pipeline/embeddings_2/build_vector_store.py

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "6_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
