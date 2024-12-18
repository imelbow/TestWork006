from sqlalchemy.orm import Session
from sqlalchemy import func
import heapq
from typing import List
from uuid import uuid4

from db.models import Transaction
from schemas.transaction import TransactionCreate, Statistics, TopTransaction
from tasks.celery_tasks import update_statistics

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    async def create_transaction(self, transaction: TransactionCreate) -> str:
        existing_transaction = self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction.transaction_id
        ).first()
        
        if existing_transaction:
            raise ValueError("Transaction with the same ID already exists.")

        db_transaction = Transaction(
            transaction_id=transaction.transaction_id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            currency=transaction.currency,
            timestamp=transaction.timestamp
        )
        
        try:
            self.db.add(db_transaction)
            self.db.commit()
            self.db.refresh(db_transaction)
            
            task_id = str(uuid4())
            update_statistics.delay(task_id)
            
            return task_id
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error saving transaction:{str(e)}")

    async def delete_all_transactions(self) -> None:
        try:
            self.db.query(Transaction).delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error when deleting transactions: {str(e)}")

    async def get_statistics(self) -> Statistics:
        try:
            total = self.db.query(func.count(Transaction.transaction_id)).scalar() or 0
            
            currency_stats = (
                self.db.query(
                    Transaction.currency,
                    func.avg(Transaction.amount).label('avg_amount'),
                    func.count(Transaction.transaction_id).label('count')
                )
                .group_by(Transaction.currency)
                .all()
            )
            
            if total > 0:
                average = sum(stat.avg_amount * stat.count for stat in currency_stats) / total
            else:
                average = 0.0
            
            top_transactions = self._get_top_transactions(3)

            return Statistics(
                total_transactions=total,
                average_transaction_amount=round(float(average), 2),
                top_transactions=top_transactions,
                currency_breakdown=[{
                    'currency': stat.currency,
                    'average_amount': round(float(stat.avg_amount), 2),
                    'transaction_count': stat.count
                } for stat in currency_stats]
            )
            
        except Exception as e:
            raise ValueError(f"Error getting statistics: {str(e)}")

    def _get_top_transactions(self, n: int) -> List[TopTransaction]:
        heap = []
        
        batch_size = 1000
        offset = 0
        
        while True:
            batch = (
                self.db.query(Transaction.transaction_id, Transaction.amount)
                .order_by(Transaction.transaction_id)
                .offset(offset)
                .limit(batch_size)
                .all()
            )
            
            if not batch:
                break
                
            for transaction_id, amount in batch:
                if len(heap) < n:
                    heapq.heappush(heap, (amount, transaction_id))
                elif amount > heap[0][0]:
                    heapq.heapreplace(heap, (amount, transaction_id))
            
            offset += batch_size
        
        result = []
        while heap:
            amount, transaction_id = heapq.heappop(heap)
            result.append(
                TopTransaction(transaction_id=transaction_id, amount=amount)
            )
        
        return list(reversed(result))
