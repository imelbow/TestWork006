from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any

class TransactionCreate(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    user_id: str = Field(..., description="Identifier of the user")
    amount: float = Field(..., gt=0, description="Transaction amount, must be greater than zero")
    currency: str = Field(..., min_length=3, max_length=3, description="Transaction currency, represented by a 3-character ISO code")
    timestamp: datetime = Field(..., description="Timestamp of the transaction")

    @field_validator('currency')
    def validate_currency(cls, v):
        if not v.isupper():
            raise ValueError('Currency must be in uppercase')
        valid_currencies = {'USD', 'EUR', 'RUB', 'GBP', 'JPY', 'CNY'}
        if v not in valid_currencies:
            raise ValueError(f'Unsupported currency. Supported currencies are: {", ".join(valid_currencies)}')
        return v

class TransactionResponse(BaseModel):
    message: str = Field(..., description="Response message")
    task_id: str = Field(..., description="Identifier of the created task for transaction processing")

class TopTransaction(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    amount: float = Field(..., description="Transaction amount")

class Statistics(BaseModel):
    total_transactions: int = Field(..., description="Total number of transactions")
    average_transaction_amount: float = Field(..., description="Average amount of all transactions")
    top_transactions: List[TopTransaction] = Field(..., description="Top-3 largest transactions by amount")
    currency_breakdown: List[Dict[str, Any]] = Field(..., description="Breakdown of transactions by currency")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "total_transactions": 25,
                "average_transaction_amount": 180.03,
                "top_transactions": [
                    {"transaction_id": "1", "amount": 1000},
                    {"transaction_id": "2", "amount": 850},
                    {"transaction_id": "3", "amount": 500}
                ]
            }
        }
