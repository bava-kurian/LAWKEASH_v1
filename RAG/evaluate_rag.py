import chromadb
from chromadb.utils import embedding_functions
import os

# Configuration
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
        print(f"Error: {e}")
        return None

def query_rag(query_text: str, n_results: int = 3):
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
    
    return results

def print_results(results):
    for i in range(len(results['ids'][0])):
        print(f"\nResult {i+1}:")
        print(f"ID: {results['ids'][0][i]}")
        meta = results['metadatas'][0][i]
        print(f"Act: {meta.get('act')} (Section {meta.get('section')})")
        print(f"Distance: {results['distances'][0][i]}")
        print("-" * 50)
        print(results['documents'][0][i][:500] + "...") # Preview first 500 chars

def main():
    print("Legal RAG Evaluation CLI")
    print("------------------------")
    
    test_queries = [
        "What is the punishment for murder?",
        "Procedure for arrest without warrant",
        "Definition of cheating",
        "Rights of arrested person"
    ]
    
    print("\nRunning automated test queries...")
    for q in test_queries:
        print(f"\nQuery: {q}")
        try:
            results = query_rag(q)
            print_results(results)
        except Exception as e:
            print(f"Query failed: {e}")

    # Interactive Loop
    while True:
        user_q = input("\nEnter a legal query (or 'q' to quit): ")
        if user_q.lower() == 'q':
            break
        try:
            results = query_rag(user_q)
            print_results(results)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
