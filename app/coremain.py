from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.agent import run_agent
from app.llm import ask_llm
from app.registry import TOOLS
from app.history import save_research
from app.cal import cal


app = FastAPI(
    title="AI Research Agent API",
    description="API for the AI Research Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "AI Research Agent API is running!"
    }


class ResearchRequest(BaseModel):
    question: str


@app.post("/research")
def research(request: ResearchRequest):

    answer = run_agent(request.question)

    return {
        "question": request.question,
        "answer": answer
    }