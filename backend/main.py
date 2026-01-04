from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

# Import Service Modules
from backend.rag_service import retrieve_context
from backend.llm.gemini import generate_response as gemini_generate
# Lazy import for local LLM to avoid heavy load on startup if not needed immediately
# from backend.llm.local import LocalLLM

app = FastAPI(title="LAWKEASH AI Backend", version="1.0")

class ChatRequest(BaseModel):
    query: str
    use_local: bool = False

class ChatResponse(BaseModel):
    response: str
    context_used: str
    source: str = "Gemini"

@app.get("/")
def read_root():
    return {"status": "online", "message": "LAWKEASH AI Backend is running."}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint.
    1. Retrieves context from RAG.
    2. Constructs a prompt.
    3. Sends to LLM (Gemini by default, or Local if requested).
    """
    
    # 1. Retrieve Context
    context = retrieve_context(request.query)
    
    # 2. Construct Prompt
    if "No relevant legal context found" in context:
        prompt = f"""You are an expert Indian Legal Consultant.
The user has asked a question regarding Indian Law.
Please provide a comprehensive answer using your own legal knowledge.
State clearly that this advice is based on general knowledge as no specific documents were retrieved from the local database.

Question: {request.query}

Answer:"""
    else:
        prompt = f"""You are an expert Indian Legal Consultant.
Answer the user's question based primarily on the specific legal context provided below.
Cite the Acts and Sections explicitly.
If the context is insufficient, supplement it with your general knowledge but clearly distinguish between what is in the documents and what is not.

Context provided:
{context}

Question: {request.query}

Answer:"""

    # 3. Generate Response
    if request.use_local:
        # Import here to avoid loading model globally on start unless used
        try:
            from backend.llm.local import LocalLLM
            llm = LocalLLM.get_instance()
            response_text = llm.generate_response(prompt)
            source = "Local Mistral"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Local LLM Error: {str(e)}")
            
    else:
        # Use Gemini
        response_text = gemini_generate(prompt)
        source = "Gemini Pro"
    
    
    # Add Disclaimer
    disclaimer = "\n\nDisclaimer: This is AI-generated legal advice. Please consult a qualified lawyer for professional advice."
    response_text += disclaimer
    
    return ChatResponse(
        response=response_text,
        context_used=context,
        source=source
    )

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
