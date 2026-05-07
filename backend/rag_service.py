import chromadb
from chromadb.utils import embedding_functions
import os
import re
from typing import List, Dict, Any, Tuple, Optional
from functools import lru_cache

# Optimizations
try:
    from sentence_transformers import CrossEncoder
    # Load re-ranker model - optimized for speed/accuracy trade-off
    RERANKER = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2-v2') 
    HAS_RERANKER = True
except ImportError:
    print("sentence-transformers not found. Re-ranking disabled.")
    RERANKER = None
    HAS_RERANKER = False

# Configuration
DB_DIR = r"d:\coding_projects\LAWKEASH_v1\RAG\vector_store"
COLLECTION_NAME = "indian_law"

# Regex patterns for Act detection
ACT_PATTERNS = {
    "ipc": [r"ipc", r"indian penal code"],
    "crpc": [r"crpc", r"criminal procedure"],
    "cpc": [r"cpc", r"civil procedure"],
    "iea": [r"evidence act", r"iea"],
    "consti": [r"constitution", r"article"],
    "mva": [r"motor vehicle", r"mva"],
    "hma": [r"hindu marriage", r"hma"],
    "nia": [r"negotiable instrument", r"nia", r"cheque bounce"]
}

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

_chroma_client = None
_embed_fn = None
_collection = None

def get_chroma_collection():
    global _chroma_client, _embed_fn, _collection
    if _collection is None:
        try:
            _chroma_client = chromadb.PersistentClient(path=DB_DIR)
            _embed_fn = get_embedding_function()
            _collection = _chroma_client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=_embed_fn
            )
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            return None
    return _collection

def extract_metadata_filters(query: str) -> Dict[str, Any]:
    """
    Extracts potential metadata filters (Act names, Sections) from the query.
    """
    query_lower = query.lower()
    filters = {}
    
    # 1. Detect Act
    for act_key, patterns in ACT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query_lower):
                # Map short keys back to full Act names if needed, or rely on loose matching if schema varies
                # For now, we return the key or we can try to map to the exact 'act' field in DB if we know it.
                # Since DB 'act' fields are full names (e.g., "Indian Penal Code"), we should map them.
                if act_key == "ipc": filters["act"] = "Indian Penal Code"
                elif act_key == "crpc": filters["act"] = "Code of Criminal Procedure"
                elif act_key == "iea": filters["act"] = "Indian Evidence Act"
                elif act_key == "cpc": filters["act"] = "Code of Civil Procedure"
                elif act_key == "mva": filters["act"] = "Motor Vehicles Act"
                elif act_key == "hma": filters["act"] = "Hindu Marriage Act"
                elif act_key == "nia": filters["act"] = "Negotiable Instruments Act"
                break
    
    # 2. Detect Section
    # Pattern: "Section 302", "Sec 420", "Section 304A", etc.
    sec_match = re.search(r"(?:section|sec|s\.)\s*(\d+[A-Za-z]*)", query_lower)
    if sec_match:
        filters["section"] = sec_match.group(1)
        
    return filters

@lru_cache(maxsize=100)
def retrieve_context(query_text: str, n_initial: int = 10, n_final: int = 5) -> str:
    """
    Retrieves context using Hybrid Search:
    1. Metadata Filtering (if Act/Section detected)
    2. Vector Search (Semantic)
    3. Re-ranking (Cross-Encoder)
    """
    try:
        collection = get_chroma_collection()
        if collection is None:
            return "Error initializing vector database collection."
        
        # 1. Build Query Filters based on metadata
        filters = extract_metadata_filters(query_text)
        where_clause = {}
        
        if "act" in filters:
            where_clause["act"] = filters["act"]
        
        # Note: Filtering by specific section might be too strict if the user asks about a concept in that section
        # but the chunk is split. However, if they explicitly mention section, we can boost or filter.
        # Let's use 'act' for hard filtering if detected, but keeps 'section' for re-ranking boost or soft filter.
        # For now, strict filtering on Act is safe. Strict filtering on Section is risky if data quality varies.
        
        print(f"Retrieving for query: '{query_text}' with filters: {where_clause}")

        # 2. Initial Vector Retrieval (Fetch more candidates: n_initial)
        results = collection.query(
            query_texts=[query_text],
            n_results=n_initial,
            where=where_clause if where_clause else None
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "No relevant legal context found."

        # Flatten results for re-ranking
        candidates = []
        for i in range(len(results['ids'][0])):
            candidates.append({
                "id": results['ids'][0][i],
                "doc": results['documents'][0][i],
                "meta": results['metadatas'][0][i],
                "initial_score": results['distances'][0][i] if 'distances' in results else 0
            })

        # 3. Re-ranking
        if HAS_RERANKER and candidates:
            # Pair query with each document content
            pairs = [[query_text, c['doc']] for c in candidates]
            scores = RERANKER.predict(pairs)
            
            # Attach scores
            for i, score in enumerate(scores):
                candidates[i]['rerank_score'] = score
            
            # Sort by re-rank score (descending)
            candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
            
            # Select top N final
            final_selection = candidates[:n_final]
        else:
            # Fallback to vector scores (approximated by order returned if distances not valid)
            final_selection = candidates[:n_final]

        # 4. Format Output
        formatted_context = ""
        for item in final_selection:
            meta = item['meta']
            source_info = f"Act: {meta.get('act')}, Section: {meta.get('section')}"
            formatted_context += f"Source: {source_info}\nContent: {item['doc']}\n\n"
            
        return formatted_context

    except Exception as e:
        print(f"RAG Retrieval Error: {e}")
        return f"Error retrieving context: {str(e)}"
