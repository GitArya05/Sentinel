# core/generator.py
import asyncio
import random
from faker import Faker
from core.schemas import Transaction

fake = Faker('en_IN')

MERCHANT_CATEGORIES = ["Retail", "Food & Beverage", "Travel", "Utility", "Transfer", "Crypto"]
# Aligning exactly with the trained ML encoder
VALID_LOCATIONS = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune", "Nagpur", "Foreign_IP"]

async def generate_stream(stream_id: int, queue: asyncio.Queue):
    while True:
        await asyncio.sleep(random.uniform(0.01, 0.2))
        
        # 95% Legitimate, 5% Fraud Injection
        is_fraud_scenario = random.random() < 0.05
        
        if is_fraud_scenario:
            # Force a known fraud signature: High transfer or Crypto/Foreign IP
            category = random.choice(["Crypto", "Transfer"])
            location = "Foreign_IP" if category == "Crypto" else random.choice(VALID_LOCATIONS)
            amount = round(random.uniform(20000.0, 80000.0), 2)
        else:
            # Normal distribution
            category = random.choice(MERCHANT_CATEGORIES)
            location = random.choice([loc for loc in VALID_LOCATIONS if loc != "Foreign_IP"])
            amount = round(random.uniform(10.0, 5000.0), 2)

        transaction_data = Transaction(
            transaction_id=fake.uuid4(),
            user_id=fake.user_name(),
            amount=amount,
            merchant_category=category,
            location=location,
            stream_id=stream_id
        )
        
        await queue.put(transaction_data)