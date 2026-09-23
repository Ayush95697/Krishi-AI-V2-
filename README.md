# KrishiAI+

An integrated, intelligent agricultural decision-support system for Indian farmers.

## Vision
To provide actionable, hyper-local, and scientifically grounded agricultural advisory by combining machine learning, robust data retrieval (RAG), and localized context (weather, soil, and crop).

## Current Status
The backend services are actively being developed. 
The core decision-support endpoints for crop recommendation, financial analysis, soil health interpretation, and weather advisory are fully operational via the FastAPI backend (`krishiai/`).

## Features

### 🚀 Implemented Features
- **Crop Recommendation Engine**: Uses a Random Forest ML model to recommend the best crop based on soil properties (Nitrogen, Phosphorus, Potassium, pH) and climate (temperature, humidity, rainfall). Also returns the top 3 alternative crops with confidence scores.
- **Yield & Revenue Estimation**: Analyzes farm area, fertilizer/pesticide usage, and rainfall to predict expected yield using Random Forest Regression. It fetches real-time market prices from AGMARKNET via daily automated syncs to estimate potential revenue.
- **Soil Health Interpretation**: A strict rule-based engine interpreting raw N, P, K, OC, and pH metrics against the Government of India (GoI) 2011 Methods Manual standards, providing farmer-friendly ratings without hallucinating values.
- **Weather Advisory Module**: Integrates with Open-Meteo for 7-day hyper-local forecasts and applies strict Indian Meteorological Department (IMD) standard rules to trigger warnings (Heavy Rain, Heat Wave, Cold Wave, Ground Frost). Caches results efficiently and transparently notes microclimate caveats.

### ⏳ Planned Features
- [NOT IMPLEMENTED] **Crop Disease Detection**: Computer vision model to identify plant diseases from uploaded images.
- [NOT IMPLEMENTED] **RAG-based Agricultural Chatbot**: Knowledge retrieval system backed by ICAR/IMD documents.
- [NOT IMPLEMENTED] **Smart Notifications**: Push alerts based on severe weather or market price fluctuations.
- [NOT IMPLEMENTED] **Farmer Dashboard**: Interactive visualization of farm health and financials.
- [NOT IMPLEMENTED] **User Accounts and History**: Persistent profiles for tracking soil tests and yields over time.

## Architecture
The system employs a multi-tier layered architecture:
- **Frontend (React)**: User Interface.
- **Backend (FastAPI)**: Application and decision logic gateway.
- **Decision/Advisory Layer**: Aggregates models and context.
- **ML Services**: Crop and Disease inference.
- **RAG Services**: Verified agricultural knowledge base.
- **Database (MySQL)**: Persistent state, pricing caches, and history.

## Technology Stack
- **Frontend**: React, TypeScript, Tailwind CSS, Vite
- **Backend**: Python, FastAPI, Pydantic, SQLAlchemy, Alembic, apscheduler
- **Database**: MySQL (Production: Azure Database for MySQL - Flexible Server)
- **ML & CV**: scikit-learn, PyTorch, OpenCV, Pillow
- **Infrastructure**: Docker, Azure

## Repository Structure
- `krishiai/`: FastAPI application and backend advisory engine.
- `frontend/`: React single-page application.
- `models/`: Pre-trained ML models and encoders.
- `ml/`: Model training and evaluation code.
- `rag/`: Knowledge ingestion and retrieval pipelines.
- `tests/`: Pytest test suites for validating backend logic.
- `backend/`: Reserved for future use / legacy.
- `data/`: Placeholder for datasets (not committed).
- `infrastructure/`: Docker and Azure deployment configurations.
- `docs/`: System documentation and architectural decisions.

## Development Setup
The FastAPI application can be run locally using Uvicorn. A `run_app.bat` script is included for quick startups. It requires Python 3.10+ and uses `pip` for dependency management (`requirements_krishiai.txt`).
*(Full Docker Compose configuration for local environments is planned)*

## Scientific Integrity Principles
The architecture of KrishiAI+ strictly enforces the following rules to prevent AI hallucination:
- **Weather Uncertainty**: Acknowledging that weather forecasts do not represent exact farm microclimates. Caveats are explicitly returned in the API responses.
- **Soil Spatial Variability**: Soil sample data provides guidance, not absolute sub-meter truth. Ratings never infer unavailable parameters based on GPS.
- **ML & Financial Uncertainty**: Predictions and estimates are advisory, not guarantees. Market prices rely on official AGMARKNET data syncs.
- **RAG Grounding**: Responses must be grounded in verified agricultural sources (e.g., ICAR, IMD).
