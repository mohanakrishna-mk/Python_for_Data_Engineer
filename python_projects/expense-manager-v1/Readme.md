# 💰 Expense Manager — V1

A simple command-line **Expense Manager** built using core Python.

The purpose of V1 is to learn and practice Python fundamentals by building a real application.

---

## 📌 Features

* Add income
* Add expenses
* View all transactions
* Delete transactions
* View income/expense summary
* Store data in a JSON file
* Basic input validation
* Error handling

---

## 🛠️ Technologies

* Python 3
* JSON
* `datetime`

No external Python packages are required.

---

## 📁 Project Structure

```text
expense-manager-v1/
│
├── expense_manager.py
├── expenses.json
└── README.md
```

`expenses.json` is created automatically when the first transaction is saved.

---

## ▶️ Run the Application

Check Python version:

```bash
python --version
```

Run the application:

```bash
python expense_manager.py
```

---

## 🖥️ Application Menu

```text
==============================
       EXPENSE MANAGER
==============================

1. Add Income
2. Add Expense
3. View Transactions
4. Delete Transaction
5. View Summary
6. Exit

Choose an option:
```

---

## 💵 Add Income

Example:

```text
Choose an option: 1

Amount: 50000
Category: Salary
Description: September salary

Transaction added successfully!
```

---

## 💸 Add Expense

Example:

```text
Choose an option: 2

Amount: 500
Category: Food
Description: Dinner

Transaction added successfully!
```

---

## 📋 View Transactions

Example:

```text
========== Transactions ==========

ID: 1 | income | ₹50000 | Salary | September salary | 2026-09-29
ID: 2 | expense | ₹500 | Food | Dinner | 2026-09-29
```

---

## 🗑️ Delete Transaction

Example:

```text
Choose an option: 4

Enter transaction ID: 2

Transaction deleted.
```

---

## 📊 View Summary

Example:

```text
========== Summary ==========

Total Income  : ₹50000
Total Expense : ₹500
Balance       : ₹49500
```

---

# 📄 Data Storage

Transactions are stored in:

```text
expenses.json
```

Example:

```json
[
    {
        "id": 1,
        "type": "income",
        "amount": 50000,
        "category": "Salary",
        "description": "September salary",
        "date": "2026-09-29"
    },
    {
        "id": 2,
        "type": "expense",
        "amount": 500,
        "category": "Food",
        "description": "Dinner",
        "date": "2026-09-29"
    }
]
```

---

# 🧠 Python Concepts Covered

## 1. Variables

```python
amount = 500
category = "Food"
```

---

## 2. Data Types

The project uses:

```text
int
float
str
list
dict
bool
```

---

## 3. Lists

Transactions are stored in a list:

```python
expenses = []
```

Example:

```python
expenses.append(transaction)
```

---

## 4. Dictionaries

Each transaction is represented as a dictionary:

```python
transaction = {
    "id": 1,
    "type": "expense",
    "amount": 500,
    "category": "Food",
    "description": "Dinner",
    "date": "2026-09-29"
}
```

---

## 5. Conditions

```python
if choice == "1":
    add_income()

elif choice == "2":
    add_expense()

else:
    print("Invalid option")
```

---

## 6. Loops

The main application uses a `while` loop:

```python
while True:
    # menu
```

Transactions are processed using a `for` loop:

```python
for expense in expenses:
    print(expense)
```

---

## 7. Functions

The application is divided into functions:

```python
def add_transaction():
    pass


def view_transactions():
    pass


def delete_transaction():
    pass


def show_summary():
    pass
```

This keeps the code organized and reusable.

---

## 8. List Comprehensions

Example:

```python
expenses_only = [
    transaction
    for transaction in transactions
    if transaction["type"] == "expense"
]
```

---

## 9. `sum()`

Calculate total expenses:

```python
total = sum(
    transaction["amount"]
    for transaction in transactions
    if transaction["type"] == "expense"
)
```

---

## 10. Exception Handling

Invalid user input is handled using:

```python
try:
    amount = float(input("Amount: "))

except ValueError:
    print("Please enter a valid number.")
```

---

## 11. File Handling

The application reads and writes files using:

```python
with open("expenses.json", "r") as file:
    data = json.load(file)
```

Writing:

```python
with open("expenses.json", "w") as file:
    json.dump(data, file, indent=4)
```

---

## 12. JSON

Python objects are stored as JSON:

```python
import json
```

Reading:

```python
json.load(file)
```

Writing:

```python
json.dump(data, file)
```

---

## 13. Modules

The application uses Python's built-in modules:

```python
import json
from datetime import datetime
```

---

## 14. Date and Time

Transaction dates are generated using:

```python
from datetime import datetime

today = datetime.now()
```

---

# 🎯 V1 Learning Goals

After completing V1, you should be comfortable with:

```text
Variables
Data Types
Strings
Numbers
Lists
Dictionaries
Tuples
Sets
if / elif / else
for loops
while loops
break / continue
Functions
Parameters
Return values
List comprehensions
File handling
JSON
Exception handling
Modules
datetime
```

---

# 🚫 Not Included in V1

These concepts are intentionally reserved for V2:

```text
OOP
Dataclasses
Inheritance
Decorators
Generators
Iterators
Custom Context Managers
SQLite/PostgreSQL
SQLAlchemy
FastAPI
Pydantic
Async/Await
Concurrency
Logging
pytest
Production architecture
```

---

# 🚀 V2

V2 will convert this simple application into a more production-style Python application with:

```text
Expense Manager V1
       │
       ▼
   Refactor
       │
       ▼
       V2
       │
       ├── OOP
       ├── Database
       ├── FastAPI
       ├── Pydantic
       ├── Decorators
       ├── Generators
       ├── Context Managers
       ├── Async Python
       ├── Logging
       └── Testing
```

**V1 goal:** Learn the Python language by building a working application.

**V2 goal:** Learn advanced Python and production-style application development.
