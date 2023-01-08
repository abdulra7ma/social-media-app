from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

PROJECT_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """App configuration class."""

    class Config:
        env_file = PROJECT_DIR.joinpath(".env")

    PROJECT_NAME: str = "Social Media"

    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRES_IN: int = 60
    TOKEN_ALGORITHM = "HS256"
    ACCESS_TOKEN_JWT_SUBJECT = "access"

    EMAILHUNTER_API_KEY: str
    CLEARBIT_API_KEY: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8000",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        """Supports JSON list, actual list, comma-separated list."""

        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ECHO_SQL_STATEMENTS: bool = False
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_URI: Optional[PostgresDsn] = None

    REDIS_HOST: str
    REDIS_PORT: int

    @validator("DB_URI", pre=True)
    def assemble_db_uri(
        cls, field_value: Optional[str], values: Dict[str, Any]
    ) -> Any:
        """Assembles DB_URI from arguments."""

        if isinstance(field_value, str):
            return field_value

        uri = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values["POSTGRES_HOST"],
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
        return uri



settings = Settings()
test_settings = Settings(POSTGRES_DB="test")
