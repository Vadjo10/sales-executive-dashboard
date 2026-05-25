from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class APIConfig:
    base_url: str = field(
        default_factory=lambda: os.getenv("API_BASE_URL", "https://fakestoreapi.com")
    )
    timeout: int = int(os.getenv("API_TIMEOUT", "30"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))


@dataclass
class DatabaseConfig:
    host: str = field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    port: int = int(os.getenv("DB_PORT", "5432"))
    name: str = field(default_factory=lambda: os.getenv("DB_NAME", "sales_db"))
    user: str = field(default_factory=lambda: os.getenv("DB_USER", "sales_admin"))
    password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", ""))

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class PipelineConfig:
    batch_size: int = int(os.getenv("BATCH_SIZE", "100"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_dir: str = field(default_factory=lambda: os.getenv("LOG_DIR", "logs"))


@dataclass
class Settings:
    api: APIConfig = field(default_factory=APIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    root_dir: Path = Path(__file__).resolve().parent.parent


settings = Settings()
