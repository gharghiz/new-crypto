import sqlite3
from datetime import datetime, timezone

DB_PATH = "data.db"

def now_utc():
    return datetime.now(timezone.utc).isoformat()

# ============================
# Init
# ============================

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id TEXT PRIMARY KEY,
            title TEXT,
            source TEXT,
            url TEXT,
            posted_at TEXT,
            summary TEXT,
            sentiment TEXT
        )
        """)
        conn.commit()

# ============================
# Insert
# ============================

def save(news_id, title, source, url, summary="", sentiment=""):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        INSERT OR IGNORE INTO news
        (id, title, source, url, posted_at, summary, sentiment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (news_id, title, source, url, now_utc(), summary, sentiment))
        conn.commit()

# ============================
# Check
# ============================

def is_posted(news_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT 1 FROM news WHERE id=?", (news_id,))
        return cur.fetchone() is not None

# ============================
# Get news
# ============================

def get_news(limit=100):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
        SELECT * FROM news
        ORDER BY posted_at DESC
        LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]

# ============================
# Stats
# ============================

def get_stats():
    with sqlite3.connect(DB_PATH) as conn:
        total = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
        today = conn.execute("""
        SELECT COUNT(*) FROM news
        WHERE posted_at >= datetime('now','-1 day')
        """).fetchone()[0]

    return {"total": total, "today": today}
