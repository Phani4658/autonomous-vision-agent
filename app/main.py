from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import setup_logging
from app.core.middleware import RequestIDMiddleware
from app.db.session import engine
from app.db.models import Base

logger = setup_logging()

app = FastAPI(title="Vision Agent Platform")
app.add_middleware(RequestIDMiddleware)
app.include_router(router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("startup complete")