from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "vision-agent-platform"
    upload_dir: str = "data/uploads"
    models_dir: str = "data/models"
    output_dir: str = "data/outputs"
    database_url: str = "sqlite+aiosqlite:///./data/app.db"

settings = Settings()
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path("data").mkdir(parents=True, exist_ok=True)