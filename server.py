import os
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

load_dotenv()

# =========================================================
# CONFIG
# =========================================================

APP_NAME = os.getenv("APP_NAME", "Telegram Bot Platform")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("telegram-platform")


# =========================================================
# LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("==========================================")
    logger.info("Starting %s", APP_NAME)
    logger.info("Version: %s", APP_VERSION)
    logger.info("==========================================")

    # Future startup services:
    #
    # - Database
    # - Telegram Bot Manager
    # - Webhook Manager
    # - Scheduler
    # - Plugin Manager
    # - Background Workers

    yield

    logger.info("Shutting down %s", APP_NAME)

    # Future cleanup:
    #
    # - Stop bots
    # - Close database
    # - Stop workers
    # - Close HTTP sessions


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Multi-purpose Telegram Bot Hosting Platform "
        "with Mini App API support."
    ),
    lifespan=lifespan,
)


# =========================================================
# CORS
# =========================================================

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "*"
)

if allowed_origins == "*":
    origins = ["*"]
else:
    origins = [
        origin.strip()
        for origin in allowed_origins.split(",")
        if origin.strip()
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
async def root():

    return {
        "success": True,
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "online",
        "service": "Telegram Bot Platform",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "success": True,
        "status": "healthy",
    }


# =========================================================
# API STATUS
# =========================================================

@app.get("/api/status")
async def api_status():

    return {
        "success": True,
        "server": "online",
        "telegram": "ready",
        "mini_app": "ready",
        "database": "pending",
        "bot_manager": "pending",
        "scheduler": "pending",
    }


# =========================================================
# BOT LIST
# =========================================================

@app.get("/api/bots")
async def bot_list():

    return {
        "success": True,
        "bots": [],
        "message": "Bot modules will be loaded here.",
    }


# =========================================================
# GLOBAL ERROR HANDLER
# =========================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):

    logger.exception(
        "Unhandled error: %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
        },
    )


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
  )
