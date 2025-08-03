from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from config import Config
import os
from pathlib import Path

FAISS_INDEX_DIR = Config.FAISS_INDEX_DIR


class PolicyRetriever:
    def __init__(self):
        try:
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=Config.OPENAI_API_KEY
            )

            if os.path.exists(FAISS_INDEX_DIR):
                print("Loading existing FAISS index...")
                self.vectorstore = FAISS.load_local(
                    folder_path=FAISS_INDEX_DIR,
                    embeddings=self.embeddings,
                    allow_dangerous_deserialization=True  # Required for security
                )
            else:
                print("Creating new FAISS index...")
                docs = self._load_documents()
                self.vectorstore = FAISS.from_documents(docs, self.embeddings)
                Path(FAISS_INDEX_DIR).mkdir(parents=True, exist_ok=True)
                self.vectorstore.save_local(FAISS_INDEX_DIR)
                print(f"FAISS index saved to: {FAISS_INDEX_DIR}")

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(
                    model=Config.LLM_MODEL,
                    api_key=Config.OPENAI_API_KEY,
                    temperature=0
                ),
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                chain_type="stuff"
            )

        except Exception as e:
            raise RuntimeError(f"Failed to initialize RAG system: {str(e)}")

    def _load_documents(self):
        try:
            loader = TextLoader(Config.TXT_PATH)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100
            )
            return splitter.split_documents(loader.load())
        except Exception as e:
            raise RuntimeError(f"Failed to load documents: {str(e)}")

    def query(self, question: str) -> str:
        try:
            return self.qa_chain.invoke({"query": question})["result"]
        except Exception as e:
            return f"Error processing your query: {str(e)}"


if __name__ == "__main__":
    rag = PolicyRetriever()
    print(rag.query("What is the return policy of general terms?"))
