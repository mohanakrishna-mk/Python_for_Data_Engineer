from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    id: int | None
    type: str
    amount: float
    category: str
    description: str
    date: datetime