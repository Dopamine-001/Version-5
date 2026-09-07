from __future__ import annotations

import sqlite3
import pandas as pd
import streamlit as st

DB_NAME = "proteins.db"

def get_connection():
    """Creates a local SQLite connection."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """Initializes the database tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                query TEXT
            )
        """)
        conn.commit()

def log_search(query: str):
    """Logs a protein search query."""
    if not query:
        return
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO search_history (query) VALUES (?)", (query,))
        conn.commit()

def get_recent_searches(limit: int = 10) -> pd.DataFrame:
    """Retrieves recent searches as a DataFrame."""
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT query, timestamp FROM search_history ORDER BY timestamp DESC LIMIT ?", 
            conn, 
            params=(limit,)
        )
