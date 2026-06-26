import sqlite3
from datetime import datetime

DB_PATH = "memory.db"

def init_memory():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                created_at TEXT
            )       
                   """)

    connection.commit()
    connection.close()
    
def save_memory(session_id, role, content):
    init_memory()
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO memory (session_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
    """, (session_id, role, content, datetime.now().isoformat()))

    connection.commit()
    connection.close()

def get_memory(session_id, limit=5):
    init_memory()
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, content FROM memory
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cursor.fetchall()
    connection.close()

    return list(reversed(rows))