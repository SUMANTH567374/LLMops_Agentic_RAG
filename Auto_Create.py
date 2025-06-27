import os

structure = [
    "1_data/health_info.pdf",
    "2_embeddings/build_vector_store.py",
    "2_embeddings/query_vector_store.py",
    "3_llm/ai21_generate.py",
    "4_tools/serper_search.py",
    "5_agent/hybrid_agent.py",
    "6_api/main.py",
    "6_api/schemas.py",
    "tests/test_pipeline.py",
    ".env",
    "config.yaml",
    "requirements.txt",
    "Dockerfile",
    "README.md"
]

def create_structure():
    for path in structure:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Avoid overwriting existing files
        if not os.path.exists(path):
            with open(path, 'w') as f:
                if path.endswith(".py"):
                    f.write(f"# {os.path.basename(path)}\n")
                elif path.endswith(".env"):
                    f.write("AI21_API_KEY=your_key_here\nSERPER_API_KEY=your_key_here\n")
                elif path.endswith("requirements.txt"):
                    f.write("fastapi\nuvicorn\nrequests\nlangchain\nfaiss-cpu\nPyPDF2\n")
                elif path.endswith("README.md"):
                    f.write("# Hybrid RAG with AI21 + Serper AI\n")
                elif path.endswith("config.yaml"):
                    f.write("embedding_model: 'openai'\nvector_db: 'faiss'\n")
                elif path.endswith("Dockerfile"):
                    f.write("FROM python:3.10\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD [\"uvicorn\", \"6_api.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n")
    print("✅ Project structure created.")

create_structure()
