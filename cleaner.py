import os
from dotenv import load_dotenv
from file_handler import FileHandler
from vector_store_manager import VectorStoreManager

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

DB_NAME = os.getenv("DB_NAME")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

file = "sample files/N2ProductOverviewForAnuj11292024.pdf"

content = FileHandler().read_file_contents(file)
vector_store_manager = VectorStoreManager(DB_NAME, CHUNK_SIZE, CHUNK_OVERLAP)
vector_store_manager.add_content_to_db(content)
