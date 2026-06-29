import os
import requests
from src.filter import classify_category
from src.summarizer import summarize_article

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def _send(text, disable_preview=False):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": disable_preview,
    }
    resp = requests.post(url, json=payload, timeout=10)
    if not resp.ok:
        print(f"[telegram] ERROR {resp.status_code}: {resp.text}")
    return resp.ok


def send_article_alert(article):
    title = article.get("title", "No title")
    link = article.get("link", "")
    source = article.get("source", "Unknown")
    category = classify_category(article)

    ai_summary = summarize_article(article)

    if ai_summary:
        text = (
            f"🔔 *{_escape(title)}*\n\n"
            f"📌 {category} | {source}\n\n"
            f"🤖 {_escape(ai_summary)}\n\n"
            f"[Baca selengkapnya]({link})"
        )
    else:
        summary = article.get("summary", "")[:200]
        text = (
            f"🔔 *{_escape(title)}*\n\n"
            f"_{_escape(summary)}_\n\n"
            f"📌 {category} | {source}\n"
            f"[Baca selengkapnya]({link})"
        )

    if _send(text):
        print(f"[telegram] Alert sent: {title}")


def send_daily_digest(articles):
    if not articles:
        print("[telegram] No articles for digest today")
        return

    from datetime import datetime
    from collections import Counter

    today_str = datetime.utcnow().strftime("%d %b %Y")
    top = articles[:5]

    cats = Counter(classify_category(a) for a in articles)
    dominant_cat, dominant_count = cats.most_common(1)[0]

    header = (
        f"📰 *BITCOIN NEWS — {today_str}*\n"
        f"_{len(articles)} artikel relevan hari ini_\n"
        f"Kategori dominan: *{dominant_cat}* ({dominant_count} artikel)\n\n"
    )

    items = []
    for i, a in enumerate(top, 1):
        title = a.get("title", "No title")
        link = a.get("link", "")
        summary = a.get("summary", "")[:120]
        items.append(f"{i}. [{_escape(title)}]({link})\n   _{_escape(summary)}..._")

    text = header + "\n\n".join(items)

    if _send(text, disable_preview=True):
        print(f"[telegram] Daily digest sent ({len(articles)} articles)")


def _escape(text):
    for ch in ["_", "*", "`", "["]:
        text = text.replace(ch, "\\" + ch)
    return text
