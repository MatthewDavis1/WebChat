#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qa import QAChat
from rag import RAGVectorStore
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

qa_chat = QAChat()
vector_store = RAGVectorStore()

class WebpageInput(BaseModel):
    url: str

class TextInput(BaseModel):
    text: str

class QuestionInput(BaseModel):
    question: str

@app.post("/add_webpage")
async def add_webpage(input: WebpageInput):
    try:
        vector_store.add_webpages([input.url])
        return {"message": f"Webpage {input.url} added to the vector store."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain_text")
async def explain_text(input: TextInput):
    try:
        explanation = qa_chat.ask_question(f"Explain the following text: {input.text}")
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_vector_store")
async def clear_vector_store():
    try:
        vector_store.clear_vector_store()
        return {"message": "Vector store has been cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(input: QuestionInput):
    try:
        answer = qa_chat.ask_question(input.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
