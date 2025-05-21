# AI-Powered Goal Setting Assistant & OKR Chatbot

## Introduction/Overview

This web application serves as an AI-powered goal-setting assistant and a specialized chatbot for Objectives and Key Results (OKRs). It provides users with an interactive platform to set goals, receive AI-driven coaching, and gain insights into OKR methodologies by leveraging the knowledge from John Doerr's "Measure What Matters." The application also features dynamic image generation to help visualize user goals.

## Features

*   **Interactive Chat Interface:** A user-friendly web interface for goal setting, coaching, and OKR-related queries.
*   **AI-Powered Goal Feedback:** Utilizes OpenAI's GPT models to provide constructive feedback and coaching on user-defined goals.
*   **Specialized OKR Q&A:** Implements a Retrieval Augmented Generation (RAG) model, using "Measure What Matters" as its knowledge base, to answer questions about Objectives and Key Results.
*   **Dynamic Image Generation:** Generates images related to user goals using the Replicate API to enhance motivation and visualization.
*   **Web Interface:** Built with Flask, providing a responsive and accessible user experience.
*   **Goal Storage (CLI):** The command-line interface version (`app/chatbot.py`) includes functionality to save and display monthly, weekly, and daily goals in a `goals.json` file. The main web application currently focuses on interactive chat and RAG.

## Core Technologies Used

*   **Python:** The primary programming language for the application.
*   **Flask:** Micro web framework used for the web application.
*   **OpenAI API:** Powers the LLM-driven chat for goal coaching (using `gpt-3.5-turbo` in the web app and `gpt-4` in the CLI app) and text embeddings for the RAG system.
*   **Replicate API:** Used for generating goal-related images (specifically "ideogram-ai/ideogram-v2a-turbo" model).
*   **Langchain:** Framework used for implementing the RAG functionality.
*   **FAISS:** Vector store used for efficient similarity search in the RAG system.
*   **"Measure What Matters" by John Doerr:** The core knowledge base document for the OKR RAG feature.

## Prerequisites

*   Python 3.8 or higher
*   pip (Python package installer)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd <project_directory>
    ```
3.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    ```
4.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5.  **Install dependencies:**
    ```bash
    pip install -r app/requirements.txt
    ```
6.  **Set up environment variables:**
    Create a `.env` file in the root project directory and add your API keys:
    ```env
    OPENAI_API_KEY="your_openai_api_key"
    REPLICATE_API_TOKEN="your_replicate_api_token"
    ```
    *(Note: The `OPENAI_API_KEY` is used for both GPT model interactions and embeddings generation.)*

7.  **Build the RAG Index:**
    Run the `index_builder.py` script from the root directory to process `Measure-What-Matters-John-Doerr.pdf`, create text embeddings, and store them in a FAISS index under the `okrs_index/` directory. This step is crucial for the OKR Q&A functionality.
    ```bash
    python index_builder.py
    ```
    This will create `okrs_index/index.faiss` and `okrs_index/index.pkl`.

8.  **Run the Flask application:**
    ```bash
    python app/flask_app.py
    ```

## Usage

*   Once the application is running, open your web browser and navigate to `http://localhost:5001` (or the port specified in your Flask app configuration).
*   Interact with the chatbot to:
    *   Define and refine your personal or professional goals.
    *   Receive AI-generated feedback and coaching on your goals.
    *   Ask questions about OKRs, their implementation, and best practices based on "Measure What Matters."
    *   See an image dynamically generated based on your goal.

## Project Structure

```
.
├── Measure-What-Matters-John-Doerr.pdf # Knowledge base for OKR RAG
├── app/                            # Main application directory
│   ├── flask_app.py                # Flask web server
│   ├── chatbot.py                  # CLI chatbot (alternative interface, includes goal saving)
│   ├── rag_engine.py               # RAG implementation
│   ├── requirements.txt            # Python dependencies for the app
│   ├── static/                     # CSS, JS files for Flask app
│   ├── templates/                  # HTML templates for Flask app
│   └── README.md                   # App-specific README (may contain outdated info)
├── okrs_index/                     # Stores the FAISS index for RAG
│   ├── index.faiss                 # FAISS index data
│   └── index.pkl                   # FAISS index metadata
├── index_builder.py                # Script to build the RAG index
└── README.md                       # Project README (this file)
```

## How it Works

*   **Goal Coaching:** User inputs related to general goal setting are processed by an OpenAI GPT model (e.g., `gpt-3.5-turbo` in the web app). The model provides coaching, feedback, and suggestions to help users formulate effective goals.
*   **OKR Q&A (RAG):** Questions identified as relating to OKRs, goals, objectives, or key results are routed to the Retrieval Augmented Generation (RAG) system.
    1.  The user's query is converted into an embedding.
    2.  This embedding is used to search the FAISS vector index (built from "Measure What Matters") for relevant text chunks.
    3.  The retrieved text chunks and the original query are then passed to an LLM, which generates a comprehensive answer based on the provided context.
*   **Image Generation:** When a goal is submitted, the system makes a call to the Replicate API with the goal description. Replicate then generates a relevant image, and the URL of this image is displayed to the user.

## Future Enhancements

(Potentially, based on ideas from `app/README.md` and common goal-setting app features)
*   User accounts and persistent goal storage in the web application.
*   Goal progress tracking and reminders.
*   Mechanisms for accountability partnerships.
*   Coaching modules for overcoming obstacles and goal recovery.
*   More advanced goal visualization options.

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests to help improve this application.
