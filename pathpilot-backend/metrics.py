import psycopg2
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS total_requests (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS error_count (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS degree_searches (
            degree VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP DEFAULT NOW(),
            id SERIAL PRIMARY KEY
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS response_times (
            response_time FLOAT NOT NULL,
            timestamp TIMESTAMP DEFAULT NOW(),
            id SERIAL PRIMARY KEY
        )
    """)

    conn.commit()
    cur.close()
    conn.close()