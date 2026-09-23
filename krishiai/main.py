import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from krishiai.database import init_db, SessionLocal, CropPriceCache
from krishiai.schemas import (
    CropRecommendationRequest, CropRecommendationResponse,
    YieldPredictionRequest, YieldPredictionResponse, HealthResponse,
    SoilInterpretationRequest, SoilInterpretationResponse,
    WeatherAdvisoryRequest, WeatherAdvisoryResponse
)
from krishiai.ml_service import load_models, recommend_crop, estimate_yield_and_revenue
from krishiai.soil_service import interpret_soil
from krishiai.weather_service import get_weather_advisory
from krishiai.agmarknet_sync import sync_agmarknet_prices, seed_prices_if_empty

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Note: This service uses a BackgroundScheduler within the FastAPI process.
# IMPORTANT: This service must be run with a single worker (e.g., `uvicorn main:app --workers 1`).
# Running multiple workers will cause the scheduler to duplicate jobs across each worker process.

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing database...")
    init_db()
    
    logger.info("Seeding prices if empty...")
    seed_prices_if_empty()
    
    logger.info("Loading ML models...")
    load_models()
    
    logger.info("Starting APScheduler for daily price sync...")
    # Schedule the sync job to run daily at 2:00 AM
    scheduler.add_job(
        sync_agmarknet_prices,
        CronTrigger(hour=2, minute=0),
        id="daily_agmarknet_sync",
        replace_existing=True
    )
    scheduler.start()
    
    yield
    
    # Shutdown actions
    logger.info("Shutting down APScheduler...")
    scheduler.shutdown()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="KrishiAI+ Backend API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend-crop", response_model=CropRecommendationResponse)
def recommend_crop_endpoint(request: CropRecommendationRequest):
    return recommend_crop(request.dict())

@app.post("/estimate-yield-and-revenue", response_model=YieldPredictionResponse)
def estimate_yield_and_revenue_endpoint(request: YieldPredictionRequest):
    return estimate_yield_and_revenue(request.dict())

@app.post("/interpret-soil", response_model=SoilInterpretationResponse)
def interpret_soil_endpoint(request: SoilInterpretationRequest):
    # Using request.dict() for consistency with other endpoints (even if deprecated in Pydantic v2)
    return interpret_soil(**request.dict())

@app.post("/weather-advisory", response_model=WeatherAdvisoryResponse)
def weather_advisory_endpoint(request: WeatherAdvisoryRequest):
    return get_weather_advisory(**request.dict())

@app.get("/health", response_model=HealthResponse)
def health_check():
    db = SessionLocal()
    try:
        crops_priced = db.query(CropPriceCache).count()
    except Exception as e:
        logger.error(f"Healthcheck DB error: {e}")
        crops_priced = 0
    finally:
        db.close()
        
    # We can hardcode crops_supported based on the label encoder's classes,
    # or just assume the length of crop_label_encoder.classes_
    from krishiai.ml_service import crop_label_encoder
    
    if crop_label_encoder and hasattr(crop_label_encoder, 'classes_'):
        crops_supported = len(crop_label_encoder.classes_)
    else:
        crops_supported = 22 # default fallback if not loaded or accessible
        
    return {
        "status": "ok",
        "crops_supported": crops_supported,
        "crops_priced": crops_priced
    }
