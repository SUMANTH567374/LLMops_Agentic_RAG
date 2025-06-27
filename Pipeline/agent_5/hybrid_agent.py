# File: 5_agent/hybrid_qa_agent.py

import yaml
from typing import List
from Pipeline.embeddings_2.query_vector_store import query_vector_store
from Pipeline.tools_4.serper_search import SerperSearchAgent
from Pipeline.llm_3.gemini_generate import generate_with_gemini
from logging_config import setup_logger

# Load configuration from config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logger = setup_logger("hybrid_agent")

# Extract prompt and settings from config
ADVANCED_SYSTEM_PROMPT = config["prompt"]["system_prompt"]
TOP_K = config["vector_store"]["top_k"]
SERPER_MAX_RESULTS = config["serper"]["max_results"]

def build_prompt(context: str, user_query: str) -> str:
    """
    Build a detailed and instructive prompt for LLM response.
    """
    return f"""{ADVANCED_SYSTEM_PROMPT}

Context:
{context}

User Question:
{user_query}

Your Answer (strictly based on the context above):
"""

def hybrid_qa_agent(user_query: str, top_k: int = TOP_K) -> str:
    """
    Hybrid RAG Agent: FAISS Vector DB → Serper Search → LLM Response.

    Args:
        user_query (str): The user's question.
        top_k (int): Number of top chunks/snippets to retrieve.

    Returns:
        str: Final generated answer from Gemini.
    """
    try:
        logger.info(f"📩 Received user query: '{user_query}'")
        logger.info("🔍 Step 1: Querying local vector DB...")

        chunks = query_vector_store(user_query, k=top_k)

        if chunks:
            logger.info(f"✅ Retrieved {len(chunks)} relevant chunks from vector DB.")
            context = "\n".join(chunks)
        else:
            logger.warning("⚠️ No data found in vector DB. Using Serper for web search...")

            agent = SerperSearchAgent()
            web_results = agent.search(user_query, max_results=SERPER_MAX_RESULTS)

            if not web_results:
                logger.error("❌ No relevant content found from Serper search.")
                return "I'm sorry, I could not find any relevant information for your question."

            context = "\n".join(web_results)
            logger.info(f"🌐 Collected {len(web_results)} web snippets via Serper.")

        final_prompt = build_prompt(context, user_query)

        logger.info("🤖 Sending prompt to AI LLM...")
        answer = generate_with_gemini(final_prompt)
        logger.info("✅ AI response received.")

        # 🔁 Fallback check: If answer is vague or unhelpful, retry with web search
        fallback_triggers = [
            "does not contain any information",
            "no relevant information",
            "i'm sorry",
            "context is insufficient",
            "i do not know"
        ]

        if any(trigger in answer.lower() for trigger in fallback_triggers):
            logger.warning("⚠️ LLM could not answer from context. Retrying with Serper...")

            agent = SerperSearchAgent()
            web_results = agent.search(user_query, max_results=SERPER_MAX_RESULTS)

            if not web_results:
                logger.error("❌ No relevant content found from Serper fallback.")
                return "I'm sorry, I could not find any relevant information for your question."

            context = "\n".join(web_results)
            final_prompt = build_prompt(context, user_query)

            logger.info("🔁 Re-sending prompt to LLM using Serper context...")
            answer = generate_with_gemini(final_prompt)
            logger.info("✅ AI response from Serper fallback received.")

        return answer

    except Exception as e:
        logger.exception("🚨 Exception in hybrid_qa_agent:", exc_info=e)
        return "An error occurred while generating your response."
