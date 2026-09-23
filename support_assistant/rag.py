import os
from pathlib import Path
from typing import TypedDict
import chromadb
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from langgraph.graph import END, START, StateGraph
BASE_DIR = Path(__file__).parent
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "zepto_policies"
MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"
class AssistantState(TypedDict, total=False):
    query: str
    intent: str
    retrieved_chunks: list[dict]
    answer: str
    sources: list[str]
    confidence: float


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0, le=1)


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)
def classify_intent(state: AssistantState) -> dict:
    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours",
    ]

    intent = (
        "policy_question"
        if any(keyword in query for keyword in policy_keywords)
        else "general_question"
    )

    return {"intent": intent}
def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        chunks.append(
            {
                "document_id": metadata["document_id"],
                "text": document,
                "distance": distance,
                "similarity": 1 - distance,
            }
        )

    return chunks
def retrieve_and_answer(state: AssistantState) -> dict:
    chunks = retrieve_chunks(state["query"], top_k=3)

    top_chunk = chunks[0]
    answer = top_chunk["text"]
    confidence = 1.0

    sources = [chunk["document_id"] for chunk in chunks]

    return {
        "retrieved_chunks": chunks,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }
def direct_answer(state: AssistantState) -> dict:
    return {
        "answer": "I can only answer questions about Zepto policies right now.",
        "sources": [],
        "confidence": 1.0,
    }
def route_intent(state: AssistantState) -> str:
    return state["intent"]


workflow = StateGraph(AssistantState)

workflow.add_node("classify_intent", classify_intent)
workflow.add_node("retrieve_and_answer", retrieve_and_answer)
workflow.add_node("direct_answer", direct_answer)

workflow.add_edge(START, "classify_intent")

workflow.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "policy_question": "retrieve_and_answer",
        "general_question": "direct_answer",
    },
)

workflow.add_edge("retrieve_and_answer", END)
workflow.add_edge("direct_answer", END)

graph = workflow.compile()
def validate_response(data: dict) -> AnswerResponse:
    return AnswerResponse.model_validate(data)


def generate_with_retry(
    llm_call,
    prompt: str,
    max_retries: int = 2,
) -> AnswerResponse:
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            result = llm_call(prompt)

            if isinstance(result, AnswerResponse):
                return result

            if isinstance(result, dict):
                return validate_response(result)

            raise ValueError("LLM response must be a dictionary.")

        except Exception as error:
            last_error = error

            prompt = (
                prompt
                + "\n\nCORRECTION:\n"
                "Your previous response failed schema validation. "
                "Return only a valid JSON object with exactly these fields: "
                "answer (string), sources (list of strings), "
                "confidence (number from 0 to 1)."
            )

    return AnswerResponse(
        answer=f"ERROR: Unable to produce a valid structured response after retries: {last_error}",
        sources=[],
        confidence=0.0,
    )
