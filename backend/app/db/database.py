from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Note: connection test placeholder. We do not connect automatically to allow for failure-free imports.
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    engine = None
    SessionLocal = None
