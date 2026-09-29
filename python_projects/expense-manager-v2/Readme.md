# 💰 Expense Manager — V2

A production-style **Expense Manager REST API** built with Python.

V2 takes the simple V1 Expense Manager and upgrades it into a modular backend application using advanced Python concepts, database persistence, REST APIs, validation, logging, and testing.

---

# 🎯 Objective

V1 focused on learning Python fundamentals.

V2 focuses on applying Python in a real backend application.

```text
V1
 │
 │  JSON + CLI
 ▼
V2
 │
 ├── OOP
 ├── SQLite
 ├── FastAPI
 ├── Pydantic
 ├── Type Hints
 ├── Custom Exceptions
 ├── Decorators
 ├── Context Managers
 ├── Generators
 ├── Async/Await
 ├── Logging
 └── Testing
```

---

# 📌 Features

* Create income transactions
* Create expense transactions
* View transactions
* Delete transactions
* Validate transaction data
* Store data in SQLite
* REST API using FastAPI
* Request validation using Pydantic
* Custom exceptions
* Centralized database handling
* Logging
* Async Python examples
* Generator-based processing
* Automated tests
* Modular architecture

---

# 🛠️ Technologies

## Core

* Python 3
* SQLite

## Backend

* FastAPI
* Pydantic
* Uvicorn

## Testing

* pytest

## Python Standard Library

```text
dataclasses
datetime
logging
contextlib
functools
asyncio
sqlite3
```

---

# 📁 Project Structure

```text
expense-manager-v2/
│
├── app/
│   ├── __init__.py
│   │
│   ├── models.py
│   ├── database.py
│   ├── exceptions.py
│   ├── decorators.py
│   ├── context.py
│   ├── repository.py
│   ├── service.py
│   └── api.py
│
├── tests/
│   └── test_service.py
│
├── main.py
├── expenses.db
├── .env
├── requirements.txt
└── README.md
```

---

# 🏗️ Architecture

V2 follows a simple layered architecture.

```text
                    Client
                      │
                      ▼
              ┌───────────────┐
              │    FastAPI    │
              │   API Layer   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    Service    │
              │     Layer     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Repository   │
              │     Layer     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    SQLite     │
              │   Database    │
              └───────────────┘
```

### Responsibilities

**API Layer**

Handles HTTP requests and responses.

**Service Layer**

Contains business logic.

**Repository Layer**

Handles database operations.

**Database Layer**

Manages database connections and transactions.

---

# 📦 Installation

## 1. Clone the project

```bash
git clone <your-repository-url>
cd expense-manager-v2
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install fastapi uvicorn pydantic pytest
```

---

# 📄 requirements.txt

```text
fastapi
uvicorn
pydantic
pytest
```

---

# 🗄️ Database

V2 uses SQLite.

Database:

```text
expenses.db
```

Table:

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);
```

---

# ▶️ Initialize Application

Run:

```bash
python main.py
```

The application will create the database and required tables.

---

# 🚀 Start API

Run:

```bash
uvicorn app.api:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

---

# 📚 API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://localhost:8000/docs
```

Alternative ReDoc:

```text
http://localhost:8000/redoc
```

---

# 🔌 API Endpoints

## Create Transaction

```http
POST /transactions
```

Request:

```json
{
    "type": "expense",
    "amount": 500,
    "category": "Food",
    "description": "Dinner"
}
```

Response:

```json
{
    "message": "Transaction created"
}
```

---

# 📋 Get Transactions

```http
GET /transactions
```

Example response:

```json
[
    [
        1,
        "expense",
        500,
        "Food",
        "Dinner",
        "2026-09-29T10:00:00"
    ]
]
```

---

# 🗑️ Delete Transaction

```http
DELETE /transactions/{transaction_id}
```

Example:

```http
DELETE /transactions/1
```

Response:

```json
{
    "message": "Transaction deleted"
}
```

---

# 🧱 Data Model

A transaction contains:

```text
Transaction
│
├── id
├── type
├── amount
├── category
├── description
└── date
```

Python model:

```python
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
```

---

# 🧠 Python Concepts Covered

## 1. Object-Oriented Programming

```python
class ExpenseService:

    def __init__(self, repository):
        self.repository = repository
```

Concepts:

* Classes
* Objects
* Constructors
* Instance variables
* Methods
* Encapsulation

---

# 2. Dataclasses

```python
from dataclasses import dataclass


@dataclass
class Transaction:

    id: int | None
    type: str
    amount: float
```

Dataclasses reduce boilerplate code for data objects.

---

# 3. Type Hints

```python
def add_transaction(
    transaction_type: str,
    amount: float,
    category: str,
    description: str
):
    ...
```

Type hints make code easier to understand and maintain.

---

# 4. Custom Exceptions

```python
class ExpenseManagerError(Exception):
    pass


class InvalidAmountError(ExpenseManagerError):
    pass
```

Example:

```python
if amount <= 0:
    raise InvalidAmountError(
        "Amount must be greater than zero"
    )
```

---

# 5. Decorators

Example:

```python
@log_execution
def add_transaction():
    ...
```

Decorator:

```python
from functools import wraps


def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print(f"Executing {func.__name__}")

        result = func(*args, **kwargs)

        print(f"Finished {func.__name__}")

        return result

    return wrapper
```

Concepts covered:

```text
functions as objects
*args
**kwargs
closures
decorators
functools.wraps
```

---

# 6. Context Managers

Database operations use:

```python
with get_connection() as connection:
    ...
