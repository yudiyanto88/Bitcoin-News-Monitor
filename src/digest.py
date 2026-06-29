import datetime
from src.storage import get_today_articles
from src.telegram_bot import send_daily_digest


def maybe_send_digest(today_articles):
    """Send digest only on the 00:00 UTC run."""
    current_hour = datetime.datetime.utcnow().hour
    if current_hour != 0:
        print(f"[digest] Skipping digest — current UTC hour is {current_hour}, not 0")
        return

    print(f"[digest] 00:00 UTC run — sending daily digest with {len(today_articles)} articles")
    send_daily_digest(today_articles)
