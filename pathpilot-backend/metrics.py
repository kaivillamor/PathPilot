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
            error_source VARCHAR(20) DEFAULT 'unknown',
            timestamp TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        ALTER TABLE error_count
        ADD COLUMN IF NOT EXISTS error_source VARCHAR(20) DEFAULT 'unknown'
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id SERIAL PRIMARY KEY,
            code VARCHAR(20) NOT NULL,
            name VARCHAR(200) NOT NULL,
            degree VARCHAR(100) NOT NULL,
            required BOOLEAN DEFAULT FALSE,
            elective BOOLEAN DEFAULT FALSE,
            mathematics BOOLEAN DEFAULT FALSE
        )
    """)
    cur.execute("""
        ALTER TABLE courses
        ADD COLUMN IF NOT EXISTS required BOOLEAN DEFAULT FALSE
    """)
    cur.execute("""
        ALTER TABLE courses
        ADD COLUMN IF NOT EXISTS elective BOOLEAN DEFAULT FALSE
    """)
    cur.execute("""
        ALTER TABLE courses
        ADD COLUMN IF NOT EXISTS mathematics BOOLEAN DEFAULT FALSE
    """)

    conn.commit()
    cur.close()
    conn.close()

def log_request():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO total_requests DEFAULT VALUES")
    conn.commit()
    cur.close()
    conn.close()

def log_error(error_source="unknown"):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO error_count (error_source) VALUES (%s)", (error_source,))
    conn.commit()
    cur.close()
    conn.close()

def log_degree_search(degree):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO degree_searches (degree) VALUES (%s)", (degree,))
    conn.commit()
    cur.close()
    conn.close()

def log_response_time(response_time):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO response_times (response_time) VALUES (%s)", (response_time,))
    conn.commit()
    cur.close()
    conn.close()

def get_metrics():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM total_requests")
    total_requests = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM error_count")
    error_count = cur.fetchone()[0]

    cur.execute("SELECT error_source, COUNT(*) FROM error_count GROUP BY error_source")
    error_breakdown = {row[0]: row[1] for row in cur.fetchall()}

    cur.execute("SELECT degree, COUNT(*) FROM degree_searches GROUP BY degree ORDER BY COUNT(*) DESC")
    degree_searches = {row[0]: row[1] for row in cur.fetchall()}

    cur.execute("SELECT AVG(response_time) FROM response_times")
    avg_response_time = cur.fetchone()[0]

    cur.execute("SELECT response_time, timestamp FROM response_times ORDER BY timestamp")
    response_times = [{"time": row[1].isoformat(), "value": row[0]} for row in cur.fetchall()]

    cur.close()
    conn.close()

    return {
        "total_requests": total_requests,
        "error_count": error_count,
        "error_breakdown": error_breakdown,
        "degree_searches": degree_searches,
        "response_times": response_times,
        "avg_response_time": round(avg_response_time, 4) if avg_response_time else None,
    }
