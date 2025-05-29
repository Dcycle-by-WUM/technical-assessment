import os
from typing import Dict, List, Optional, Union

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "recommendation-engine"
    
    # Database configurations
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "recommendation_engine")
    
    # Redis configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    
    # Algorithm settings
    DEFAULT_RECOMMENDATION_LIMIT: int = 10
    RECOMMENDATION_CACHE_TTL: int = 3600  # 1 hour
    
    # Service scaling parameters
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "100"))
    
    # Feature flags
    ENABLE_REAL_TIME_RECOMMENDATIONS: bool = os.getenv("ENABLE_REAL_TIME_RECOMMENDATIONS", "True").lower() == "true"
    ENABLE_PERSONALIZATION: bool = os.getenv("ENABLE_PERSONALIZATION", "True").lower() == "true"
    ENABLE_AB_TESTING: bool = os.getenv("ENABLE_AB_TESTING", "False").lower() == "true"
    
    # Monitoring
    ENABLE_PROMETHEUS: bool = os.getenv("ENABLE_PROMETHEUS", "True").lower() == "true"
    ENABLE_OPENTELEMETRY: bool = os.getenv("ENABLE_OPENTELEMETRY", "False").lower() == "true"
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    
    # Algorithm versions
    ALGORITHM_VERSION: str = os.getenv("ALGORITHM_VERSION", "v1")
    AVAILABLE_ALGORITHM_VERSIONS: List[str] = ["v1", "v2-beta"]
    
    @validator("AVAILABLE_ALGORITHM_VERSIONS", pre=True)
    def check_algorithm_version(cls, v, values):
        if values.get("ALGORITHM_VERSION") not in v:
            raise ValueError(f"ALGORITHM_VERSION must be one of {v}")
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

