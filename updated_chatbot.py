import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from vector_store_manager import VectorStoreManager

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
openai = OpenAI()

DB_NAME = os.getenv("DB_NAME")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 500))
RETRIEVER_SIZE = int(os.getenv("RETRIEVER_SIZE", 40))

# Initialize vector store manager
vector_store_manager = VectorStoreManager(
    DB_NAME, CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVER_SIZE
)

def generate_user_message(query, retrieved_contexts):
    # Construct context block
    context_block = "CONTEXT:\n"
    for i, context in enumerate(retrieved_contexts, 1):
        context_block += f"[Source {i}]\n{context}\n\n"

    # Construct the full prompt
    prompt = f"""
{context_block}
USER QUERY: {query}
ASSISTANT RESPONSE:"""

    return prompt


def chat(message, history):
    # Reload vector store to ensure latest data
    vector_store_manager.reload()
    # Retrieve relevant documents
    retriever = vector_store_manager.as_retriever()
    retrieved_docs = retriever.invoke(message)
    # Extract text from retrieved documents
    retrieved_contexts = [doc.page_content for doc in retrieved_docs]

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for human, assistant in history:
            messages.append({"role": "user", "content": human})
            messages.append({"role": "assistant", "content": assistant})
        messages.append({"role": "user", "content": generate_user_message(message, retrieved_contexts)})
        stream = openai.chat.completions.create(model=MODEL_NAME, messages=messages, stream=True)
        reply = ""
        for chunk in stream:
            fragment = chunk.choices[0].delta.content or ""
            reply += fragment
            yield reply
    except Exception as e:
        print(f"Error in chat function: {e}")
        return "I'm sorry, but there was an error processing your request."

# Gradio Interface
def launch_gradio_interface():
    """
    Launch the Gradio chat interface
    """
    gr.ChatInterface(chat).launch(share=False)

# Main execution
def main():
    launch_gradio_interface()

# Run the app
if __name__ == "__main__":
    main()