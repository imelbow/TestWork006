from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float, index=True)
    currency = Column(String(3), index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
