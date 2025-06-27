# File: Pipeline/embeddings_2/query_vector_store.py

import os
import yaml
from typing import List
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from logging_config import setup_logger

from Pipeline.embeddings_2.custom_encoder import SentenceTransformerEmbeddings

# Load .env (for safety if used elsewhere)
load_dotenv()

# Logger setup
logger = setup_logger("query_vector")

# Load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Config values
DB_PATH = config["vector_store"]["db_path"]
TOP_K = config["vector_store"]["top_k"]
ALLOW_DANGER = config["vector_store"]["allow_dangerous_deserialization"]

def query_vector_store(query: str, k: int = TOP_K) -> List[str]:
    """
    Query the FAISS vector store with a natural language question.

    Args:
        query (str): User's question.
        k (int): Number of similar chunks to retrieve.

    Returns:
        List[str]: Retrieved relevant document chunks.
    """
    try:
        if not os.path.exists(DB_PATH):
            logger.error("❌ Vector DB missing. Run build_vector_store.py first.")
            return []

        # Use your custom embedding model
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # Load FAISS vector DB
        db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=ALLOW_DANGER)

        # Retrieve top-k similar chunks
        results: List[Document] = db.similarity_search(query, k=k)

        if not results:
            logger.warning("⚠️ No matching results found.")
            return []

        return [doc.page_content for doc in results]

    except Exception as e:
        logger.exception("💥 Error querying vector store:", exc_info=e)
        return []
