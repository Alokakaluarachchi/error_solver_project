import sqlite3
import numpy as np
import io

DB_NAME = 'company_errors.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_text TEXT NOT NULL,
            solution_text TEXT NOT NULL,
            embedding BLOB NOT NULL,
            user_validated INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Helper: Convert Numpy array to Bytes for SQLite
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return out.read()

# Helper: Convert Bytes from SQLite back to Numpy
def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)