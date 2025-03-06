# database.py
import sqlite3

def get_connection(db_name="food_journal.db"):
    conn = sqlite3.connect(db_name, check_same_thread=False)
    return conn

def initialize_db(conn):
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        meal TEXT,
        food TEXT,
        calories INTEGER,
        mood TEXT,
        notes TEXT
    )
    ''')
    conn.commit()

def add_entry(conn, entry):
    c = conn.cursor()
    c.execute(
        "INSERT INTO journal (date, meal, food, calories, mood, notes) VALUES (?, ?, ?, ?, ?, ?)",
        entry
    )
    conn.commit()

def get_entries_by_date_range(conn, start_date, end_date):
    c = conn.cursor()
    query = """
    SELECT date, meal, food, calories, mood, notes FROM journal
    WHERE date BETWEEN ? AND ? ORDER BY date
    """
    return c.execute(query, (start_date, end_date)).fetchall()

def get_all_entries(conn):
    c = conn.cursor()
    return c.execute("SELECT date, meal, food, calories, mood, notes FROM journal ORDER BY date").fetchall()

def get_calories_by_meal(conn, start_date, end_date):
    c = conn.cursor()
    query = """
    SELECT date, meal, SUM(calories) as calories 
    FROM journal 
    WHERE date BETWEEN ? AND ? 
    GROUP BY date, meal 
    ORDER BY date
    """
    return c.execute(query, (start_date, end_date)).fetchall()
