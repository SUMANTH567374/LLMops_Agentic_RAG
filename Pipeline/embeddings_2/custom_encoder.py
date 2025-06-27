# File: Pipeline/embeddings_2/custom_encoder.py

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings

load_dotenv()

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, text):
        return self.model.encode(text, show_progress_bar=False)

def get_embedding():
    return SentenceTransformerEmbeddings()
