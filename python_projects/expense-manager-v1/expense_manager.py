import json
from datetime import datetime

FILE_NAME = "expenses.json"


# ---------- File Handling ----------

def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------- Add Transactions ----------

def add_transaction(expenses, transaction_type):

    amount = float(input("Amount: "))
    category = input("Category: ")
    description = input("Description: ")

    transaction = {
        "id": len(expenses) + 1,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses.append(transaction)
    save_data(expenses)

    print("Transaction added successfully!")


# ---------- View Transactions ----------

def view_transactions(expenses):

    if not expenses:
        print("No transactions found.")
        return

    print("\n========== Transactions ==========")

    for expense in expenses:
        print(
            f"ID: {expense['id']} | "
            f"{expense['type']} | "
            f"₹{expense['amount']} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"{expense['date']}"
        )


# ---------- Delete Transaction ----------

def delete_transaction(expenses):

    view_transactions(expenses)

    if not expenses:
        return

    transaction_id = int(input("\nEnter transaction ID: "))

    for expense in expenses:

        if expense["id"] == transaction_id:
            expenses.remove(expense)

            # Re-create IDs
            for index, item in enumerate(expenses, start=1):
                item["id"] = index

            save_data(expenses)

            print("Transaction deleted.")
            return

    print("Transaction not found.")


# ---------- Summary ----------

def show_summary(expenses):

    income = sum(
        expense["amount"]
        for expense in expenses
        if expense["type"] == "income"
    )

    expenses_total = sum(
        expense["amount"]
        for expense in expenses
        if expense["type"] == "expense"
    )

    balance = income - expenses_total

    print("\n========== Summary ==========")
    print(f"Total Income  : ₹{income}")
    print(f"Total Expense : ₹{expenses_total}")
    print(f"Balance       : ₹{balance}")


# ---------- Main Menu ----------

def main():

    expenses = load_data()

    while True:

        print("""
==============================
       EXPENSE MANAGER
==============================

1. Add Income
2. Add Expense
3. View Transactions
4. Delete Transaction
5. View Summary
6. Exit
""")

        choice = input("Choose an option: ")

        try:

            if choice == "1":
                add_transaction(expenses, "income")

            elif choice == "2":
                add_transaction(expenses, "expense")

            elif choice == "3":
                view_transactions(expenses)

            elif choice == "4":
                delete_transaction(expenses)

            elif choice == "5":
                show_summary(expenses)

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()