# api/config.py
import os

class Settings:
    PROJECT_NAME = "Sentinel Engine"
    VERSION = "1.0.0"
    
    BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000-2/api/v1")
    
    # Lowered from 0.8 to catch boundary probabilities
    BLOCK_THRESHOLD = 0.5 
    
settings = Settings()