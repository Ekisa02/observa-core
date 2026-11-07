from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.predictor import Predictor
from app.utils.logging import setup_logging

setup_logging()

app = FastAPI(title="Observa Core", version="0.1.0")

# Initialize predictor early (will create model file if missing)
predictor = Predictor()

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    # Warm up predictor on startup
    predictor.warmup()


@app.get("/")
async def root():
    return {"service": "observa-core", "status": "ok"}
