import os
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from vector_store_manager import VectorStoreManager
from logging_utility import LoggingUtility
from file_handler import FileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = float(os.getenv("TEMPERATURE"))

DB_NAME = os.getenv("DB_NAME")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
RETRIEVER_SIZE = int(os.getenv("RETRIEVER_SIZE"))

LOG_DIR = os.getenv("LOG_DIR")
LOG_VERBOSE = bool(os.getenv("LOG_VERBOSE"))

INPUT_FOLDER = os.getenv("INPUT_FOLDER")
PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER")
ERROR_FOLDER = os.getenv("ERROR_FOLDER")

# Initialize components
file_handler = FileHandler()
logger = LoggingUtility(LOG_DIR)
vector_store_manager = VectorStoreManager(
    DB_NAME, CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVER_SIZE
)


# Set up the LLM and memory
llm = ChatOpenAI(temperature=TEMPERATURE, model_name=MODEL_NAME)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# Chat function for Gradio
def chat(message, history):
    vector_store_manager.reload()
    retriever = vector_store_manager.as_retriever()
    retrieved_docs = retriever.invoke(message)


    print(
        f"Number of documents in store: {len(vector_store_manager.vector_store.get()['documents'])}"
    )
    print(f"Number of documents retrieved: {len(retrieved_docs)}")

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, memory=memory
    )

    result = conversation_chain.invoke({"question": message})
    return result["answer"]


# Gradio Interface
def launch_gradio_interface():
    gr.ChatInterface(chat).launch()


# initialize Gradio interface
def main():
    launch_gradio_interface()


# Run the app
if __name__ == "__main__":
    main()
