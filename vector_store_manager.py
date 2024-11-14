from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os


class VectorStoreManager:
    def __init__(self, db_name, chunk_size=1000, chunk_overlap=500, retriever_size=10):
        self.db_name = db_name
        self.retriever_size = retriever_size
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        self.vector_store = self._initialize_vector_store()

    def _initialize_vector_store(self):
        if os.path.exists(self.db_name):
            print("Data directory found, reusing it.")
        else:
            print("Persisted directory not found, initializing a new one.")
        return Chroma(
            persist_directory=self.db_name, embedding_function=self.embeddings
        )

    def reload(self):
        """Reload vector store if needed."""
        # Clear previous instances if any, then reinitialize
        self.vector_store = self._initialize_vector_store()
        print("Vector store reloaded.")

    def as_retriever(self):
        """Return the retriever for conversational use."""
        return self.vector_store.as_retriever(search_kwargs={"k": self.retriever_size})

    def add_content_to_db(self, content):
        chunks = self.text_splitter.split_text(content)
        self.vector_store.add_texts(chunks)
        print(f"Vectorstore updated with {len(chunks)} chunks")
