RELEVANT_KEYWORDS = [
    # On-chain metrics
    "mvrv", "sopr", "nupl", "realized price", "puell",
    "long-term holder", "short-term holder", "exchange outflow",
    "exchange inflow", "coin days destroyed",

    # Bitcoin-specific institutional
    "bitcoin etf", "spot bitcoin", "ibit", "bitcoin treasury",
    "bitcoin reserve", "microstrategy", "mstr",

    # Macro yang langsung pengaruhi Bitcoin
    "federal reserve", "fed rate", "interest rate", "global liquidity",
    "inflation", "cpi", "dxy", "money supply",

    # Regulasi Bitcoin-specific
    "bitcoin regulation", "crypto regulation", "bitcoin ban",
    "bitcoin legislation", "clarity act", "bitcoin tax",

    # Supply & demand signal
    "bitcoin accumulation", "bitcoin whale", "large holder",
    "bitcoin sell", "bitcoin buying",
]

NOISE_KEYWORDS = [
    # Altcoin & ecosystem
    "ethereum", "solana", "xrp", "dogecoin", "cardano",
    "altcoin", "defi", "nft", "stablecoin", "tokenization",
    "web3", "layer 2", "l2", "airdrop", "presale",

    # Platform yang tidak relevan
    "polymarket", "kalshi", "prediction market",
    "securitize", "ethena", "aladdin",

    # Noise konten
    "price prediction", "technical analysis", "support level",
    "resistance", "breakout", "bullish pattern",
    "github", "developer", "open source", "rust",

    # AI & tech non-Bitcoin
    "anthropic", "openai", "artificial intelligence",
    "machine learning",
]

CATEGORIES = {
    "On-Chain": ["mvrv", "sopr", "nupl", "realized price", "puell", "long-term holder",
                 "short-term holder", "exchange outflow", "exchange inflow",
                 "coin days destroyed", "bitcoin whale", "large holder", "bitcoin accumulation"],
    "ETF & Institutional": ["bitcoin etf", "spot bitcoin", "ibit", "bitcoin treasury",
                             "bitcoin reserve", "microstrategy", "mstr"],
    "Macro": ["federal reserve", "fed rate", "interest rate", "global liquidity",
               "inflation", "cpi", "dxy", "money supply"],
    "Regulation": ["bitcoin regulation", "crypto regulation", "bitcoin ban",
                   "bitcoin legislation", "clarity act", "bitcoin tax"],
}


def _text(article):
    return (article.get("title", "") + " " + article.get("summary", "")).lower()


def classify_category(article):
    text = _text(article)
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text:
                return category
    return "General"


def is_relevant(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()

    has_noise = any(kw in text for kw in NOISE_KEYWORDS)
    if has_noise:
        return False

    matches = sum(1 for kw in RELEVANT_KEYWORDS if kw in text)
    return matches >= 2
