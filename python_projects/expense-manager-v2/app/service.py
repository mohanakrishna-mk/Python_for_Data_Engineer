from datetime import datetime

from models import Transaction
from exceptions import (
    InvalidAmountError,
    InvalidTransactionTypeError,
    TransactionNotFoundError
)
from decorators import log_execution


class ExpenseService:

    def __init__(self, repository):
        self.repository = repository

    @log_execution
    def add_transaction(
        self,
        transaction_type: str,
        amount: float,
        category: str,
        description: str
    ):

        if amount <= 0:
            raise InvalidAmountError(
                "Amount must be greater than zero"
            )

        if transaction_type not in ("income", "expense"):
            raise InvalidTransactionTypeError(
                "Type must be income or expense"
            )

        transaction = Transaction(
            id=None,
            type=transaction_type,
            amount=amount,
            category=category,
            description=description,
            date=datetime.now()
        )

        self.repository.add(transaction)

    def get_transactions(self):

        return self.repository.get_all()

    def delete_transaction(self, transaction_id):

        deleted = self.repository.delete(transaction_id)

        if deleted == 0:
            raise TransactionNotFoundError(
                "Transaction not found"
            )