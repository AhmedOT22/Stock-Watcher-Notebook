"""Stable paths preserve the existing root JSON files regardless of launch directory."""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
WATCHLIST_FILE = BASE_DIR / 'watchlist.json'
PORTFOLIO_FILE = BASE_DIR / 'portfolio.json'
