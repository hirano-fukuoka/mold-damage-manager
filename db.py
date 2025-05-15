import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect("data/mold_data.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usage INTEGER,
        part TEXT,
        damage TEXT,
        action TEXT,
        result TEXT
    )""")
    conn.commit()
    conn.close()

def insert_report(report):
    conn = sqlite3.connect("data/mold_data.db")
    conn.execute("""
        INSERT INTO reports (usage, part, damage, action, result)
        VALUES (?, ?, ?, ?, ?)
    """, (report["usage"], report["part"], report["damage"], report["action"], report["result"]))
    conn.commit()
    conn.close()

def search_reports(keyword):
    conn = sqlite3.connect("data/mold_data.db")
    return pd.read_sql_query("""
        SELECT * FROM reports
        WHERE damage LIKE ? OR action LIKE ? OR result LIKE ?
    """, conn, params=[f"%{keyword}%"] * 3)

def get_all_reports():
    conn = sqlite3.connect("data/mold_data.db")
    return pd.read_sql_query("SELECT * FROM reports", conn)

def get_stats():
    df = get_all_reports()
    total = len(df)
    success = len(df[df["result"].str.contains("成功", na=False)])
    rate = round(success / total * 100, 1) if total else 0
    by_action = df.groupby("action").size().reset_index(name="count") if not df.empty else None
    return {"total": total, "success": success, "rate": rate, "by_action": by_action}
