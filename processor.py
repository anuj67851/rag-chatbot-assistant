import os
from dotenv import load_dotenv
from file_handler import FileHandler
from logging_utility import LoggingUtility
from vector_store_manager import VectorStoreManager
from folder_monitor import FolderMonitor

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

DB_NAME = os.getenv("DB_NAME")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

LOG_DIR = os.getenv("LOG_DIR")
LOG_VERBOSE = bool(os.getenv("LOG_VERBOSE"))

INPUT_FOLDER = os.getenv("INPUT_FOLDER")
PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER")
ERROR_FOLDER = os.getenv("ERROR_FOLDER")

SCANNER_CHECK_TIMER = int(os.getenv("SCANNER_CHECK_TIMER"))

# Initialize components
file_handler = FileHandler()
logger = LoggingUtility(LOG_DIR)
vector_store_manager = VectorStoreManager(DB_NAME, CHUNK_SIZE, CHUNK_OVERLAP)
folder_monitor = FolderMonitor(
    INPUT_FOLDER,
    PROCESSED_FOLDER,
    ERROR_FOLDER,
    file_handler,
    vector_store_manager,
    logger,
    SCANNER_CHECK_TIMER,
)

# Start monitoring
if __name__ == "__main__":
    folder_monitor.start_monitoring()
