import os
import telegram
from src.filter import classify_category

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def _get_bot():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    return telegram.Bot(token=TELEGRAM_BOT_TOKEN)


def send_article_alert(article):
    bot = _get_bot()
    title = article.get("title", "No title")
    summary = article.get("summary", "")[:200]
    link = article.get("link", "")
    source = article.get("source", "Unknown")
    category = classify_category(article)

    text = (
        f"🔔 *{_escape(title)}*\n\n"
        f"_{_escape(summary)}_\n\n"
        f"📌 {category} | {source}\n"
        f"[Baca selengkapnya]({link})"
    )

    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=False,
        )
        print(f"[telegram] Alert sent: {title}")
    except Exception as e:
        print(f"[telegram] ERROR sending alert: {e}")


def send_daily_digest(articles):
    if not articles:
        print("[telegram] No articles for digest today")
        return

    bot = _get_bot()
    from datetime import datetime

    today_str = datetime.utcnow().strftime("%d %b %Y")
    top = articles[:5]

    # Determine dominant category
    from src.filter import classify_category as _cat
    from collections import Counter
    cats = Counter(_cat(a) for a in articles)
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

    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
        print(f"[telegram] Daily digest sent ({len(articles)} articles)")
    except Exception as e:
        print(f"[telegram] ERROR sending digest: {e}")


def _escape(text):
    # Escape Markdown special chars that break formatting (but keep intentional *)
    for ch in ["_", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", "."]:
        text = text.replace(ch, "\\" + ch)
    return text
