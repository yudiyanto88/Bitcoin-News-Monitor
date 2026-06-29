import datetime
import time
from dotenv import load_dotenv

load_dotenv()

from src.fetcher import fetch_all_feeds
from src.filter import is_relevant, classify_category
from src.storage import is_seen, mark_seen, get_today_articles
from src.telegram_bot import send_article_alert
from src.digest import maybe_send_digest


def main():
    print(f"[main] Run started at {datetime.datetime.utcnow().isoformat()} UTC")

    articles = fetch_all_feeds()
    print(f"[main] Total articles fetched: {len(articles)}")

    new_relevant = 0
    for article in articles:
        url = article.get("link", "")
        if not url:
            continue

        if is_seen(url):
            continue

        if is_relevant(article.get("title", ""), article.get("summary", "")):
            article["category"] = classify_category(article)
            send_article_alert(article)
            mark_seen(article)
            new_relevant += 1
            print(f"[main] Relevant & sent: {article['title']}")
            time.sleep(7)
        else:
            # Still mark as seen so we don't re-evaluate it next run
            mark_seen(article)

    print(f"[main] New relevant articles this run: {new_relevant}")

    today_articles = get_today_articles()
    maybe_send_digest(today_articles)

    print("[main] Run complete")


if __name__ == "__main__":
    main()
