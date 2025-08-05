from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any

from backend.app.vanna_agent import ask_vanna, train_vanna

class QueryRequest(BaseModel):
    question: str

app = FastAPI()

# --- CORS Configuration ---
# You need to configure CORS to allow your React frontend to communicate with your FastAPI backend.
# In production, replace "*" with your React app's domain (e.g., "http://localhost:3000" for dev).
origins = [
    "http://localhost",
    "http://localhost:3000", # React development server
    # Add your production React app URL here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup Event to Train Vanna ---
@app.on_event("startup")
async def startup_event():
    print("FastAPI application startup. Training Vanna...")
    # This will train Vanna every time the server starts.
    # In a production environment, you might only run this as a separate script
    # or ensure it only runs once and persists the Vanna state.
    train_vanna()
    print("Vanna training completed during startup.")

# --- API Endpoint ---
@app.post("/api/ask") 
async def ask_query(request: QueryRequest) -> Dict[str, Any]:
    """
    API endpoint to ask Vanna a natural language question.
    """
    question = request.question
    print(f"Received question: {question}")
    
    response = ask_vanna(question)

    if response["error"]:
        print(f"Error processing question: {response['error']}")
        # For security, you might not want to expose raw error messages to the frontend.
        # Customize this based on your security policy.
        raise HTTPException(status_code=500, detail=response["error"])
    
    return {
        "question": question,
        "sql": response["sql"],
        "results": response["results"]
    }

@app.get("/")
async def root():
    return {"message": "Vanna AI Agent Backend is running."}