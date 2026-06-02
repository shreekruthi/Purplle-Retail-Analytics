from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.database.tables import Base
from app.database.database import engine

from app.routers.health import router as health_router
from app.routers.events import router as events_router

from app.routers.metrics import (
    router as metrics_router
)
from app.routers.funnel import (
    router as funnel_router
)

from app.routers.heatmap import (
    router as heatmap_router
)

from app.routers.anomalies import (
    router as anomalies_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(events_router)

app.include_router(metrics_router)

app.include_router(funnel_router)
app.include_router(
    heatmap_router
)

app.include_router(
    anomalies_router
)

@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }