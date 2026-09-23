import datetime
import requests
from typing import Optional
from cachetools import TTLCache
from fastapi import HTTPException

# TTLCache with max size 1000 and TTL of 3 hours (10800 seconds)
weather_cache = TTLCache(maxsize=1000, ttl=10800)

def get_weather_advisory(latitude: float, longitude: float, crop: Optional[str] = None) -> dict:
    if not (-90 <= latitude <= 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90.")
    if not (-180 <= longitude <= 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180.")

    rounded_lat = round(latitude, 2)
    rounded_lon = round(longitude, 2)
    today_str = datetime.date.today().isoformat()
    cache_key = f"{rounded_lat}_{rounded_lon}_{today_str}"

    if cache_key in weather_cache:
        data = weather_cache[cache_key]
    else:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"precipitation_probability_max,relative_humidity_2m_max&"
            f"timezone=Asia%2FKolkata&forecast_days=7"
        )
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            weather_cache[cache_key] = data
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Failed to fetch weather data: {str(e)}")

    daily_forecasts = []
    daily = data.get("daily", {})
    
    dates = daily.get("time", [])
    temp_maxes = daily.get("temperature_2m_max", [])
    temp_mins = daily.get("temperature_2m_min", [])
    precip_sums = daily.get("precipitation_sum", [])
    precip_probs = daily.get("precipitation_probability_max", [])
    humidity_maxes = daily.get("relative_humidity_2m_max", [])

    num_days = min(len(dates), 7)

    for i in range(num_days):
        daily_forecasts.append({
            "date": dates[i] if i < len(dates) else "",
            "temp_max": temp_maxes[i] if i < len(temp_maxes) else 0.0,
            "temp_min": temp_mins[i] if i < len(temp_mins) else 0.0,
            "precipitation_mm": precip_sums[i] if i < len(precip_sums) else 0.0,
            "precipitation_probability": precip_probs[i] if i < len(precip_probs) else 0.0,
            "humidity_max": humidity_maxes[i] if i < len(humidity_maxes) else 0.0
        })

    triggered_advisories = []
    
    # 1. Rain Advisories
    # Check next 1-2 days (index 0 and 1)
    rain_warning = False
    max_rain = 0
    warning_type = ""
    for i in range(min(2, len(precip_sums))):
        rain = precip_sums[i]
        if rain >= 64.5:
            rain_warning = True
            if rain > max_rain:
                max_rain = rain
                if rain > 204.4:
                    warning_type = "Extremely Heavy Rain"
                elif rain >= 115.6:
                    warning_type = "Very Heavy Rain"
                else:
                    warning_type = "Heavy Rain"
                    
    if rain_warning:
        triggered_advisories.append({
            "category": "Rainfall",
            "severity": warning_type,
            "message": "Advise postponing irrigation, and advise against applying fertilizer immediately before the rain (nutrient runoff risk)."
        })

    # 2. Heat Wave / Hot Day
    # "Heat Wave: max temp >=40°C ... OR absolute max temp >=45°C regardless of departure... use ONLY the absolute threshold (>=45°C) and do not fabricate a departure-based trigger."
    heat_wave_triggered = False
    for t_max in temp_maxes:
        if t_max >= 45.0:
            heat_wave_triggered = True
            break
            
    if heat_wave_triggered:
        triggered_advisories.append({
            "category": "Temperature",
            "severity": "Heat Wave",
            "message": "Advise adjusting irrigation timing to early morning or evening, and general crop heat-stress protection guidance."
        })

    # 3. Cold Wave / Ground Frost
    cold_wave_triggered = False
    ground_frost_triggered = False
    for t_min in temp_mins:
        if t_min <= 4.0:
            cold_wave_triggered = True
        if t_min <= 0.5:
            ground_frost_triggered = True

    if ground_frost_triggered:
        triggered_advisories.append({
            "category": "Temperature",
            "severity": "Ground Frost",
            "message": "Advise frost protection measures."
        })
    elif cold_wave_triggered:
        triggered_advisories.append({
            "category": "Temperature",
            "severity": "Cold Wave",
            "message": "Advise frost protection measures."
        })

    # 4. High relative humidity (>85%) sustained for 2+ consecutive forecast days
    consecutive_high_humidity = 0
    humidity_alert = False
    for h_max in humidity_maxes:
        if h_max > 85:
            consecutive_high_humidity += 1
            if consecutive_high_humidity >= 2:
                humidity_alert = True
                break
        else:
            consecutive_high_humidity = 0

    if humidity_alert:
        msg = f"Increased risk of fungal disease conditions."
        if crop:
            msg = f"Increased risk of fungal disease conditions for {crop}."
        triggered_advisories.append({
            "category": "Humidity",
            "severity": "High Humidity",
            "message": msg
        })

    # 5. No rain forecast for the full 7-day window
    total_rain = sum(precip_sums)
    if total_rain == 0.0 and len(precip_sums) > 0:
        triggered_advisories.append({
            "category": "Rainfall",
            "severity": "No Rain",
            "message": "No rain forecast for the full 7-day window. General irrigation-planning reminder."
        })

    disclaimer = "This forecast reflects the nearest available weather station or grid point, not necessarily the exact microclimate of your specific field. Treat this as a planning aid, not a precise prediction."
    location_str = f"Lat: {latitude}, Lon: {longitude} (nearest available forecast point, not exact field location)"
    
    return {
        "location": location_str,
        "daily_forecast": daily_forecasts,
        "triggered_advisories": triggered_advisories,
        "disclaimer": disclaimer
    }
