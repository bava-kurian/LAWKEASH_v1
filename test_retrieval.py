
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.rag_service import retrieve_context

def test_query(query):
    print(f"\n--- Testing Query: '{query}' ---")
    try:
        context = retrieve_context(query)
        print("Retrieved Context:")
        print(context[:500] + "..." if len(context) > 500 else context)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_query("What is Section 302 of IPC?")
    test_query("Grounds for divorce under Hindu Marriage Act")
    test_query("Motor Vehicle Act insurance requirements")
