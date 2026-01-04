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
    # You can refine this prompt template later
    prompt = f"""You are an intelligent legal assistant for Indian Law.
Use the following context to answer the user's question. If the answer is not in the context, use your general knowledge but mention that it is not from the provided source.

Context:
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
    
    return ChatResponse(
        response=response_text,
        context_used=context,
        source=source
    )

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
