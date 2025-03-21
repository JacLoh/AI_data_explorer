import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id VARCHAR(255) PRIMARY KEY,
            filename TEXT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id VARCHAR(255) PRIMARY KEY,
            prompt_id VARCHAR(255),
            rating TEXT,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_prompt(id, filename, question, answer, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prompts (id, filename, question, answer, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (id, filename, question, answer, timestamp))
    conn.commit()
    conn.close()

def insert_feedback(id, prompt_id, rating, comment, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (id, prompt_id, rating, comment, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (id, prompt_id, rating, comment, timestamp))
    conn.commit()
    conn.close()

def fetch_prompts(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename, question, answer, timestamp FROM prompts ORDER BY timestamp DESC LIMIT %s", (limit,))
    results = cursor.fetchall()
    conn.close()
    return results
