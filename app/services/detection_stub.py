import time

def detect_stub(asset_id: str):
    t0 = time.time()
    # stub response: pretend there's one "person"
    detections = [
        {"label": "person", "score": 0.9, "bbox": [0.1, 0.1, 0.4, 0.6]}
    ]
    latency_ms = int((time.time() - t0) * 1000)
    return {"asset_id": asset_id, "detections": detections, "model": "stub", "latency_ms": latency_ms}