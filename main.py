from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import setup_logging
from app.db.session import engine
from app.db.models import Base

logger = setup_logging()

app = FastAPI(title="Vision Agent Platform")
app.include_router(router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("startup complete")