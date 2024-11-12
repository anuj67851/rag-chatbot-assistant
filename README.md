# Document-Aware Chatbot with Real-Time Vector Store Updates

This project is a document-aware chatbot built with Python, using LangChain and Chroma for real-time vector storage, and OpenAI's GPT models for conversational AI. Designed to dynamically update its vector store with new documents, this chatbot provides contextually relevant responses by retrieving information from the latest documents.

## Features

- **Real-Time Document Monitoring**: Continuously monitors a designated folder for new or updated documents, automatically adding them to the vector store for contextual retrieval.
- **Efficient Vector Storage with Chroma**: The application uses Chroma for vector storage, utilizing OpenAI embeddings to ensure document content can be effectively retrieved.
- **Intelligent Conversational AI**: Integrates with OpenAI’s conversational models to provide responses based on the most relevant documents in the vector store.
- **Modular Design**: Organized into classes for vector store management, file monitoring, logging, and chatbot handling, making the codebase easy to understand, maintain, and expand.
- **Web Interface with Gradio**: Offers a user-friendly, web-based interface powered by Gradio, allowing users to chat with the bot from their browser.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/anuj67851/rag-chatbot-assistant
   cd rag-chatbot-assistant
   ```

2. **Install Dependencies: Install the required packages using ```pip```**:
    ```bash
    pip install -r requirements.txt
    ```

3. Set Up Environment Variables: Copy the provided ```.env.example``` to ```.env``` and replace placeholders with your information (e.g., API keys).

    ```bash
    cp .env.example .env
    ```

4. Configure API Keys:

    Set your ```OPENAI_API_KEY``` in the ```.env``` file to enable the chatbot to use OpenAI's language model.
    Ensure all other necessary credentials and params are filled out as needed.
## Usage

1. **Start the Application**: 

Run the `processor.py` script to start monitoring the designated input folder for new documents as well as setting up chroma and logging.

    ```bash
    python processor.py
    ```


Run the `chatbot.py` script to launch the Gradio-based chatbot.

    ```bash
    python chatbot.py
    ```

2. **Add Documents**: Place documents in the `input` folder for real-time updates to the vector store. Supported formats include `.pdf`, `.txt`, `.docx`, `.doc` and `.md`.

3. **Interact with the Chatbot**: Access the Gradio interface in your browser and start interacting with the chatbot. It will provide responses based on the content of the documents in the vector store.

## Project Structure

- `file_handler.py`: Handles the reading and processing of various document formats, including `.pdf`, `.docx`, `.doc`, `.txt`, and `.md`.
- `folder_monitor.py`: Monitors the specified input folder and triggers updates when new documents are added, moved, or modified.
- `vector_store_manager.py`: Manages the vector store using Chroma and updates the vector database with new documents in real-time.
- `logging_utility.py`: Provides logging capabilities, recording the status of document processing to a CSV log file.
- `chatbot.py`: Main entry point for running the chatbot, launching the Gradio interface, 
- `processor.py`: Program which is responsible for file scanning and updating vector database.
- `.env`: Stores configuration details like API keys, folder paths, and vector store settings.

## Configuration

The `.env` file contains essential configuration details:

- **API Keys**: Set `OPENAI_API_KEY` for OpenAI’s language model.
- **Vector Store Settings**: Adjust `DB_NAME`, `CHUNK_SIZE`, and `CHUNK_OVERLAP` to control the vector storage parameters.
- **Folders**: Define paths for `INPUT_FOLDER`, `PROCESSED_FOLDER`, and `ERROR_FOLDER`.
- **Logging**: Set `LOG_DIR` and enable verbose logging with `LOG_VERBOSE`.

## Requirements

- Python 3.7 or higher
- Required libraries (see `requirements.txt` for full list)

## Troubleshooting

- **Vector Store Not Updating**: Ensure the folder monitor is running, and new documents are placed in the correct input folder.
- **API Key Errors**: Verify that `OPENAI_API_KEY` is set in the `.env` file and has access to the required model.
- **File Permissions**: Make sure the script has permission to read from the input folder and write to the processed and error folders.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
