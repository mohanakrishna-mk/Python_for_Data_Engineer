from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from repository import TransactionRepository
from service import ExpenseService


app = FastAPI(
    title="Expense Manager API"
)


repository = TransactionRepository()
service = ExpenseService(repository)


class TransactionRequest(BaseModel):
    type: str
    amount: float
    category: str
    description: str


@app.post("/transactions")
def add_transaction(request: TransactionRequest):

    try:

        service.add_transaction(
            request.type,
            request.amount,
            request.category,
            request.description
        )

        return {
            "message": "Transaction created"
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.get("/transactions")
def get_transactions():

    return service.get_transactions()


@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):

    try:

        service.delete_transaction(transaction_id)

        return {
            "message": "Transaction deleted"
        }

    except Exception as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )