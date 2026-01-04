# Vision Agent Platform

A production-minded system that converts **visual inputs (images/videos)** into **structured perception outputs**, and then uses **LLM-based agents** to answer questions with **grounded evidence**.

This project is intentionally built in phases:
- Start simple (Week 1): stable APIs, storage, DB, stubs
- Gradually scale: real CV inference, events, memory, multi-agent reasoning, async workers, observability

---

## Why this project

Most AI demos jump straight to models.  
This project focuses on **building AI systems**:

- Clean API contracts
- Swappable implementations (stub → real models)
- Evidence-grounded GenAI
- Scalability and debuggability from day one

---

## Current Status (Week 1)

✅ Upload image/video and receive an `asset_id`  
✅ Call `/detect` to get stub detection output  
✅ Call `/ask` to get stub agent response  
✅ Runs fully via Docker  

> The goal of Week 1 is **correct structure**, not intelligence yet.

---

## Tech Stack (Week 1)

- FastAPI (API server)
- SQLite + SQLAlchemy (async metadata storage)
- Docker + Docker Compose
- pytest (testing)
- loguru (structured JSON logging)

---

## Repository Structure

```
vision-agent-platform/
├── app/
│   ├── main.py                # FastAPI bootstrap
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   ├── config.py          # Environment & settings
│   │   └── logging.py         # Structured logging
│   ├── services/
│   │   ├── storage.py         # File persistence
│   │   ├── detection_stub.py  # Stub CV model (Week 1)
│   │   └── llm_stub.py        # Stub agent (Week 1)
│   └── db/
│       ├── models.py          # DB models
│       └── session.py         # Async DB session
├── tests/
│   └── test_health.py
├── data/
│   └── uploads/               # Uploaded assets (mounted volume)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## API Contracts

### Health Check

**GET /health**

Response:
```json
{ "ok": true }
```

---

### Upload Asset

**POST /ingest** (multipart/form-data)

Response:
```json
{
  "asset_id": "uuid",
  "asset_type": "video_or_image",
  "path": "data/uploads/example.mp4",
  "created_at": "2026-01-04T10:00:00Z"
}
```

---

### Run Detection (Stub)

**POST /detect**

Request:
```json
{ "asset_id": "uuid" }
```

Response:
```json
{
  "asset_id": "uuid",
  "detections": [
    { "label": "person", "score": 0.9, "bbox": [0.1, 0.1, 0.4, 0.6] }
  ],
  "model": "stub",
  "latency_ms": 1
}
```

---

### Ask a Question (Stub Agent)

**POST /ask**

Request:
```json
{
  "asset_id": "uuid",
  "question": "What is happening in the scene?"
}
```

Response:
```json
{
  "answer": "(stub) You asked: 'What is happening in the scene?' about asset <id>.",
  "evidence": [],
  "mode": "stub"
}
```

---

## Running the Project

### Build and start

```bash
docker compose up --build
```

API will be available at: **http://localhost:8000**

---

## Example Usage

### Upload an image or video:

```bash
curl -F "file=@sample.jpg" http://localhost:8000/ingest
```

### Run detection:

```bash
curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"asset_id":"<ASSET_ID>"}'
```

### Ask a question:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"asset_id":"<ASSET_ID>","question":"summarize the scene"}'
```

---

## Running Tests

```bash
pytest -q
```

---

## Design Principles

- **Stable API contracts** – clients never break
- **Swappable implementations** – stubs → real CV/LLMs
- **Immutable artifacts** – detections/events are append-only
- **Evidence-first answers** – reduce hallucinations
- **Production-first mindset** – logging, structure, scalability

---

## Roadmap

### Phase 1: Real Computer Vision
- Replace detection stub with YOLO/DETR
- Persist detection outputs

### Phase 2: Event Extraction
- Convert detections → events (enter/exit, loitering, count changes)
- Build event timelines

### Phase 3: Memory & Grounding
- Short-term and long-term memory
- Vector search over events
- Enforce evidence-backed answers

### Phase 4: Multi-Agent Reasoning
- Reasoning, planner, critic agents
- Tool calling (OCR, crop, redetect)

### Phase 5: Scaling & Reliability
- Async workers + queues
- Observability and evaluation harness
- Cost and latency controls

---

## License

MIT

---

## What's Next

Before moving to Week 2, we should:
1. Refactor stubs behind **service interfaces**
2. Add **request IDs** to logs
3. Add a simple **architecture diagram**

Next steps options:
- Cleanly refactor Week 1 code (no behavior change)
- Or start **Week 2: real YOLO inference** step-by-step
