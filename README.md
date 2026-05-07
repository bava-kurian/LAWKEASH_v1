# LAWkeash BOT - Indian Law RAG AI

LAWkeash BOT is an AI-powered legal research assistant designed for Indian Law. It uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers by referencing uploaded Acts and Sections.

## 🚀 Features

-   **Legal RAG Engine**: Retrieves relevant sections from Indian Bare Acts.
-   **AI Chat Interface**: Interactive chat with streaming responses.
-   **Source Citations**: Displays the exact Act, Section, and Page number for every claim.
-   **Legal Disclaimer**: Mandatory disclaimer for AI-generated advice.
-   **Collapsible Sources**: Clean UI with expandable source references.

## ⚡ Performance Optimizations

To ensure real-time query responses, the RAG pipeline is highly optimized:
- **Fast Re-ranking**: Uses the distilled `TinyBERT-L-2-v2` cross-encoder model to rapidly re-rank vector search results with minimal latency.
- **Global Lazy Loading**: The ChromaDB client and embedding models are cached as singletons upon startup, drastically reducing per-query latency (down to ~50 milliseconds for warm starts).
- **Optimized Retrieval Pool**: Limits the initial candidate pool to prevent processing bottlenecks during the computationally heavy cross-encoder phase.

## 🛠️ Tech Stack

-   **Backend**: FastAPI, Python
-   **Frontend**: Next.js, React, Tailwind CSS
-   **LLM**: Gemini Pro (via Google Generative AI) / Local Mistral 7B (Optional)
-   **Vector Store**: ChromaDB
-   **Orchestration**: LangChain

## 📦 Installation & Setup

### Prerequisites
-   Python 3.10+
-   Node.js 18+
-   Google Gemini API Key

### 1. Backend Setup

```bash
# Navigate to project root
cd LAWKEASH

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
# Create a .env file in the root directory:
# GEMINI_API_KEY=your_api_key_here

# Run the Backend
python -m uvicorn backend.main:app --reload
```
*Backend runs on `http://localhost:8000`*

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the Development Server
npm run dev
```
*Frontend runs on `http://localhost:3000`*

## 📝 Usage

1.  Open `http://localhost:3000` in your browser.
2.  Type a legal question (e.g., *"What is the punishment for theft under IPC?"*).
3.  The bot will retrieve relevant context and provide an answer with citations.

## ⚠️ Disclaimer
This is an AI-powered tool. Content generated should **not** be considered professional legal advice. Always consult a qualified advocate.
