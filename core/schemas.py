# core/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float = Field(..., gt=0, description="Transaction amount in INR")
    merchant_category: str
    location: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    stream_id: int
    
    # We will populate this later in Segment 4
    risk_score: Optional[float] = None 
    is_blocked: Optional[bool] = False