from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "placeholder_secret_key"
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "krishiai"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
