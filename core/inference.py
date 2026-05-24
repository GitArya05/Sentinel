# core/inference.py
import joblib
import pandas as pd
import logging
from core.schemas import Transaction
from api.config import settings

logger = logging.getLogger("SentinelInference")

# FAANG Pattern: Load model into memory ONCE at module initialization
MODEL_PATH = "models/sentinel_lr_model_v1.pkl"
try:
    logger.info(f"Loading inference model from {MODEL_PATH}...")
    pipeline = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully into RAM.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    pipeline = None

def evaluate_transaction(transaction: Transaction) -> Transaction:
    """
    Transforms the transaction into a DataFrame, runs it through the 
    Scikit-Learn pipeline, and applies the blocking threshold.
    """
    if not pipeline:
        return transaction

    # Format the Pydantic model into a Pandas DataFrame expected by the pipeline
    df = pd.DataFrame([{
        "amount": transaction.amount,
        "merchant_category": transaction.merchant_category,
        "location": transaction.location,
        "stream_id": transaction.stream_id
    }])

    # Extract probability of Class 1 (Fraud)
    probabilities = pipeline.predict_proba(df)
    risk_score = float(probabilities[0][1])
    
    # Mutate the transaction object with decisions
    transaction.risk_score = round(risk_score, 4)
    transaction.is_blocked = risk_score > settings.BLOCK_THRESHOLD
    
    return transaction