```

Custom context managers can use:

```python
class DatabaseContext:

    def __enter__(self):
        print("Connection opened")
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        print("Connection closed")
```

Concepts:

```text
__enter__
__exit__
with
resource management
```

---

# 7. Generators

Generators allow data to be processed one item at a time.

```python
def transaction_generator(transactions):

    for transaction in transactions:

        if transaction["amount"] > 1000:
            yield transaction
```

Usage:

```python
for transaction in transaction_generator(transactions):
    print(transaction)
```

Concepts:

```text
yield
lazy evaluation
memory-efficient processing
iterators
```

---

# 8. Lambda

```python
get_amount = lambda transaction: transaction["amount"]
```

Example:

```python
sorted(
    transactions,
    key=lambda x: x["amount"]
)
```

---

# 9. map()

```python
amounts = list(
    map(
        lambda transaction: transaction["amount"],
        transactions
    )
)
```

---

# 10. filter()

```python
expenses = list(
    filter(
        lambda transaction:
            transaction["type"] == "expense",
        transactions
    )
)
```

---

# 11. Async / Await

V2 introduces asynchronous Python.

```python
import asyncio


async def fetch_data():

    await asyncio.sleep(1)

    return "data"
```

Run:

```python
asyncio.run(fetch_data())
```

---

# 12. asyncio.gather()

Multiple asynchronous operations can run concurrently.

```python
results = await asyncio.gather(
    fetch_data(),
    fetch_data(),
    fetch_data()
)
```

Concepts:

```text
async
await
coroutines
event loop
tasks
asyncio
gather
```

---

# 13. Database Transactions

The database layer handles:

```text
connection
    ↓
execute SQL
    ↓
commit
    ↓
close
```

If something fails:

```text
connection
    ↓
execute SQL
    ↓
ERROR
    ↓
rollback
    ↓
close
```

Example:

```python
try:

    connection.execute(query)

    connection.commit()

except Exception:

    connection.rollback()

    raise
```

---

# 14. Repository Pattern

The repository handles database operations.

```python
class TransactionRepository:

    def add(self, transaction):
        ...

    def get_all(self):
        ...

    def delete(self, transaction_id):
        ...
```

The service doesn't need to know how SQL works.

```text
Service
   ↓
Repository
   ↓
SQLite
```

---

# 15. Service Layer

The service contains business rules.

Example:

```python
class ExpenseService:

    def __init__(self, repository):
        self.repository = repository

    def add_transaction(
        self,
        transaction_type,
        amount,
        category,
        description
    ):

        if amount <= 0:
            raise InvalidAmountError()

        self.repository.add(...)
```

This keeps business logic separate from the API.

---

# 16. Pydantic

FastAPI uses Pydantic for request validation.

```python
from pydantic import BaseModel


class TransactionRequest(BaseModel):

    type: str
    amount: float
    category: str
    description: str
```

Invalid requests are automatically rejected.

---

# 17. FastAPI

Create API:

```python
from fastapi import FastAPI


app = FastAPI()


@app.get("/transactions")
def get_transactions():

    return service.get_transactions()
```

---

# 18. Logging

Use Python's logging system instead of relying only on `print()`.

```python
import logging


logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)


logger.info("Application started")
logger.warning("Invalid transaction")
logger.error("Database error")
```

Logging levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

---

# 19. Testing

Tests are stored under:

```text
tests/
```

Example:

```python
def test_amount_validation():

    amount = 100

    assert amount > 0
```

Run:

```bash
pytest
```

---

# 🔄 V1 → V2

| Area             | V1          | V2       |
| ---------------- | ----------- | -------- |
| Interface        | CLI         | REST API |
| Storage          | JSON        | SQLite   |
| Architecture     | Single file | Layered  |
| Functions        | ✅           | ✅        |
| Lists/dicts      | ✅           | ✅        |
| Exceptions       | Basic       | Custom   |
| OOP              | ❌           | ✅        |
| Dataclasses      | ❌           | ✅        |
| Type hints       | Basic       | ✅        |
| Decorators       | ❌           | ✅        |
| Generators       | ❌           | ✅        |
| Context managers | Basic       | ✅        |
| Database         | ❌           | ✅        |
| FastAPI          | ❌           | ✅        |
| Pydantic         | ❌           | ✅        |
| Async            | ❌           | ✅        |
| Logging          | ❌           | ✅        |
| Testing          | ❌           | ✅        |

---

# 🎯 Learning Goals

After completing V2, you should understand:

```text
Core Python
     ↓
Functions
     ↓
OOP
     ↓
Dataclasses
     ↓
Exceptions
     ↓
Decorators
     ↓
Generators
     ↓
Context Managers
     ↓
Type Hints
     ↓
Database
     ↓
FastAPI
     ↓
Pydantic
     ↓
Async Python
     ↓
Logging
     ↓
Testing
     ↓
Production-style Python
```

---

# 🚀 Possible Future Improvements

If you want to extend the project later:

* JWT authentication
* User management
* PostgreSQL
* SQLAlchemy
* Redis caching
* Docker
* Background jobs
* Monthly budgets
* Expense reports
* CSV export
* React frontend
* CI/CD

These are **optional** and are outside the scope of V2.

---

# ✅ Final Goal

The project should demonstrate that you can:

1. Write clean Python.
2. Use OOP appropriately.
3. Handle errors correctly.
4. Work with databases.
5. Build REST APIs.
6. Use asynchronous Python.
7. Write tests.
8. Structure a maintainable Python application.

**V1 = Learn Python**

**V2 = Build with Python**
