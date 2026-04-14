from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config.settings import settings
from db import create_tables
from routes.health import router as health_router
from routes.auth import router as auth_router
from routes.identity import router as identity_router
from routes.risk import router as risk_router
from routes.transaction import router as transaction_router
from utils.observability import configure_logging, metrics_response, request_metrics_middleware


limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
app = FastAPI(title=settings.app_name)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_metrics_middleware)


@app.on_event("startup")
def on_startup():
    configure_logging(settings.log_level)
    if not settings.production_mode:
        create_tables()


@app.get("/metrics")
async def metrics(token: str = ""):
    if settings.metrics_token and token != settings.metrics_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await metrics_response()


app.include_router(health_router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(identity_router, prefix="/api/v1")
app.include_router(transaction_router, prefix="/api/v1")
app.include_router(risk_router, prefix="/api/v1")
