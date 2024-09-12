from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Expense
import os
import pdb; pdb.set_trace()


from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"



if __name__ == "__main__":
    app.run(debug=True, port=5001)



app = Flask(__name__)
app.secret_key = 'your_secret_key'

engine = create_engine('sqlite:///expensestrack.db')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        item = request.form['item']
        amount = float(request.form['amount'])
        category = request.form['category']
        new_expense = Expense(item=item, amount=amount, category=category)
        session.add(new_expense)
        session.commit()
        flash("Expense added successfully!")
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html')

@app.route('/view')
def view_expenses():
    expenses = session.query(Expense).order_by(Expense.id).all()
    return render_template('view_expenses.html', expenses=expenses)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = session.query(Expense).get(id)
    if expense:
        session.delete(expense)
        session.commit()
        flash("Expense deleted successfully!")
    else:
        flash("Expense not found!")
    return redirect(url_for('view_expenses'))

@app.route('/clear', methods=['POST'])
def clear_database():
    session.query(Expense).delete()
    session.commit()
    flash("Database cleared!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
