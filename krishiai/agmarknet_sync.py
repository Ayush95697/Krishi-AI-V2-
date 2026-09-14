import os
import json
import logging
import httpx
import pandas as pd
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func

from krishiai.database import SessionLocal, CropPriceCache

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def seed_prices_if_empty():
    """Seeds the crop_prices_cache table from the static JSON file if the table is empty."""
    db = SessionLocal()
    try:
        count = db.query(CropPriceCache).count()
        if count == 0:
            logger.info("crop_prices_cache is empty. Seeding from crop_price_lookup.json...")
            json_path = os.path.join(MODELS_DIR, "crop_price_lookup.json")
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    lookup_data = json.load(f)
                    
                for crop_name, price in lookup_data.items():
                    db.add(CropPriceCache(
                        crop_name=crop_name,
                        price_per_kg=float(price),
                        last_updated=datetime.utcnow()
                    ))
                db.commit()
                logger.info(f"Successfully seeded {len(lookup_data)} prices.")
            else:
                logger.warning(f"Seed file not found at {json_path}.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
    finally:
        db.close()

def sync_agmarknet_prices():
    """Fetches prices from Agmarknet, aggregates to median price per crop, and upserts to DB."""
    logger.info("Starting Agmarknet price sync...")
    db = SessionLocal()
    try:
        api_key = os.getenv("AGMARKNET_API_KEY", "YOUR_API_KEY_HERE") 
        # Using a public demo key or dummy key if not set. User might need to provide a real one.
        
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        params = {
            "api-key": api_key,
            "format": "json",
            "limit": 10000,
            "offset": 0
        }
        
        response = httpx.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        
        records = data.get("records", [])
        if not records:
            logger.warning("No records returned from Agmarknet API.")
            return
            
        # Create a DataFrame for easier aggregation
        df = pd.DataFrame(records)
        
        if "commodity" not in df.columns or "modal_price" not in df.columns:
            logger.error("API response missing expected columns 'commodity' or 'modal_price'.")
            return
            
        # Clean and convert modal_price
        # modal_price is in Rs./Quintal. We need Rs./Kg (divide by 100)
        df["modal_price"] = pd.to_numeric(df["modal_price"], errors="coerce")
        df = df.dropna(subset=["modal_price"])
        df["price_per_kg"] = df["modal_price"] / 100.0
        
        # Aggregate to median price per commodity
        # Typically Agmarknet provides commodities in uppercase, we'll title-case it
        df["commodity_clean"] = df["commodity"].astype(str).str.strip().str.title()
        
        median_prices = df.groupby("commodity_clean")["price_per_kg"].median().reset_index()
        
        # Upsert into PostgreSQL
        for _, row in median_prices.iterrows():
            crop_name = row["commodity_clean"]
            price_kg = float(row["price_per_kg"])
            
            stmt = insert(CropPriceCache).values(
                crop_name=crop_name,
                price_per_kg=price_kg,
                last_updated=datetime.utcnow()
            )
            
            # ON CONFLICT DO UPDATE
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=['crop_name'],
                set_={
                    'price_per_kg': stmt.excluded.price_per_kg,
                    'last_updated': stmt.excluded.last_updated
                }
            )
            
            db.execute(upsert_stmt)
            
        db.commit()
        logger.info(f"Successfully synced {len(median_prices)} crop prices.")
        
    except Exception as e:
        logger.error(f"Failed to sync Agmarknet prices: {e}")
        db.rollback()
    finally:
        db.close()
