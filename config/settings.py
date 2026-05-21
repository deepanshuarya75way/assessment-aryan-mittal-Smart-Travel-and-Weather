"""
Application configuration loaded from environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Load .env file
_ROOT = Path(__file__).resolve().parents[1]

for candidate in (_ROOT, _ROOT.parent):
    load_dotenv(candidate / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    groq_api_key: str
    weather_api_key: str

    # Default model
    groq_model: str = "llama-3.1-8b-instant"

    weather_timeout_s: float = 20.0
    http_max_retries: int = 3


def get_settings() -> Settings:

    groq = (os.getenv("GROQ_API_KEY") or "").strip()
    weather = (os.getenv("WEATHER_API_KEY") or "").strip()

    model = (
        os.getenv("GROQ_MODEL")
        or "llama-3.1-8b-instant"
    ).strip()

    if not groq:
        raise ValueError(
            "Missing GROQ_API_KEY in .env"
        )

    if not weather:
        raise ValueError(
            "Missing WEATHER_API_KEY in .env"
        )

    return Settings(
        groq_api_key=groq,
        weather_api_key=weather,
        groq_model=model,
        weather_timeout_s=20.0,
        http_max_retries=3
    )