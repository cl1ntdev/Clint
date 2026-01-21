# Clint - NORSU AI Assistant

Clint is a web-based AI assistant that can answer questions about a given document. It uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate and context-aware answers.

## About

This project is a simple yet powerful implementation of a RAG pipeline. It uses a FastAPI backend to serve a language model that can answer questions based on a provided text file (`DATA.txt`). The frontend is a clean and simple chat interface that allows users to interact with the AI assistant.

The backend is designed to be deployed on Hugging Face Spaces, and the frontend is a static website that can be hosted anywhere.

## Features

-   **Retrieval-Augmented Generation (RAG):** The AI assistant uses a RAG pipeline to retrieve relevant information from a document and generate human-like answers.
-   **FastAPI Backend:** The backend is built with FastAPI, a modern and fast web framework for Python.
-   **Sentence Transformers:** The project uses Sentence Transformers to create embeddings for the text chunks and the user's questions.
-   **FAISS:** The embeddings are stored in a FAISS index for efficient similarity search.
-   **Groq API:** The project uses the Groq API to generate answers based on the retrieved context.
-   **Dockerized:** The application is containerized using Docker, making it easy to deploy and run.

## Tech Stack

-   **Backend:** Python, FastAPI, Sentence Transformers, FAISS, Groq
-   **Frontend:** HTML, CSS, JavaScript
-   **Deployment:** Docker, Hugging Face Spaces

## Getting Started

To run the project locally, you need to have Docker and Docker Compose installed.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```
2.  **Create a `.env` file:**
    In the `backend` directory, create a `.env` file and add your Groq API key:
    ```
    GROQ_API_KEY=your-groq-api-key
    ```
3.  **Add your data:**
    Place the text file you want the AI to learn from in the `backend` directory and name it `DATA.txt`.
4.  **Run the application:**
    ```bash
    docker-compose up -d --build
    ```
5.  **Access the application:**
    The frontend will be available at `http://localhost:8000`, and the backend will be available at `http://localhost:8080`.

## Configuration

The following environment variables can be configured in the `backend/.env` file:

-   `GROQ_API_KEY`: Your Groq API key.

The following constants can be configured in `backend/server.py`:

-   `DATA_FILE`: The name of the data file (default: `DATA.txt`).
-   `EMBEDDING_MODEL`: The Sentence Transformer model to use (default: `all-MiniLM-L6-v2`).
-   `EMBEDDING_DIM`: The dimension of the embeddings (default: `384`).
-   `GROQ_MODEL`: The Groq model to use (default: `llama-3.1-8b-instant`).
