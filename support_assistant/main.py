from fastapi import FastAPI
from pydantic import BaseModel, Field
from rag import AnswerResponse, graph
app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline deterministic Zepto policy support assistant",
)
class AskRequest(BaseModel):
    query: str = Field(min_length=1)
@app.get("/")
def root():
    return {"message": "Zepto Support Assistant is running."}
@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest):
    result = graph.invoke({"query": request.query.strip()})
    return AnswerResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0),
    )