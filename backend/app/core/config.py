from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Csyrus Approval Workflow"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    
    # Auth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    FRONTEND_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

settings = Settings()