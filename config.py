import os
from dotenv import load_dotenv

load_dotenv()

# ============================
# Environment
# ============================

def get_env(name: str, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"❌ Missing required env variable: {name}")
    return value

# ============================
# Telegram
# ============================

TELEGRAM_BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN", required=True)
TELEGRAM_CHAT_ID   = get_env("TELEGRAM_CHAT_ID", required=True)

# ============================
# OpenAI
# ============================

OPENAI_API_KEY = get_env("OPENAI_API_KEY")

# ============================
# App Settings
# ============================

INTERVAL_MINUTES = int(get_env("INTERVAL_MINUTES", 5))
MAX_POSTS_PER_CYCLE = int(get_env("MAX_POSTS_PER_CYCLE", 5))

SIMILARITY_THRESHOLD = float(get_env("SIMILARITY_THRESHOLD", 0.8))

# ============================
# RSS Sources
# ============================

RSS_FEEDS = [
    {"name": "CoinTelegraph", "url": "https://cointelegraph.com/rss"},
    {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
    {"name": "Decrypt", "url": "https://decrypt.co/feed"},
    {"name": "CryptoSlate", "url": "https://cryptoslate.com/feed"},
    {"name": "Bitcoin Magazine", "url": "https://bitcoinmagazine.com/feed"},
]

# ============================
# Keywords (basic filtering)
# ============================

IMPORTANT_KEYWORDS = [
    "bitcoin", "btc", "ethereum", "eth",
    "crypto", "blockchain", "web3",
    "etf", "sec", "hack", "crash", "pump",
    "regulation", "ban", "market"
]

COIN_MAP = {
    "bitcoin": "bitcoin",
    "btc": "bitcoin",
    "ethereum": "ethereum",
    "eth": "ethereum",
    "bnb": "binancecoin",
    "solana": "solana",
    "sol": "solana",
    "xrp": "ripple",
    "ripple": "ripple",
    "cardano": "cardano",
    "ada": "cardano",
    "dogecoin": "dogecoin",
    "doge": "dogecoin",
}
