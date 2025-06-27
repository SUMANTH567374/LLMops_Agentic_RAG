# File: 6_api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Pipeline.agent_5.hybrid_agent import hybrid_qa_agent
from logging_config import setup_logger
from Pipeline.api_6.schemas import QueryRequest, QueryResponse

# Initialize logger
logger = setup_logger("api")

# Create FastAPI app instance
app = FastAPI(
    title="Hybrid RAG API",
    description="API for AI21-powered hybrid retrieval-augmented generation using vector DB + Serper",
    version="1.0.0"
)

# Enable CORS (⚠️ Allowing all origins - restrict in production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Health Check"])
def health_check():
    """
    Simple health check route.
    """
    logger.info("Health check pinged.")
    return {"status": "🟢 API is running"}

@app.post("/query", response_model=QueryResponse, tags=["RAG Inference"])
def query_agent(request: QueryRequest):
    """
    Endpoint to query the hybrid RAG agent with a user's question.
    """
    try:
        logger.info(f"📩 Received question: {request.question}")
        response = hybrid_qa_agent(request.question)
        logger.info("✅ Query processed successfully.")
        return QueryResponse(answer=response)

    except Exception as e:
        logger.exception("❌ Failed to process query:", exc_info=e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
