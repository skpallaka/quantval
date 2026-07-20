# cache.py
import sqlite3
import pandas as pd
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "price_cache.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            ticker TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (ticker, date)
        )
    """)
    # NEW: tracks which (ticker, start, end) ranges we've already fully fetched
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fetch_log (
            ticker TEXT,
            start TEXT,
            end TEXT,
            PRIMARY KEY (ticker, start, end)
        )
    """)
    conn.commit()
    conn.close()

def is_range_cached(ticker: str, start: str, end: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT 1 FROM fetch_log
        WHERE ticker = ? AND start <= ? AND end >= ?
        LIMIT 1
    """
    result = conn.execute(query, (ticker, start, end)).fetchone()
    conn.close()
    return result is not None

def log_fetch(ticker: str, start: str, end: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO fetch_log (ticker, start, end) VALUES (?, ?, ?)",
                 (ticker, start, end))
    conn.commit()
    conn.close()

def save_to_cache(df: pd.DataFrame, ticker: str):
    conn = sqlite3.connect(DB_PATH)
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    df["ticker"] = ticker
    df.index.name = "date"
    df.reset_index(inplace=True)
    df["date"] = df["date"].astype(str)

    conn.execute("BEGIN")
    for _, row in df.iterrows():
        conn.execute("""
            INSERT OR REPLACE INTO cache (ticker, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row["ticker"], row["date"], row["open"], row["high"],
              row["low"], row["close"], row["volume"]))
    conn.commit()
    conn.close()

def load_from_cache(ticker: str, start: str, end: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM cache WHERE ticker = ? AND date BETWEEN ? AND ? ORDER BY date"
    df = pd.read_sql_query(query, conn, params=(ticker, start, end))
    conn.close()
    return df