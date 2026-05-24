# core/ingestion.py
import asyncio
import logging
import time
from core.inference import evaluate_transaction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SentinelIngestion")

async def process_queue(queue: asyncio.Queue):
    """
    Pulls data from the 60 streams and routes it to the ML Inference Engine.
    """
    transactions_processed = 0
    start_time = time.time()
    blocks_executed = 0

    while True:
        transaction = await queue.get()
        
        # 1. Run Real-Time Inference
        evaluated_txn = evaluate_transaction(transaction)
        transactions_processed += 1
        
        # --- DEFENSIVE DEBUG LOG ---
        # Only evaluate if the model successfully assigned a score
        if evaluated_txn.risk_score is not None:
            if evaluated_txn.risk_score > 0.3:
                logger.info(f"🔍 INVESTIGATING: Score {evaluated_txn.risk_score:.2f} | {evaluated_txn.amount} INR at {evaluated_txn.merchant_category} ({evaluated_txn.location})")
            
            # 2. Execute Protocol Blocks
            if evaluated_txn.is_blocked:
                blocks_executed += 1
                logger.warning(f"🚨 BLOCKED: Txn {evaluated_txn.transaction_id[:8]} | Score: {evaluated_txn.risk_score:.2f} | {evaluated_txn.amount} INR at {evaluated_txn.merchant_category}")
        else:
            # If the model is offline, log it but don't crash
            if transactions_processed % 100 == 0:
                logger.error("⚠️ SYSTEM WARNING: Model offline. Transactions passing without scoring.")
            
        queue.task_done()