import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


def add_expense(expenses):
    try:
        date = input("Date (DD-MM-YYYY): ").strip()
        datetime.strptime(date, "%d-%m-%Y")

        category = input("Category: ").strip().title()
        description = input("Description: ").strip()
        amount = float(input("Amount (₹): "))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        expenses.append({
            "date": date,
            "category": category,
            "description": description,
            "amount": amount
        })
        print("Expense added successfully.")

    except ValueError:
        print("Invalid input. Enter a valid date and a positive amount.")


def show_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    print("\nDate         Category        Description                 Amount")
    print("-" * 65)
    for e in expenses:
        print(f"{e['date']:<12}{e['category']:<16}"
              f"{e['description'][:25]:<27}₹{e['amount']:.2f}")


def analyze_budget(expenses):
    try:
        budget = float(input("Enter monthly budget (₹): "))
        if budget <= 0:
            raise ValueError

        total = sum(e["amount"] for e in expenses)
        remaining = budget - total

        print(f"\nTotal spent: ₹{total:.2f}")
        print(f"Budget:      ₹{budget:.2f}")
        print(f"Remaining:   ₹{remaining:.2f}")

        if total > budget:
            print("Status: OVER BUDGET")
        elif total >= 0.8 * budget:
            print("Status: WARNING - 80% or more of budget used")
        else:
            print("Status: WITHIN BUDGET")

    except ValueError:
        print("Enter a valid positive budget.")


def category_summary(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]

    if not totals:
        print("No data available for analysis.")
        return

    print("\nCategory-wise spending:")
    for category, amount in sorted(totals.items(),
                                   key=lambda item: item[1],
                                   reverse=True):
        print(f"{category:<18} ₹{amount:.2f}")


def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["date", "category", "description", "amount"]
        )
        writer.writeheader()
        writer.writerows(expenses)
    print("Data saved to expenses.csv.")


def load_expenses():
    expenses = []
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                row["amount"] = float(row["amount"])
                expenses.append(row)
    except FileNotFoundError:
        pass
    return expenses


def main():
    expenses = load_expenses()

    while True:
        print("\n=== STUDENT EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Budget analysis")
        print("4. Category summary")
        print("5. Save and exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            analyze_budget(expenses)
        elif choice == "4":
            category_summary(expenses)
        elif choice == "5":
            save_expenses(expenses)
            print("Thank you for using the Student Expense Tracker.")
            break
        else:
            print("Invalid choice. Select 1-5.")


if __name__ == "__main__":
    main()