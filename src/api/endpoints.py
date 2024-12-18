from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.security import get_api_key
from db.database import get_db
from schemas.transaction import TransactionCreate, TransactionResponse, Statistics
from services.transaction_service import TransactionService

router = APIRouter()

@router.post(path="/transactions",
            response_model=TransactionResponse,
            status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(get_api_key)],
            )
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    try:
        task_id = await service.create_transaction(transaction)
        return TransactionResponse(
            message="Transaction received",
            task_id=task_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(path="/transactions",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_api_key)],
               )
async def delete_transactions(db: Session = Depends(get_db)):
    service = TransactionService(db)
    await service.delete_all_transactions()
    return {"message": "All transactions deleted"}

@router.get(path="/statistics",
            response_model=Statistics,
            dependencies=[Depends(get_api_key)],
            )
async def get_statistics(db: Session = Depends(get_db)):
    service = TransactionService(db)
    return await service.get_statistics()
