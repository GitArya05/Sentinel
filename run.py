# run.py
import asyncio
import logging
from core.generator import generate_stream
from core.ingestion import process_queue

logger = logging.getLogger("SentinelBoot")

async def main():
    logger.info("Initializing Sentinel Engine...")
    
    # 1. Create the central message broker (Queue)
    ingestion_queue = asyncio.Queue()
    
    # 2. Spin up the 60 heterogeneous data streams
    TOTAL_STREAMS = 60
    logger.info(f"Spinning up {TOTAL_STREAMS} concurrent data streams...")
    
    producers = [
        asyncio.create_task(generate_stream(stream_id, ingestion_queue)) 
        for stream_id in range(1, TOTAL_STREAMS + 1)
    ]
    
    # 3. Spin up the consumer (Ingestion engine)
    consumer = asyncio.create_task(process_queue(ingestion_queue))
    
    # Run indefinitely
    await asyncio.gather(*producers, consumer)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSentinel Engine gracefully shut down.")