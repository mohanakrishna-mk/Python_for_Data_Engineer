class ExpenseManagerError(Exception):
    pass


class InvalidAmountError(ExpenseManagerError):
    pass


class InvalidTransactionTypeError(ExpenseManagerError):
    pass


class TransactionNotFoundError(ExpenseManagerError):
    pass