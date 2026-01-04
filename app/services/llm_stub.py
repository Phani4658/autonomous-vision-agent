def answer_stub(asset_id: str, question: str):
    return {
        "answer": f"(stub) You asked: '{question}' about asset {asset_id}.",
        "evidence": [],
        "mode": "stub",
    }