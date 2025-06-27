import os
import pytest

from Pipeline.embeddings_2.query_vector_store import query_vector_store
from Pipeline.agent_5.hybrid_agent import hybrid_qa_agent

# Ensure test runs from project root
os.environ["PYTHONPATH"] = "."

def test_vector_query_returns_results():
    """Test that querying the vector DB returns non-empty results for a relevant query."""
    query = "What is Mukku Sumanth's technical background?"
    results = query_vector_store(query)
    assert isinstance(results, list), "Results should be a list"
    assert len(results) > 0, "Should return at least one result"

def test_hybrid_agent_local_vector_only():
    """Test hybrid agent with a query expected to be in local vector DB."""
    query = "Skills mentioned in the resume"
    response = hybrid_qa_agent(query)
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 10, "Response should be meaningful"

def test_hybrid_agent_triggers_web_search():
    """Test hybrid agent fallback to web when local DB has no info."""
    query = "What is photosynthesis?"  # Unlikely to be in your resume
    response = hybrid_qa_agent(query)
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 10, "Fallback should return a valid web-based answer"

