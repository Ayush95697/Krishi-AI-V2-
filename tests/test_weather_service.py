import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from krishiai.main import app

client = TestClient(app)

@pytest.fixture
def mock_open_meteo():
    with patch('krishiai.weather_service.requests.get') as mock_get:
        yield mock_get

def test_weather_advisory_heavy_rain(mock_open_meteo):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06", "2024-01-07"],
            "temperature_2m_max": [30.0] * 7,
            "temperature_2m_min": [20.0] * 7,
            "precipitation_sum": [100.0, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # 100mm on day 1 is Heavy Rain
            "precipitation_probability_max": [80] * 7,
            "relative_humidity_2m_max": [60] * 7
        }
    }
    mock_open_meteo.return_value = mock_response

    response = client.post("/weather-advisory", json={"latitude": 20.0, "longitude": 80.0})
    assert response.status_code == 200
    data = response.json()
    
    assert "location" in data
    assert "disclaimer" in data
    assert "nearest available weather station" in data["disclaimer"]
    
    advisories = data["triggered_advisories"]
    assert any(a["category"] == "Rainfall" and a["severity"] == "Heavy Rain" for a in advisories)

def test_weather_advisory_heat_wave_absolute(mock_open_meteo):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01"] * 7,
            "temperature_2m_max": [45.5, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0],  # 45.5 triggers Heat Wave
            "temperature_2m_min": [25.0] * 7,
            "precipitation_sum": [5.0] * 7,
            "precipitation_probability_max": [10] * 7,
            "relative_humidity_2m_max": [50] * 7
        }
    }
    mock_open_meteo.return_value = mock_response

    response = client.post("/weather-advisory", json={"latitude": 20.1, "longitude": 80.1})
    assert response.status_code == 200
    data = response.json()
    
    advisories = data["triggered_advisories"]
    assert any(a["category"] == "Temperature" and a["severity"] == "Heat Wave" for a in advisories)

def test_weather_advisory_mild_unremarkable(mock_open_meteo):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01"] * 7,
            "temperature_2m_max": [30.0] * 7,
            "temperature_2m_min": [20.0] * 7,
            "precipitation_sum": [10.0] * 7,  # Not heavy, not 0
            "precipitation_probability_max": [20] * 7,
            "relative_humidity_2m_max": [60] * 7
        }
    }
    mock_open_meteo.return_value = mock_response

    response = client.post("/weather-advisory", json={"latitude": 20.2, "longitude": 80.2})
    assert response.status_code == 200
    data = response.json()
    
    advisories = data["triggered_advisories"]
    assert len(advisories) == 0  # No advisories
    assert "disclaimer" in data  # Disclaimer is still present

def test_weather_advisory_invalid_latitude():
    response = client.post("/weather-advisory", json={"latitude": 200.0, "longitude": 80.0})
    assert response.status_code == 400
    
def test_weather_advisory_disclaimer_always_present(mock_open_meteo):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2024-01-01"] * 7,
            "temperature_2m_max": [30.0] * 7,
            "temperature_2m_min": [20.0] * 7,
            "precipitation_sum": [10.0] * 7,
            "precipitation_probability_max": [20] * 7,
            "relative_humidity_2m_max": [60] * 7
        }
    }
    mock_open_meteo.return_value = mock_response

    response = client.post("/weather-advisory", json={"latitude": 20.3, "longitude": 80.3})
    data = response.json()
    assert "disclaimer" in data
    assert len(data["disclaimer"]) > 0
