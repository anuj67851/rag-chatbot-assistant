import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

from file_handler import FileHandler
from vector_store_manager import VectorStoreManager

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

DB_NAME = os.getenv("DB_NAME")

file = "sample files/hr_policy.pdf"

content = FileHandler().read_file_contents(file)

content = FileHandler().clean_text(content)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

vector_store_manager = VectorStoreManager(DB_NAME)

chunks = vector_store_manager.text_splitter.split_text(content)

vector_store_manager.vector_store.add_texts(chunks)

print(f"added {len(chunks)} chunks")

x = 1