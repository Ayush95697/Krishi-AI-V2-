from pydantic import BaseModel
from typing import List, Optional, Dict

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

class SoilInterpretationRequest(BaseModel):
    n_kg_ha: float
    p_kg_ha: float
    k_kg_ha: float
    oc_percent: float
    ph: float
    ec_dsm: Optional[float] = None
    s_ppm: Optional[float] = None
    b_ppm: Optional[float] = None
    zn_ppm: Optional[float] = None
    fe_ppm: Optional[float] = None
    mn_ppm: Optional[float] = None
    cu_ppm: Optional[float] = None

class ParameterRatingSchema(BaseModel):
    parameter: str
    value: float
    unit: str
    rating: str
    source: str
    note: Optional[str] = None

class SoilInterpretationResponse(BaseModel):
    ratings: Dict[str, ParameterRatingSchema]
    concerns: List[str]
    disclaimer: str
