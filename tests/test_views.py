import datetime
import json
import pandas as pd
from plistlib import loads

import requests
import pytest

from deepdiff import DeepDiff
from unittest.mock import patch

from src.views import get_start_date, get_data_home_page, get_greeting, get_cards_expenses, get_top_transactions, get_currency_exchange_rates, get_stock_prices
from tests.conftest import DATA_FROM_XLCX, expected_top, expected_stocks


@pytest.mark.parametrize('date, expected', [
    ('2021-01-23 22:34:55', '01.01.2021'),
    ('2022-12-01 22:34:55', '01.12.2022'),
    ('2023-03-02 22:34:55', '01.03.2023')
])
def test_get_start_date(date: str, expected: str) -> None:
    assert get_start_date(date).strftime('%d.%m.%Y') == expected


def test_get_data_home_page(data_home_page: json) -> None:
    assert get_data_home_page('2021-01-23 22:34:55') == data_home_page


@pytest.mark.parametrize('date, expected', [
    ('YYYY-MM-DD 06:MM:SS', 'Доброе утро'),
    ('YYYY-MM-DD 12:MM:SS', 'Добрый день'),
    ('YYYY-MM-DD 22:MM:SS', 'Добрый вечер'),
    ('YYYY-MM-DD 04:MM:SS', 'Доброй ночи')
])
def test_get_greeting(date: str, expected: str) -> None:
    assert get_greeting(date) == expected


def test_get_cards_expenses(expected_cards: list) -> None:
    start_date = datetime.datetime.strptime('2021-01-23 22:34:55', '%Y-%m-%d %H:%M:%S')
    diff = DeepDiff(get_cards_expenses(DATA_FROM_XLCX, start_date), expected_cards, ignore_order=True)
    assert diff == {}


@patch('src.views.get_stock_prices')
@patch('src.views.get_currency_exchange_rates')
def test_get_top_transactions(mock_rates, mock_stock) -> None:
    mock_rates.return_value = [
        {"currency": "USD", "rate": 78.29},
        {"currency": "EUR", "rate": 89.84}
    ]
    mock_stock.return_value = [
        {"stock": "AAPL", "price": 201.5},
        {"stock": "AMZN", "price": 208.47},
        {"stock": "GOOGL", "price": 165.19},
        {"stock": "MSFT", "price": 486.0},
        {"stock": "TSLA", "price": 348.68}
    ]
    assert get_top_transactions(DATA_FROM_XLCX, get_start_date('2021-01-23 22:34:55')) == expected_top


def test_get_currency_exchange_rates() -> None:
    codes = ['USD', 'EUR']
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    expected_rates = [
        {
            'currency': codes[0],
            'rate': round(data['Valute'][codes[0]]['Value'], 2)
        },
        {
            'currency': codes[1],
            'rate': round(data['Valute'][codes[1]]['Value'], 2)
        }
    ]
    diff = DeepDiff(get_currency_exchange_rates(codes), expected_rates, ignore_order=True)
    assert diff == {}


@patch('yfinance.download')
def test_get_stock_prices(mock_download):
    # 1. Подготовка тестовых данных
    mock_df = pd.DataFrame({
        'Close': [{
            'AAPL': 201.69,
            'AMZN': 209.77,
            'GOOGL': 165.66,
            'MSFT': 475.93,
            'TSLA': 343.68
        }]
    })
    mock_download.return_value = mock_df

    tickers = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    result = get_stock_prices(tickers)

    assert DeepDiff(result, expected_stocks, ignore_order=True) == {}
