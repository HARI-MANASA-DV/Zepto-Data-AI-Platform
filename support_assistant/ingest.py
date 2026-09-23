from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "zepto_policies"


def load_documents():
    documents = []
    ids = []
    metadatas = []

    for file_path in sorted(DOCS_DIR.glob("doc_*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        documents.append(text)
        ids.append(file_path.stem)
        metadatas.append({"document_id": file_path.stem})

    return ids, documents, metadatas


def build_collection():
    ids, documents, metadatas = load_documents()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(documents).tolist()

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Documents loaded: {len(documents)}")
    print(f"Chroma collection: {COLLECTION_NAME}")
    print(f"Chunks stored: {collection.count()}")


if __name__ == "__main__":
    build_collection()