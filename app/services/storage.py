from pathlib import Path
from app.core.config import settings

def save_upload(file_bytes: bytes, filename: str) -> str:
    safe_name = filename.replace("/", "_")
    path = Path(settings.upload_dir) / safe_name
    path.write_bytes(file_bytes)
    return str(path)