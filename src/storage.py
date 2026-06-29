import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seen_articles.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_articles (
            url TEXT PRIMARY KEY,
            title TEXT,
            published TEXT,
            fetched_at TEXT
        )
    """)
    conn.commit()
    return conn


def is_seen(url):
    conn = _connect()
    row = conn.execute("SELECT 1 FROM seen_articles WHERE url = ?", (url,)).fetchone()
    conn.close()
    return row is not None


def mark_seen(article):
    conn = _connect()
    conn.execute(
        "INSERT OR IGNORE INTO seen_articles (url, title, published, fetched_at) VALUES (?, ?, ?, ?)",
        (
            article["link"],
            article["title"],
            article.get("published", ""),
            datetime.datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def get_today_articles():
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    conn = _connect()
    rows = conn.execute(
        "SELECT url, title, published, fetched_at FROM seen_articles WHERE fetched_at LIKE ?",
        (today + "%",),
    ).fetchall()
    conn.close()
    return [{"link": r[0], "title": r[1], "published": r[2], "fetched_at": r[3]} for r in rows]
