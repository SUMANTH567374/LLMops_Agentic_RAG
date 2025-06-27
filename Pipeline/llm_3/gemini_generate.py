# File: llm_3/gemini_generate.py

import os
import yaml
import google.generativeai as genai
from dotenv import load_dotenv
from logging_config import setup_logger

# Load environment variables from .env (for API key)
load_dotenv()

# Setup logger
logger = setup_logger("gemini_generate")

# Load config.yaml for model configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Get model name from config
GEMINI_MODEL_NAME = config["gemini"]["model_name"]

# Get API key from environment (not from config.yaml)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini SDK
genai.configure(api_key=GEMINI_API_KEY)

# Instantiate the Gemini model
model = genai.GenerativeModel(GEMINI_MODEL_NAME)

def generate_with_gemini(prompt: str) -> str:
    """
    Generate a response using Google's Gemini model.

    Args:
        prompt (str): Prompt to send to Gemini.

    Returns:
        str: Generated text response.
    """
    if not GEMINI_API_KEY:
        logger.error("❌ Gemini API key missing.")
        return "API key not set."

    try:
        logger.info("📤 Sending prompt to Gemini model...")
        response = model.generate_content(prompt)
        text = response.text.strip()
        logger.info("✅ Successfully received response from Gemini.")
        return text

    except Exception as e:
        logger.exception("❌ Unexpected error calling Gemini:", exc_info=e)
        return "Gemini error."
