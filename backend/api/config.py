
import os

from dotenv import load_dotenv

load_dotenv()


def get_allowed_origins() -> list[str]:
    raw_origins = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )

    origins = [
        origin.strip().rstrip("/")
        for origin in raw_origins.split(",")
        if origin.strip()
    ]

    if "*" in origins:
        raise ValueError(
            "Wildcard CORS origin is not allowed."
        )

    return origins
