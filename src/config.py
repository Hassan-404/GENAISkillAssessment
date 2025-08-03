from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = "paraphrase-MiniLM-L3-v2"
    LLM_MODEL = "gpt-4o-mini"
    MOCK_ORDERS=r"C:\Users\Hassan X\PycharmProjects\Assessment\data\orders.json"
    TXT_PATH = r"C:\Users\Hassan X\PycharmProjects\Assessment\data\policydoc.txt"
    FAISS_INDEX_DIR = r"C:\Users\Hassan X\PycharmProjects\Assessment\data\faiss_index"