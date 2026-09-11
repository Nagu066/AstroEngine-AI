"""
FastAPI Main Application Entrypoint for AstroEngine AI Personalization Context Engine.
"""
import time
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse

from app.config import settings
from app.models.request import PersonalizeRequest, DebugRequest
from app.models.response import PersonalizeResponse, DebugResponse
from app.engine.engine import personalization_engine
from app.upstream.mock_services import (
    get_mock_user,
    get_mock_kundli,
    get_mock_horoscope,
    get_mock_panchang
)
from app.utils.cache import global_cache
from app.utils.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade GenAI Context & Personalization Engine sitting between structured microservices and LLMs."
)


# Middleware for Logging Request Latency & Info
@app.middleware("http")
async def add_timing_and_logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    if not request.url.path.startswith("/static"):
        logger.info(f"HTTP | {request.method} {request.url.path} | Status: {response.status_code} | Duration: {elapsed_ms}ms")
    
    response.headers["X-Response-Time-Ms"] = str(elapsed_ms)
    return response


# Core Endpoint: /personalize
@app.post("/personalize", response_model=PersonalizeResponse, tags=["Context Engine"])
async def personalize_endpoint(request_payload: PersonalizeRequest):
    """
    Personalized AI Endpoint.
    1. Fetches user context from multiple microservices concurrently.
    2. Detects user intent and filters relevant astrological context.
    3. Personalizes language, tone, and max words.
    4. Constructs optimized prompt and invokes LLM.
    5. Returns answer, confidence, and sources used.
    """
    try:
        response = await personalization_engine.personalize_response(
            user_id=request_payload.userId,
            question=request_payload.question
        )
        return response
    except Exception as exc:
        logger.error(f"Error executing /personalize: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


# Debug Endpoint: /debug/personalization
@app.post("/debug/personalization", response_model=DebugResponse, tags=["Context Engine"])
async def debug_personalization_endpoint(request_payload: DebugRequest):
    """
    Debug Endpoint.
    Does NOT invoke the LLM.
    Returns how the Personalization Engine interpreted the request, selected context, and excluded sources.
    """
    try:
        response = await personalization_engine.get_debug_personalization(
            user_id=request_payload.userId,
            question=request_payload.question
        )
        return response
    except Exception as exc:
        logger.error(f"Error executing /debug/personalization: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


# Upstream Service Mock Endpoints
@app.get("/users/{user_id}", tags=["Mock Upstream Services"])
async def mock_user_service(user_id: str):
    return get_mock_user(user_id)


@app.get("/kundli/{user_id}", tags=["Mock Upstream Services"])
async def mock_kundli_service(user_id: str):
    return get_mock_kundli(user_id)


@app.get("/horoscope/{user_id}", tags=["Mock Upstream Services"])
async def mock_horoscope_service(user_id: str):
    return get_mock_horoscope(user_id)


@app.get("/panchang", tags=["Mock Upstream Services"])
async def mock_panchang_service():
    return get_mock_panchang()


# Cache & Health Utilities
@app.get("/cache/stats", tags=["System & Health"])
async def cache_stats_endpoint():
    return await global_cache.get_stats()


@app.get("/health", tags=["System & Health"])
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}


# Interactive Web Dashboard
@app.get("/", response_class=HTMLResponse, tags=["System & Health"])
async def dashboard():
    html_path = Path(__file__).parent / "web" / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>AstroEngine AI is running! Visit /docs for OpenAPI specifications.</h1>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
