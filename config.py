import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # App
    APP_NAME = os.getenv(
        "APP_NAME",
        "Telegram Bot Platform"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    # Server
    PORT = int(
        os.getenv("PORT", "8000")
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )

    TELEGRAM_WEBHOOK_SECRET = os.getenv(
        "TELEGRAM_WEBHOOK_SECRET",
        ""
    )

    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./telegram.db"
    )

    # CORS
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "*"
    )

    # Mini App
    MINI_APP_URL = os.getenv(
        "MINI_APP_URL",
        ""
    )

    # Environment
    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "production"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "false"
    ).lower() == "true"


settings = Settings()
