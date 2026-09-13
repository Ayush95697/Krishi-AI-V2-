from pydantic import BaseModel
from typing import List, Optional

class CropRecommendationRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class AlternativeCrop(BaseModel):
    crop: str
    probability: float

class CropRecommendationResponse(BaseModel):
    recommended_crop: str
    confidence: float
    top_3_alternatives: List[AlternativeCrop]

class YieldPredictionRequest(BaseModel):
    crop: str
    state: str
    season: str
    crop_year: int
    annual_rainfall: float
    fertilizer: float
    pesticide: float
    area: float

class YieldPredictionResponse(BaseModel):
    predicted_yield_per_unit_area: float
    estimated_production_kg: float
    price_per_kg: Optional[float]
    estimated_revenue: Optional[float]
    note: Optional[str]

class HealthResponse(BaseModel):
    status: str
    crops_supported: int
    crops_priced: int
