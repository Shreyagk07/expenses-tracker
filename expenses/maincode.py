from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tabulate import tabulate
from sqlalchemy import func
import os
import matplotlib.pyplot as plt

plt.ion()
plt.ioff()



Base = declarative_base()
engine = create_engine('sqlite:///expensestrack.db')
Session = sessionmaker(bind=engine)
session = Session()


class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_expense():
    try:
        item = input("Enter the item: ")
        amount = float(input("Enter the amount: "))
        category = input("Enter the category: ")
        new_expense = Expense(item=item, amount=amount, category=category)
        session.add(new_expense)
        session.commit()
        print("Expense added successfully!")
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")

def view_expenses():
    expenses = session.query(Expense).order_by(Expense.id).all()
    if expenses:
        table = [[expense.id, expense.item, expense.amount, expense.category, expense.date_added.strftime('%Y-%m-%d %H:%M')] for expense in expenses]
        print(tabulate(table, headers=["ID", "Item", "Amount", "Category", "Date Added"], tablefmt="fancy_grid"))
    else:
        print("No expenses recorded yet.")
    input("\nPress Enter to continue...")

def delete_expense():
    view_expenses()
    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))
        expense = session.query(Expense).get(expense_id)
        if expense:
            session.delete(expense)
            session.commit()
            print("Expense deleted successfully!")
        else:
            print("Expense not found!")
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")
    input("\nPress Enter to continue...")

def clear_database():
    confirm = input("Are you sure you want to clear all data? (yes/no): ")
    if confirm.lower() == 'yes':
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Database cleared!")


from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def predict_expenses():
   
    expenses = session.query(Expense).order_by(Expense.date_added).all()
    if not expenses:
        print("No expenses recorded yet for prediction.")
        return
    dates = np.array([expense.date_added.toordinal() for expense in expenses]).reshape(-1, 1)
    amounts = np.array([expense.amount for expense in expenses])
    
    # Create and train the model
    model = LinearRegression()
    model.fit(dates, amounts)
    
    # Predict the future expenses (e.g., for the next 30 days)
    future_dates = np.array([datetime.now().toordinal() + i for i in range(1, 31)]).reshape(-1, 1)
    future_predictions = model.predict(future_dates)
    
    # Plot the results
    plt.plot_date([datetime.fromordinal(int(d[0])) for d in dates], amounts, '-o', label="Past Expenses")
    plt.plot_date([datetime.fromordinal(int(d[0])) for d in future_dates], future_predictions, '--', label="Predicted Expenses")
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Expense Prediction')
    plt.legend()
    plt.show()

    print("Prediction completed. Check the graph for future expense trends.")


def plot_expenses():
    expenses = session.query(Expense).order_by(Expense.date_added).all()
    
    if not expenses:
        print("No expenses recorded yet to plot.")
        return
    
    # Group expenses by date or category
    dates = [expense.date_added.strftime('%Y-%m-%d') for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, amounts, marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Expenses Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_expenses_by_category():
    categories = session.query(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).all()
    
    if not categories:
        print("No expenses recorded yet to plot.")
        return

    labels, amounts = zip(*categories)
    
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.show()

    


def add_expense_with_custom_category():
    item = input("Enter the item: ")
    amount = float(input("Enter the amount: "))
    
    categories = ['Food', 'Travel', 'Shopping', 'Other']
    print("Available categories:")
    for i, category in enumerate(categories):
        print(f"{i + 1}. {category}")
    
    custom_category = input("Enter the category (or 'new' to add a custom one): ")
    if custom_category == 'new':
        category = input("Enter the new category name: ")
        categories.append(category)
    else:
        category = categories[(custom_category) - 1]
    
    new_expense = Expense(item=item, amount=amount, category=category)
    session.add(new_expense)
    session.commit()
    print("Expense added successfully with custom category!")



def main():
    while True:
        clear_console()
        print("Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Clear Database (Optional)")
        print("5. Predict Future Expenses")
        print("6. Plot Expenses")
        print("7. Add Expense with Custom Category")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            clear_database()
        elif choice == '5':
            predict_expenses()
        elif choice == '6':
            plot_expenses()
        elif choice == '7':
            add_expense_with_custom_category()
        elif choice == '8':
            print("Goodbye!")
            session.close()
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")





if __name__ == '__main__':
    main()
