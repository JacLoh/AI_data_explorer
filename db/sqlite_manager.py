import sqlite3

# Database file
DB_FILE = "database.db"

# === DATABASE SETUP ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id TEXT PRIMARY KEY,
            filename TEXT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id TEXT PRIMARY KEY,
            prompt_id TEXT,
            rating TEXT,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# === INSERT FUNCTIONS ===
def insert_prompt(id, filename, question, answer, timestamp):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prompts (id, filename, question, answer, timestamp) VALUES (?, ?, ?, ?, ?)",
        (id, filename, question, answer, timestamp)
    )
    conn.commit()
    conn.close()

def insert_feedback(id, prompt_id, rating, comment, timestamp):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (id, prompt_id, rating, comment, timestamp) VALUES (?, ?, ?, ?, ?)",
        (id, prompt_id, rating, comment, timestamp)
    )
    conn.commit()
    conn.close()

# === FETCH FUNCTIONS ===
def fetch_prompts(limit=10):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, question, answer, timestamp FROM prompts ORDER BY timestamp DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()
    return results
