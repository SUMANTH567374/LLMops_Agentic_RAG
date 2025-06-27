# File: 4_tools/serper_search.py

import os
import http.client
import json
import yaml
from typing import List
from dotenv import load_dotenv
from logging_config import setup_logger

# Load environment variables
load_dotenv()

# Load config.yaml for max_results
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SERPER_MAX_RESULTS = config["serper"]["max_results"]

logger = setup_logger("serper_search_alt")

class SerperSearchAgent:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.host = "google.serper.dev"
        self.endpoint = "/search"

        if not self.api_key:
            logger.error("❌ SERPER_API_KEY not found in environment.")
            raise ValueError("SERPER_API_KEY not set")

    def search(self, query: str, max_results: int = SERPER_MAX_RESULTS) -> List[str]:
        conn = http.client.HTTPSConnection(self.host)

        payload = json.dumps({
            "q": query,
            "gl": "us",
            "hl": "en"
        })

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            logger.info(f"🌐 Sending query to Serper API: {query}")
            conn.request("POST", self.endpoint, payload, headers)
            res = conn.getresponse()
            data = res.read()
            result = json.loads(data.decode("utf-8"))

            snippets = [item.get("snippet", "") for item in result.get("organic", [])[:max_results]]
            logger.info(f"✅ Received {len(snippets)} web results from Serper.")
            return snippets

        except Exception as e:
            logger.exception("❌ Serper search failed:", exc_info=e)
            return []

        finally:
            conn.close()
