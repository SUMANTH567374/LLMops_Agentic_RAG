import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logging_config import setup_logger

# Import your custom embedding encoder
from Pipeline.embeddings_2.custom_encoder import get_embedding  # Update path if needed

load_dotenv()
logger = setup_logger("build_vector")

DATA_PATH = "Pipeline/data_1/Mukku_Sumanth_Updated_Resume_IT.pdf"
DB_PATH = "Pipeline/embeddings_2/vector_store"

def build_vector_store():
    try:
        if not os.path.exists(DATA_PATH):
            logger.error(f"❌ Document not found at path: {DATA_PATH}")
            return

        logger.info("📄 Loading PDF document...")
        loader = PyPDFLoader(DATA_PATH)
        documents = loader.load()

        logger.info("✂️ Splitting document into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        logger.info("🧠 Generating embeddings using custom encoder...")
        embeddings = get_embedding()

        logger.info("📦 Creating FAISS index...")
        db = FAISS.from_documents(chunks, embeddings)
        db.save_local(DB_PATH)
        logger.info(f"✅ Vector store saved at: {DB_PATH}")

    except Exception as e:
        logger.exception("❌ Error in build_vector_store:", exc_info=e)

if __name__ == "__main__":
    build_vector_store()

