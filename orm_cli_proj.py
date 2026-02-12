# FINTRACK PRO - CLI FINANCE MANAGER


# importing required things from sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

import os


print("Starting FinTrack Pro...")
print("Checking database setup...")

# this will create fintrack.db in same folder
engine = create_engine("sqlite:///fintrack.db", echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

print("Database connection created successfully.")


# Category table
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # one category can have many expenses showing one to many relation
    expenses = relationship("Expense", back_populates="category")


# Expense table
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    amount = Column(Float)
    date = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="expenses")


# Subscription table
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    next_date = Column(String)


# Budget table
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    month = Column(String)
    limit = Column(Float)


print("Creating tables if not exist...")
Base.metadata.create_all(engine) #create_all creates table if doesnot exist and ignores if exists
print("Tables ready.")


# ----------- FUNCTIONS --------------

def add_category():
    print("Adding new category...")
    name = input("Enter category name: ")

    new_cat = Category(name=name)
    session.add(new_cat)
    session.commit()

    print("Category added successfully!")


def add_expense():
    print("Adding new expense...")

    title = input("Expense title: ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")
    cat_id = int(input("Category ID: "))

    new_expense = Expense(title=title, amount=amount, date=date, category_id=cat_id)

    session.add(new_expense)
    session.commit()

    print("Expense saved successfully!")


def update_expense():
    print("Updating expense...")
    eid = int(input("Expense ID: "))

    expense = session.query(Expense).filter(Expense.id == eid).first()

    if expense:
        print("Expense found. Updating...")
        expense.title = input("New title: ")
        expense.amount = float(input("New amount: "))
        session.commit()
        print("Expense updated successfully!")
    else:
        print("Expense not found.")


def delete_expense():
    print("Deleting expense...")
    eid = int(input("Expense ID: "))

    expense = session.query(Expense).filter(Expense.id == eid).first()

    if expense:
        session.delete(expense)
        session.commit()
        print("Expense deleted.")
    else:
        print("Expense not found.")


def search_by_date():
    print("Searching expense by date...")
    d = input("Enter date (YYYY-MM-DD): ")

    results = session.query(Expense).filter(Expense.date == d).all()

    print("Search results:")
    for r in results:
        print(r.title, "-", r.amount)


# ----------- RAW SQL REPORT --------------

def category_report():
    print("Generating category report...")

    sql = """
    SELECT c.name, SUM(e.amount)
    FROM categories c
    JOIN expenses e
    ON c.id = e.category_id
    GROUP BY c.name
    """

    result = session.execute(text(sql))

    print("Category wise total spending:")
    for row in result:
        print(row[0], "->", row[1])


# ----------- BUDGET SECTION --------------

def set_budget():
    print("Setting monthly budget...")
    month = input("Enter month (YYYY-MM): ")
    limit = float(input("Enter spending limit: "))

    session.add(Budget(month=month, limit=limit))
    session.commit()

    print("Budget saved.")


def budget_alert():
    print("Checking budget alert...")
    month = input("Enter month (YYYY-MM): ")

    total = session.execute(
        text("SELECT SUM(amount) FROM expenses WHERE date LIKE :m"),
        {"m": f"{month}%"}
    ).scalar()

    # if there are no expenses, SUM returns None (just in case)
    if total is None:
        total = 0

    budget = session.query(Budget).filter(Budget.month == month).first()

    print("Total spending this month:", total)

    if budget and total > budget.limit:
        print("WARNING: Budget exceeded!")
    elif not budget:
        print("No budget set for this month.")
    else:
        print("You are within budget.")



while True:
    print("""
========= FINTRACK PRO =========
1. Add Category
2. Add Expense
3. Update Expense
4. Delete Expense
5. Search by Date
6. Category Report
7. Set Monthly Budget
8. Budget Alert
9. Exit
""")

    choice = input("Choose option: ")

    if choice == "1":
        add_category()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        update_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        search_by_date()
    elif choice == "6":
        category_report()
    elif choice == "7":
        set_budget()
    elif choice == "8":
        budget_alert()
    elif choice == "9":
        print("Exiting program...")
        break
    else:
        print("Invalid option, try again.")
