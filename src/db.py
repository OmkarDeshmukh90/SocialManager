import sqlite3

def create_db():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  status_id TEXT,
                  conversation TEXT)''')
    conn.commit()
    conn.close()

def log_conversation(status_id, conversation):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("INSERT INTO conversations (status_id, conversation) VALUES (?, ?)",
              (status_id, conversation))
    conn.commit()
    conn.close()
