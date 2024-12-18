import asyncio

from celery import Celery
from sqlalchemy.orm import Session
import redis
import json
from typing import Dict, Any
import logging

from core.config import get_settings
from db.database import SessionLocal


celery_app = Celery(
    'transaction_tasks',
    broker=get_settings().REDIS_URL,
    backend=get_settings().REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

redis_client = redis.from_url(get_settings().REDIS_URL)

logger = logging.getLogger(__name__)

@celery_app.task(name="update_statistics", bind=True, max_retries=3)
def update_statistics(self, task_id: str = None) -> Dict[str, Any]:

    try:
        db = SessionLocal()
        
        stats = calculate_statistics(db)
        
        current_task_id = task_id or str(self.request.id)
        
        redis_client.setex(
            f"statistics:{current_task_id}",
            3600,
            json.dumps(stats)
        )
        
        logger.info(f"Successfully updated statistics for task_id: {current_task_id}")
        return {
            "status": "success",
            "task_id": current_task_id,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Error updating statistics: {str(e)}")
        self.retry(countdown=60 * 5)
        
    finally:
        db.close()

def calculate_statistics(db: Session) -> Dict[str, Any]:
    from services.transaction_service import TransactionService

    service = TransactionService(db)
    stats = asyncio.run(service.get_statistics())

    return {
        "total_transactions": stats.total_transactions,
        "average_transaction_amount": stats.average_transaction_amount,
        "top_transactions": [
            {
                "transaction_id": t.transaction_id,
                "amount": float(t.amount)
            }
            for t in stats.top_transactions
        ]
    }

@celery_app.task(name="clear_statistics_cache")
def clear_statistics_cache() -> Dict[str, str]:
    try:
        keys = redis_client.keys("statistics:*")
        if keys:
            redis_client.delete(*keys)
        
        return {"status": "success", "message": "Statistics cache cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        3600.0,  # каждый час
        update_statistics.s(),
        name='update-statistics-hourly'
    )
