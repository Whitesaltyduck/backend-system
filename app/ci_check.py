import os

REQUIRED_ENV_VARS = [
    "SECRET_KEY",
    "DATABASE_URL"
]

missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing:
    raise RuntimeError(
        f"CI configuration contract violated. Missing env vars: {missing}"
    )
