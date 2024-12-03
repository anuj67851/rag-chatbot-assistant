from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
import os


class VectorStoreManager:
    def __init__(self, db_name, chunk_size=2000, chunk_overlap=200, retriever_size=40):
        self.db_name = db_name
        self.retriever_size = retriever_size
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " "]
        )
        self.sem_chunker = SemanticChunker(OpenAIEmbeddings())
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
        print(f"Adding {len(chunks)} chunks to vector store.")
        self.vector_store.add_texts(chunks)
        print(f"Vectorstore updated with {len(chunks)} chunks")
