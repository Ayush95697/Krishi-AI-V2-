# KrishiAI+

An integrated, intelligent agricultural decision-support system for Indian farmers.

## Vision
To provide actionable, hyper-local, and scientifically grounded agricultural advisory by combining machine learning, robust data retrieval (RAG), and localized context (weather, soil, and crop).

## Current Status
Architecture and repository foundation phase.

## Planned Features
- Crop Recommendation
- Crop Disease Detection
- RAG-based Agricultural Chatbot
- Weather Intelligence and Weather-aware Advisory
- Soil Information and Interpretation
- Financial Analysis
- Smart Notifications
- Farmer Dashboard
- User Accounts and History

## Architecture
The system employs a multi-tier layered architecture:
- **Frontend (React)**: User Interface.
- **Backend (FastAPI)**: Application and decision logic gateway.
- **Decision/Advisory Layer**: Aggregates models and context.
- **ML Services**: Crop and Disease inference.
- **RAG Services**: Verified agricultural knowledge base.
- **Database (MySQL)**: Persistent state and history.

## Technology Stack
- **Frontend**: React, TypeScript, Tailwind CSS, Vite
- **Backend**: Python, FastAPI, Pydantic, SQLAlchemy, Alembic
- **Database**: MySQL (Production: Azure Database for MySQL - Flexible Server)
- **ML & CV**: scikit-learn, PyTorch, OpenCV, Pillow
- **Infrastructure**: Docker, Azure

## Repository Structure
- `frontend/`: React single-page application.
- `backend/`: FastAPI application and advisory engine.
- `ml/`: Model training and evaluation code.
- `rag/`: Knowledge ingestion and retrieval pipelines.
- `data/`: Placeholder for datasets (not committed).
- `infrastructure/`: Docker and Azure deployment configurations.
- `docs/`: System documentation and architectural decisions.

## Development
To be configured using Docker Compose for local environments.

## Deployment
Production deployment targets Microsoft Azure and Azure Database for MySQL – Flexible Server.

## Scientific Integrity
- Weather Uncertainty: Acknowledging that weather forecasts do not represent exact farm microclimates.
- Soil Spatial Variability: Soil sample data provides guidance, not absolute sub-meter truth.
- ML & Financial Uncertainty: Predictions and estimates are advisory, not guarantees.
- RAG Grounding: Responses must be grounded in verified agricultural sources (e.g., ICAR, IMD).
