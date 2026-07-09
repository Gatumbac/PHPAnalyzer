from dataclasses import dataclass
import os


def _parse_allowed_origins(raw: str) -> list[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = "PHPAnalyzer API"
    app_version: str = "0.1.0"
    max_source_code_size: int = 262_144
    allowed_origins: list[str] = None

    def __post_init__(self):
        if self.allowed_origins is None:
            raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
            object.__setattr__(self, "allowed_origins", _parse_allowed_origins(raw))


settings = Settings()
