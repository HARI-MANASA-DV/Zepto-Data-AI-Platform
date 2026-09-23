# Support Assistant

This module is a simple Zepto policy support assistant. It uses 8 local policy documents to answer questions about Zepto policies.

## Documents

The project contains these 8 documents:

* Delivery Policy
* Returns & Refunds
* Membership Tiers
* Order Tracking
* Order Cancellation Policy
* Damaged or Missing Items
* Gift Cards
* Customer Support Hours

The documents are stored in the `docs/` folder.

## How It Works

The RAG flow is:

```text
Ingestion
   ↓
Embedding
   ↓
Retrieval
   ↓
Generation
```

### 1. Ingestion

`ingest.py` reads all `doc_*.txt` files from the `docs/` folder and stores them in ChromaDB.

### 2. Embedding

`ingest.py` uses the Sentence Transformers model:

```text
all-MiniLM-L6-v2
```

The embeddings are stored in the local `chroma_db/` directory.

### 3. Retrieval

`rag.py` contains the `retrieve_chunks()` function. It converts the user query into an embedding and searches the `zepto_policies` ChromaDB collection for the most similar documents.

### 4. Generation

`rag.py` contains the `retrieve_and_answer` node. It uses the top retrieved chunk to create the answer in mock mode.

The `MOCK_LLM` setting controls the generation stage.

With the default setting:

```text
MOCK_LLM=1
```

the assistant uses a fixed response based on the top retrieved document and does not make an external LLM call.

With:

```text
MOCK_LLM=0
```

the code takes the optional non-mock branch. The current offline version does not configure an external LLM provider, so it returns a fixed message instead. The `generate_with_retry()` function is included for structured validation and retry handling if a real LLM is connected later.

## LangGraph Flow

The LangGraph workflow is defined in `rag.py`.

It contains three nodes:

```text
classify_intent
        |
        +----------------------+
        |                      |
policy_question        general_question
        |                      |
        v                      v
retrieve_and_answer     direct_answer
        |                      |
        +----------+-----------+
                   |
                  END
```

`classify_intent` uses keywords such as `delivery`, `return`, `refund`, `membership`, `tracking`, `cancel`, `gift card`, and `support hours`.

A policy-style question is routed to `retrieve_and_answer`.

An unrelated question is routed to `direct_answer`.

## Example 1 — Policy Question

Input:

```text
What is the delivery policy?
```

The intent is:

```text
policy_question
```

The retrieval step returns `doc_01` as the top result.

Example structured response:

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard delivery is free on orders over INR 149; orders below this threshold incur a flat INR 25 delivery fee. Priority delivery, which reserves the next available rider slot, is available at checkout for an additional INR 15. Zepto does not currently deliver to addresses outside its listed serviceable pin codes.",
  "sources": [
    "doc_01",
    "doc_02",
    "doc_05"
  ],
  "confidence": 1.0
}
```

This example uses the default `MOCK_LLM` mode.

## Example 2 — Unrelated Question

Input:

```text
What is the weather today?
```

The intent is:

```text
general_question
```

The query is routed to the `direct_answer` node, so no policy document is retrieved.

Example structured response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

This example also uses the default `MOCK_LLM` mode.

## Structured Response

The response is validated using Pydantic.

The response contains exactly these fields:

```text
answer
sources
confidence
```

`confidence` is restricted to a value between 0 and 1.

The `generate_with_retry()` function is also included to validate an optional real-LLM response and retry when the response does not follow the required structure.

## Prompt Template

`prompt.py` contains the prompt template used for the optional real-LLM extension.

The template includes:

* Role
* Context
* Task
* Format
* Length
* Negative constraint
* Few-shot example
* User query

The negative constraint tells the assistant not to use outside knowledge or invent Zepto policies.

## Main Files

* `ingest.py` – loads and embeds the policy documents
* `prompt.py` – prompt template for the optional real-LLM path
* `rag.py` – retrieval, intent routing and answer generation
* `main.py` – FastAPI application
* `docs/` – 8 policy documents
* `chroma_db/` – local ChromaDB index
* `requirements.txt` – required Python packages
* `Dockerfile` – Docker configuration

## Run Locally

Open a terminal inside the `support_assistant` folder.

Install the required packages:

```bash
pip install -r requirements.txt
```

Load the documents into ChromaDB:

```bash
python ingest.py
```

Expected output:

```text
Documents loaded: 8
Chroma collection: zepto_policies
Chunks stored: 8
```

Start the FastAPI application:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 7860
```

Open the API documentation:

```text
http://localhost:7860/docs
```

## API Example

The main endpoint is:

```text
POST /ask
```

Example request:

```json
{
  "query": "What is the delivery policy?"
}
```

The API returns a JSON response containing `answer`, `sources`, and `confidence`.

## Docker

Build the image:

```bash
docker build -t zepto-support-assistant .
```

Run the container:

```bash
docker run --rm -p 7860:7860 zepto-support-assistant
```

Open:

```text
http://localhost:7860/docs
```

## Offline Mode

The default mode is offline mock mode.

```text
MOCK_LLM=1
```

In this mode:

* Intent classification uses keywords.
* Retrieval runs using the local ChromaDB collection.
* Policy answers are created from the retrieved context.
* Unrelated questions use a fixed response.
* No external LLM API is required.
