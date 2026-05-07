import os
import json
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

# Configuration
# Configuration
INPUT_DIR = r"d:\coding_projects\LAWKEASH_v1\RAG\cleaned_corpus"
DB_DIR = r"d:\coding_projects\LAWKEASH_v1\RAG\vector_store"
COLLECTION_NAME = "indian_law"

# Ensure DB directory exists
os.makedirs(DB_DIR, exist_ok=True)

def get_embedding_function():
    # Use Nomic Embed Text v1.5 via SentenceTransformers
    # Chroma has a wrapper for SentenceTransformer, or we can use the default and specify model
    # However, Nomic requires `trust_remote_code=True` often, so using sentence_transformers directly is safer for flexibility
    try:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
        return SentenceTransformerEmbeddingFunction(
            model_name="nomic-ai/nomic-embed-text-v1.5",
            device="cpu", # or "cuda" if available, defaults to cpu for compatibility
            trust_remote_code=True
        )
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        # Fallback or allow chroma to try downloading
        return None

def main():
    # Initialize Chroma Client
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Get Embeeding Function
    embed_fn = get_embedding_function()
    
    # Reset Collection to avoid dimension mismatch
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        pass

    # Create or Get Collection
    # HNSW defaults are usually fine
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
        metadata={"description": "Indian Bare Acts RAG System"}
    )
    
    # Load Processed Files
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith("_cleaned.json")]
    
    for filename in files:
        filepath = os.path.join(INPUT_DIR, filename)
        print(f"Indexing {filename}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
            
        # Batch processing to avoid memory issues
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            
            ids = [c["chunk_id"] for c in batch]
            documents = [c["text"] for c in batch]
            metadatas = [{
                "act": c["act"],
                "year": c["year"],
                "section": c["section"],
                "section_title": c["section_title"],
                "source": c["source"]
            } for c in batch]
            
            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
        print(f"Indexed {len(chunks)} chunks from {filename}")
        
    print(f"Total documents in collection: {collection.count()}")

if __name__ == "__main__":
    main()
