import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            category TEXT,
            amount REAL,
            type TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fixed_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            category TEXT,
            amount REAL,
            type TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS closed_months (
            month_name TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def add_transaction(date, description, category, amount, t_type):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, description, category, amount, type) VALUES (?, ?, ?, ?, ?)",
                   (date, description, category, amount, t_type))
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

def get_fixed_expenses():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT * FROM fixed_expenses", conn)
    conn.close()
    return df

def add_fixed_expense(description, category, amount, t_type):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fixed_expenses (description, category, amount, type) VALUES (?, ?, ?, ?)",
                   (description, category, amount, t_type))
    conn.commit()
    conn.close()

def delete_fixed_expense(exp_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fixed_expenses WHERE id = ?", (exp_id,))
    conn.commit()
    conn.close()

def get_closed_months():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT month_name FROM closed_months")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def is_month_closed(month_name):
    closed = get_closed_months()
    return month_name in closed

def close_month_db(month_name):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO closed_months (month_name) VALUES (?)", (month_name,))
    conn.commit()
    conn.close()

def reopen_month_db(month_name):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM closed_months WHERE month_name = ?", (month_name,))
    conn.commit()
    conn.close()