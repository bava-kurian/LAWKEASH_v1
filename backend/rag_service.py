import chromadb
from chromadb.utils import embedding_functions
import os

# Configuration
# Assuming the vector store is relative to the project root or absolute path
# Adjust this path if necessary to match your deployment environment
DB_DIR = r"d:\Perosnal Projects\LAWKEASH\RAG\vector_store"
COLLECTION_NAME = "indian_law"

def get_embedding_function():
    try:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
        return SentenceTransformerEmbeddingFunction(
            model_name="nomic-ai/nomic-embed-text-v1.5",
            device="cpu", 
            trust_remote_code=True
        )
    except Exception as e:
        print(f"Error loading embedding function: {e}")
        return None

def retrieve_context(query_text: str, n_results: int = 3) -> str:
    """
    Retrieves relevant context from ChromaDB and formats it as a string.
    """
    try:
        client = chromadb.PersistentClient(path=DB_DIR)
        embed_fn = get_embedding_function()
        
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embed_fn
        )
        
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        formatted_context = ""
        
        # Check if we have results
        if not results['documents'] or not results['documents'][0]:
            return "No relevant legal context found."

        for i in range(len(results['ids'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            
            source_info = f"Act: {meta.get('act')}, Section: {meta.get('section')}"
            formatted_context += f"Source: {source_info}\nContent: {doc}\n\n"
            
        return formatted_context
    except Exception as e:
        print(f"RAG Retrieval Error: {e}")
        return f"Error retrieving context: {str(e)}"
