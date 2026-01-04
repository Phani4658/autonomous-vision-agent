# Autonomous Vision Agent System

## Run
docker compose up --build

## Test
pytest -q

## Example
curl -F "file=@sample.jpg" http://localhost:8000/ingest
curl -X POST http://localhost:8000/detect -H "Content-Type: application/json" -d '{"asset_id":"..."}'
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"asset_id":"...","question":"what is happening?"}'