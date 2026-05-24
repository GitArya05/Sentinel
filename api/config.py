import os

class Settings:
    PROJECT_NAME = "Sentinel Engine"
    VERSION = "1.0.0"
    
    # Core ingestion endpoint routed to the specific server version
    BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000-2/api/v1")
    
    # Model Thresholds
    BLOCK_THRESHOLD = 0.8
    
settings = Settings()