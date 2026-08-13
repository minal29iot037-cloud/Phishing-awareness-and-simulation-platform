import sqlite3
DATABASE = "phishing_awareness.db"

def get_connection():
  connection = sqlite3.connect(DATABASE)
  connection.row_factory = sqlite3.row
  return connection

def initialize_database():
  connection = get_connection()

  connection.execute("""
        CREATE TABLE IF NOT EXISTS users(
             id INTEGER PRIMARY KEY
AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            passward_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT
'user',
            created_at TIMESTAMP DEFAULT
CURRENT_TIMESTAMP
      )
  """)

  connection.commit()
  connection.close()
