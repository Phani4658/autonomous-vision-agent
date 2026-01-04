from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Asset
from app.services.storage import save_upload
from app.services.detection_stub import detect_stub
from app.services.llm_stub import answer_stub

router = APIRouter()

@router.get("/health")
async def health():
    return {"ok": True}

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    local_path = save_upload(content, file.filename)

    async with AsyncSessionLocal() as session:
        asset = Asset(filename=file.filename, content_type=file.content_type or "application/octet-stream", local_path=local_path)
        session.add(asset)
        await session.commit()
        await session.refresh(asset)

    return {"asset_id": asset.id, "asset_type": "video_or_image", "path": asset.local_path, "created_at": asset.created_at}

@router.post("/detect")
async def detect(payload: dict):
    asset_id = payload.get("asset_id")
    if not asset_id:
        raise HTTPException(status_code=400, detail="asset_id required")

    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Asset).where(Asset.id == asset_id))
        asset = res.scalar_one_or_none()
        if not asset:
            raise HTTPException(status_code=404, detail="asset not found")

    return detect_stub(asset_id)

@router.post("/ask")
async def ask(payload: dict):
    asset_id = payload.get("asset_id")
    question = payload.get("question")
    if not asset_id or not question:
        raise HTTPException(status_code=400, detail="asset_id and question required")

    return answer_stub(asset_id, question)