import datetime
import pytest

from deepdiff import DeepDiff
from unittest.mock import patch
from unittest.mock import Mock

from src.views import get_start_date, get_data_home_page, get_greeting, get_cards_expenses, get_top_transactions
from tests.conftest import DATA_FROM_XLCX, expected_top


@pytest.mark.parametrize('date, expected', [
    ('2021-01-23 22:34:55', '01.01.2021'),
    ('2022-12-01 22:34:55', '01.12.2022'),
    ('2023-03-02 22:34:55', '01.03.2023')
])
def test_get_start_date(date: str, expected: str) -> None:
    assert get_start_date(date).strftime('%d.%m.%Y') == expected


@patch('src.views.get_stock_prices')
@patch('src.views.get_currency_exchange_rates')
def test_get_data_home_page(mock_rates: Mock, mock_stock: Mock, data_home_page: str) -> None:
    mock_rates.return_value = [
        {'currency': 'USD', 'rate': 78.2},
        {'currency': 'EUR', 'rate': 91.06}
    ]
    mock_stock.return_value = [
        {"stock": "AAPL", "price": 201.96},
        {"stock": "AMZN", "price": 213.16},
        {"stock": "GOOGL", "price": 171.88},
        {"stock": "MSFT", "price": 491.85},
        {"stock": "TSLA", "price": 326.63}
    ]
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


def test_get_top_transactions() -> None:
    assert get_top_transactions(DATA_FROM_XLCX, get_start_date('2021-01-23 22:34:55')) == expected_top


def test_get_top_transactions_error() -> None:
    result = get_top_transactions(DATA_FROM_XLCX, None)
    assert result == []

