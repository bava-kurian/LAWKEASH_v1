# Indian Legal RAG System

This directory contains the implementation of a Retrieval Augmented Generation (RAG) system specialized for Indian Bare Acts. It allows for semantic searching across legal texts to find relevant sections based on meaning, not just keywords.

## 📂 Project Structure

- **`cleaned_corpus/`**: Stores the normalized and chunked JSON files ready for indexing.
- **`vector_store/`**: Local ChromaDB persistence directory containing the vector embeddings.
- **`normalize_and_chunk.py`**: Script to process raw JSON data into a clean, chunked format.
- **`index_vectors.py`**: Script to embed text chunks and index them into ChromaDB.
- **`evaluate_rag.py`**: CLI tool for testing and evaluating retrieval performance.

## 🚀 Setup & Installation

1. **Prerequisites**: Python 3.10+
2. **Install Dependencies**:
   ```bash
   pip install chromadb sentence-transformers langchain langchain-community langchain_text_splitters tiktoken einops
   ```

## 🛠️ Usage

### 1. Data Processing
If you have new or updated raw JSON files in the `Data` directory, run the normalization script first. This cleans the data and splits large sections into retrieval-friendly chunks.

```bash
python normalize_and_chunk.py
```
*Output: Generates `_cleaned.json` files in `cleaned_corpus/`*

### 2. Indexing
To generate embeddings and store them in the vector database. This uses the **Nomic Embed Text v1.5** model.

```bash
python index_vectors.py
```
*Note: This will clear the existing `vector_store` and rebuild the index from scratch.*

### 3. Search & Evaluation
To query the system and test retrieval accuracy:

```bash
python evaluate_rag.py
```
This runs a set of automated test queries and then enters an interactive loop where you can type your own questions.

## 🧠 Architecture

- **Embedding Model**: `nomic-ai/nomic-embed-text-v1.5` (768 dimensions)
- **Vector Database**: ChromaDB (Local, Persistent)
- **Chunking Strategy**: 
  - Default: 1 Section = 1 Chunk.
  - Large sections (>3000 chars) are semantically split using LangChain's recursive splitter.
- **Metadata**: Each chunk maps back to `Act`, `Section`, and `Year` for precise citation.

## 📜 Covered Acts
- Indian Penal Code (1860)
- Code of Criminal Procedure (1973)
- Indian Evidence Act (1872)
- Code of Civil Procedure (1908)
- Motor Vehicles Act (1988)
- Hindu Marriage Act (1955)
- Industrial Disputes Act (1947)
- Negotiable Instruments Act (1881)
