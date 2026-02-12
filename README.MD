# 📊 FinTrack Pro – CLI Finance Manager

FinTrack Pro is a command-line based personal finance management system built using **Python**, **SQLite**, and **SQLAlchemy ORM**.

This project allows users to manage daily expenses, track subscriptions, set monthly budgets, and generate analytics using raw SQL queries.

---

## 🚀 Features

- Add Expense  
- Update Expense  
- Delete Expense  
- Search Expenses by Date  
- Category-wise Spending Report  
- Set Monthly Budget  
- Budget Limit Alert  
- Persistent SQLite Storage  

---

## 🛠 Technologies Used

- Python 3  
- SQLite Database  
- SQLAlchemy ORM  
- Raw SQL Queries  
- CLI Interface  

---

## 🗂 Database Structure

### Tables

#### 1. categories
- id (Primary Key)
- name

#### 2. expenses
- id (Primary Key)
- title
- amount
- date
- category_id (Foreign Key → categories.id)

#### 3. subscriptions
- id (Primary Key)
- name
- amount
- next_date

#### 4. budgets
- id (Primary Key)
- month (YYYY-MM)
- limit

### Relationship

- One Category → Many Expenses

---

## ⚙️ Installation & Setup

```bash
pip install sqlalchemy
python fintrack.py

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/fintrack-pro.git
cd fintrack-pro
