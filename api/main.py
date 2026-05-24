# api/main.py
from fastapi import FastAPI, HTTPException
from core.schemas import Transaction
from core.inference import evaluate_transaction

app = FastAPI(
    title="Sentinel Real-Time Engine",
    description="High-throughput fraud detection API",
    version="1.0.0"
)

# Using the precise routing path from your specifications
@app.post("/api/v1/transaction", response_model=Transaction)
async def process_single_transaction(transaction: Transaction):
    """
    Synchronous endpoint for single-transaction evaluation.
    """
    try:
        evaluated_txn = evaluate_transaction(transaction)
        return evaluated_txn
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))