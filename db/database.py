import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS news (
    id TEXT PRIMARY KEY,
    title TEXT,
    source TEXT,
    url TEXT
)
""")


def is_posted(news_id):
    cur = conn.execute("SELECT 1 FROM news WHERE id=?", (news_id,))
    return cur.fetchone() is not None


def save(news_id, title, source, url):
    conn.execute(
        "INSERT OR IGNORE INTO news VALUES (?,?,?,?)",
        (news_id, title, source, url)
    )
    conn.commit()


def init_db():
    pass
