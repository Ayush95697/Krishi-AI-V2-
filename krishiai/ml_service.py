import os
import numpy as np
import pandas as pd
import joblib
from fastapi import HTTPException
from typing import Dict, Any

from krishiai.database import SessionLocal, CropPriceCache

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

# Define global variables for the models
crop_model = None
crop_label_encoder = None
yield_model = None
yield_le_crop = None
yield_le_state = None
yield_le_season = None

def load_models():
    global crop_model, crop_label_encoder, yield_model
    global yield_le_crop, yield_le_state, yield_le_season

    crop_model = joblib.load(os.path.join(MODELS_DIR, "crop_recommendation_RandomForest.joblib"))
    crop_label_encoder = joblib.load(os.path.join(MODELS_DIR, "crop_recommendation_label_encoder.joblib"))

    yield_model = joblib.load(os.path.join(MODELS_DIR, "yield_prediction_RandomForestRegressor.joblib"))
    yield_le_crop = joblib.load(os.path.join(MODELS_DIR, "yield_le_crop.joblib"))
    yield_le_state = joblib.load(os.path.join(MODELS_DIR, "yield_le_state.joblib"))
    yield_le_season = joblib.load(os.path.join(MODELS_DIR, "yield_le_season.joblib"))

def recommend_crop(input_data: Dict[str, float]) -> Dict[str, Any]:
    # Ensure pandas DataFrame is used to avoid silent feature-name warnings
    # Expected columns: ['N','P','K','temperature','humidity','ph','rainfall']
    df = pd.DataFrame([input_data])
    
    probabilities = crop_model.predict_proba(df)[0]
    
    # Get top 3 indices sorted by probability descending
    top_indices = np.argsort(probabilities)[::-1]
    
    top_3_indices = top_indices[:3]
    top_3_probs = probabilities[top_3_indices]
    
    # Inverse transform to get original labels
    top_3_labels = crop_label_encoder.inverse_transform(top_3_indices)
    
    recommended_crop = top_3_labels[0]
    confidence = top_3_probs[0]
    
    alternatives = []
    for label, prob in zip(top_3_labels, top_3_probs):
        alternatives.append({
            "crop": label,
            "probability": float(prob)
        })
        
    return {
        "recommended_crop": recommended_crop,
        "confidence": float(confidence),
        "top_3_alternatives": alternatives
    }

def estimate_yield_and_revenue(input_data: Dict[str, Any]) -> Dict[str, Any]:
    crop = input_data["crop"]
    state = input_data["state"]
    season = input_data["season"]
    
    # Encode categorical features
    try:
        encoded_crop = yield_le_crop.transform([crop])[0]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unrecognized crop value: {crop}")
        
    try:
        encoded_state = yield_le_state.transform([state])[0]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unrecognized state value: {state}")
        
    try:
        encoded_season = yield_le_season.transform([season])[0]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unrecognized season value: {season}")

    
    if input_data["area"] <= 0:
        raise HTTPException(status_code=400, detail="Area must be greater than zero")

    df = pd.DataFrame([{
        "Crop_enc": encoded_crop,
        "State_enc": encoded_state,
        "Season_enc": encoded_season,
        "Crop_Year": input_data["crop_year"],
        "Annual_Rainfall": input_data["annual_rainfall"],
        "Fertilizer": input_data["fertilizer"],
        "Pesticide": input_data["pesticide"],
        "Area": input_data["area"],
    }])

    predicted_log_yield = yield_model.predict(df)[0]
    predicted_yield = np.expm1(predicted_log_yield)
    
    estimated_production_kg = predicted_yield * input_data["area"]
    
    # Fetch price from DB
    db = SessionLocal()
    try:
        # DB lookup (case insensitive match on crop_name)
        from sqlalchemy import func
        cache_entry = db.query(CropPriceCache).filter(
            func.lower(CropPriceCache.crop_name) == crop.lower()
        ).first()
        
        if cache_entry:
            price_per_kg = cache_entry.price_per_kg
            estimated_revenue = estimated_production_kg * price_per_kg
            note = "Success"
        else:
            price_per_kg = None
            estimated_revenue = None
            note = "No current market price available for this crop."
    finally:
        db.close()
        
    return {
        "predicted_yield_per_unit_area": float(predicted_yield),
        "estimated_production_kg": float(estimated_production_kg),
        "price_per_kg": float(price_per_kg) if price_per_kg is not None else None,
        "estimated_revenue": float(estimated_revenue) if estimated_revenue is not None else None,
        "note": note
    }
