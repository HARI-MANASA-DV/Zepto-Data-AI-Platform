# Support Assistant

This module is a simple Zepto policy support assistant.

The assistant uses a set of local policy documents to answer user questions.

## Documents

I used 8 policy documents:

* Delivery Policy
* Returns & Refunds
* Membership Tiers
* Order Tracking
* Order Cancellation Policy
* Damaged or Missing Items
* Gift Cards
* Customer Support Hours

The documents are stored inside the `docs` folder.

## How It Works

The basic flow is:

```text
User Query
   ↓
Intent Classification
   ↓
Policy Question
   ↓
Document Retrieval
   ↓
Answer
```

The documents are converted into embeddings using Sentence Transformers and stored in ChromaDB.

LangGraph is used to manage the flow.

The final response is returned in a structured format using Pydantic.

## Main Files

* `ingest.py` – loads the policy documents into ChromaDB
* `prompt.py` – contains the prompt template
* `rag.py` – retrieval and LangGraph workflow
* `main.py` – FastAPI application
* `docs/` – policy documents
* `chroma_db/` – local ChromaDB data
* `requirements.txt` – required Python packages
* `Dockerfile` – Docker configuration

## Run Locally

Install the required packages:

```bash
pip install -r requirements.txt
```

First load the documents:

```bash
python ingest.py
```

Then start the API:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 7860
```

Open the API documentation in the browser:

```text
http://localhost:7860/docs
```

## Docker

Build the Docker image:

```bash
docker build -t zepto-support-assistant .
```

Run the container:

```bash
docker run --rm -p 7860:7860 zepto-support-assistant
```

Then open:

```text
http://localhost:7860/docs
```

## Offline Mode

The project is configured to work in offline mock mode using the local policy documents. An external LLM API is not required for the basic version.
