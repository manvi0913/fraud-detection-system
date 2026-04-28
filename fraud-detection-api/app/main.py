from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.transactions import fraud_router, transaction_router
from app.core.config import settings
from app.core.database import Base, engine

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Real-time fraud detection API for financial transaction monitoring.",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(transaction_router, prefix=settings.api_v1_prefix)
app.include_router(fraud_router, prefix=settings.api_v1_prefix)
app.include_router(dashboard_router)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", tags=["Root"])
def read_root():
    return {
        "project": settings.app_name,
        "message": "Fraud detection backend is running.",
        "docs": "/docs",
        "admin_dashboard": "/admin/dashboard",
    }
