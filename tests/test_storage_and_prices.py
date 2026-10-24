import json
import numpy as np
import pandas as pd
import pytest
from models.portfolio import Portfolio
from models.watchlist import Watchlist
from utils.file_manager import load_json
from data_processing.indicators import calculate_indicators
from data_processing.stock_data import download_stock_data


def test_storage_and_validation(tmp_path):
    path = tmp_path / 'nested/portfolio.json'
    p = Portfolio(path)
    p.add(' aapl ', 2)
    assert Portfolio(path).view() == {'AAPL': 2}
    copy = p.view()
    copy['AAPL'] = 999
    assert p.view()['AAPL'] == 2
    for shares in [0, -1, np.nan, True]:
        with pytest.raises(ValueError):
            p.add('AAPL', shares)
    w = Watchlist(tmp_path / 'watchlist.json')
    w.add(' aapl ')
    w.add('AAPL')
    assert w.view() == ['AAPL']


def test_corrupt_json_is_not_silently_reset(tmp_path):
    path = tmp_path / 'broken.json'
    path.write_text('{bad')
    with pytest.raises(json.JSONDecodeError):
        load_json(path)
    assert path.read_text() == '{bad'


def test_single_ticker_multiindex_and_empty_response(monkeypatch):
    cols = pd.MultiIndex.from_product([['Close', 'High', 'Low'], ['AAPL']])
    frame = pd.DataFrame([[10., 12., 9.], [11., 13., 10.]], columns=cols)
    monkeypatch.setattr('data_processing.stock_data.yf.download', lambda *a, **k: frame)
    result = download_stock_data('AAPL', '2024-01-01', '2024-02-01')
    assert list(result.columns) == ['Close', 'High', 'Low']
    monkeypatch.setattr('data_processing.stock_data.yf.download', lambda *a, **k: pd.DataFrame())
    with pytest.raises(ValueError):
        download_stock_data('AAPL', '2024-01-01', '2024-02-01')


def test_indicators_do_not_mutate_prices():
    prices = pd.DataFrame({'Close': [10., 11., 12.], 'High': [12., 13., 14.], 'Low': [9., 10., 11.]})
    original = prices.copy()
    result = calculate_indicators(prices)
    pd.testing.assert_frame_equal(prices, original)
    assert result.loc[1, 'Daily_Return'] == pytest.approx(.1)
