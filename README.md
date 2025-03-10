Local GenAI Search - Local Generative Search Engine
Local GenAI Search is a lightweight, local generative search engine designed to run on a 32GB laptop or computer (developed and tested on a MacBook Pro M2 with 32GB RAM). Powered by the Qwen/Qwen2.5-0.5B-Instruct model, this tool allows users to ask questions about the content of their local files, providing concise answers with references to relevant documents that can be opened directly.

The project uses MS MARCO embeddings for semantic search, passing top-ranking documents to the Qwen2.5-0.5B model for response generation. It runs entirely offline, ensuring privacy and independence from external APIs—perfect for personal or sensitive data.

Features
Fully Local: Operates offline with the Qwen/Qwen2.5-0.5B-Instruct model—no API keys required.
File Support: Indexes and searches .pdf, .txt, .docx, and .pptx files in a folder and its subfolders.
Semantic Search: Leverages MS MARCO embeddings for accurate document retrieval.
User Interface: Includes a Streamlit-based UI for easy interaction.
Lightweight: Optimized for modest hardware (e.g., 32GB RAM laptops).
How to Run
Prerequisites
A machine with at least 32GB RAM (e.g., MacBook Pro M2).
Python 3.8+ installed.
Git installed to clone the repository.
Setup Instructions
Clone the Repository:

git clone https://github.com/nikolamilosevic86/local-gen-search.git
cd local-gen-search
Install Requirements:


pip install -r requirements.txt
Index Your Files:
Run the indexing script to process a folder of documents:


python index.py path/to/folder
Example with the provided TestFolder:


python index.py TestFolder
This creates a local Qdrant index of all .pdf, .txt, .docx, and .pptx files.

Start the Search Service:
Launch the local server:


python uvicorn_start.py
The first run may take a few minutes to download the Qwen/Qwen2.5-0.5B-Instruct model from Hugging Face.

Query the Service:
Use the following endpoints with a POST request:

http://127.0.0.1:8000/search
http://127.0.0.1:8000/ask_localai
Example payload:


{"query": "What are knowledge graphs?"}
Set headers: Accept: application/json and Content-Type: application/json.

Sample Python code:

import requests
import json

url = "http://127.0.0.1:8000/ask_localai"
payload = json.dumps({"query": "What are knowledge graphs?"})
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)
Launch the UI:
Start the Streamlit interface:


streamlit run user_interface.py
Open your browser to interact with the tool.

Technology Used
Qwen/Qwen2.5-0.5B-Instruct: A lightweight, instruction-tuned model for local generative answers.
MS MARCO Embeddings: For semantic search over local documents.
Langchain: For chaining retrieval and generation steps.
Transformers: To load and run the Qwen model.
PyPDF2: For parsing PDF files.
Qdrant: Local vector database for indexing.
Why Qwen2.5-0.5B?
The Qwen/Qwen2.5-0.5B-Instruct model is a compact, efficient choice with 0.5 billion parameters, delivering strong performance on resource-constrained devices. It runs locally without API dependencies, making it ideal for a standalone search engine on a 32GB machine.

Learn More
For a detailed guide on building a generative search engine like this, see:

How to Build a Generative Search Engine for Your Local Files | Towards Data Science


Contributors
Benito - Creator and lead developer.
