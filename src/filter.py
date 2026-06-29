import re

RELEVANT_KEYWORDS = [
    "mvrv", "sopr", "nupl", "realized price", "puell",
    "long-term holder", "short-term holder", "exchange outflow",
    "exchange inflow", "dormant", "coin days destroyed",
    "etf", "blackrock", "fidelity", "spot bitcoin",
    "federal reserve", "fed", "interest rate", "liquidity",
    "inflation", "cpi", "dxy",
    "sec", "cftc", "regulation", "ban", "approval",
    "legislation", "congress", "senate",
    "microstrategy", "institutional", "treasury", "accumulation",
    "whale", "large holder",
]

NOISE_KEYWORDS = [
    "altcoin", "ethereum", "solana", "xrp", "dogecoin",
    "nft", "defi", "meme coin", "airdrop", "presale",
    "price prediction", "technical analysis", "support level",
    "resistance", "breakout", "bullish pattern",
]

CATEGORIES = {
    "On-Chain": ["mvrv", "sopr", "nupl", "realized price", "puell", "long-term holder",
                 "short-term holder", "exchange outflow", "exchange inflow", "dormant",
                 "coin days destroyed", "whale", "large holder", "accumulation"],
    "ETF & Institutional": ["etf", "blackrock", "fidelity", "spot bitcoin", "microstrategy",
                             "institutional", "treasury"],
    "Macro": ["federal reserve", "fed", "interest rate", "liquidity", "inflation", "cpi", "dxy"],
    "Regulation": ["sec", "cftc", "regulation", "ban", "approval", "legislation",
                   "congress", "senate"],
}


def _text(article):
    return (article.get("title", "") + " " + article.get("summary", "")).lower()


def _contains_any(text, keywords):
    for kw in keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return True
    return False


def classify_category(article):
    text = _text(article)
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                return category
    return "General"


def is_relevant(article):
    text = _text(article)
    has_relevant = _contains_any(text, RELEVANT_KEYWORDS)
    has_noise = _contains_any(text, NOISE_KEYWORDS)
    return has_relevant and not has_noise
