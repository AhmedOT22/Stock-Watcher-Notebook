# Stock Watcher Notebook

Python tools for retrieving historical stock prices, calculating SMA/EMA/ATR and returns, and managing a local watchlist and share portfolio. Includes a notebook and a runnable example script.

## Setup and usage

Use Python 3.11+ from the repository root:

```bash
git clone https://github.com/AhmedOT22/Stock-Watcher-Notebook.git
cd Stock-Watcher-Notebook
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python main.py
python -m pytest -q
```

`main.py` downloads and plots a historical AAPL example without modifying saved holdings. Override it with `python main.py --symbol MSFT --start 2024-01-01 --end 2024-12-31`. The end date is exclusive. Manage watchlist and portfolio entries explicitly through their classes. To open `notebook/main.ipynb`, install Jupyter separately and select this environment as its kernel.

Network access is needed for price downloads. Quote freshness depends on the upstream service; “latest retrieved” does not mean a guaranteed real-time feed. The downloader explicitly requests adjusted prices, normalizes single-ticker MultiIndex columns, and rejects empty responses. Return values are fractional changes, and early rolling-window indicators have expected missing warm-up values.

## Local storage

`config.py` anchors the existing root `portfolio.json` and `watchlist.json` files to the repository, so launching from another directory does not select a different holdings file. The older `data/` JSON copies are preserved and are not merged or used by default. Custom filenames remain supported by both classes.

Writes create parent directories and use a temporary file plus atomic replacement. Malformed JSON raises an error instead of silently resetting saved data. This avoids partial file replacement but does not provide multi-process transaction locking. Back up holdings before using multiple writers.

Symbols are trimmed and uppercased. Added share quantities must be finite positive numbers. `view()` returns a copy so callers cannot accidentally modify internal holdings without saving. No brokerage orders are placed.

## Tests

The offline suite checks persistence, invalid share quantities, corrupt-file preservation, single-ticker download normalization, empty downloads, and indicator calculations without mutating price inputs. Download responses are mocked: live network availability and quote correctness are not verified by these tests.

Developed by [Ahmed Ouazzani](https://github.com/AhmedOT22).
