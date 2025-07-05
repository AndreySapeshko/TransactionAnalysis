import json

import pytest
import requests
import pandas as pd

from unittest.mock import patch
from deepdiff import DeepDiff
from unittest.mock import Mock

from src.utils import read_from_xlcx, get_currency_exchange_rates, get_stock_prices, read_from_json
from tests.conftest import DATA_FROM_XLCX, expected_stocks, expected_json
from config import PATH_TEST_XLSX, PATH_FILE_NOT_FOUND, PATH_USER_SETTINGS


@pytest.mark.parametrize('path_name, expected', [
    (PATH_TEST_XLSX, DATA_FROM_XLCX),
    (PATH_FILE_NOT_FOUND, [])
])
def test_read_from_xlcx(path_name: str, expected: list) -> None:
    data_xlsx = read_from_xlcx(path_name)
    diff = DeepDiff(data_xlsx, expected, ignore_order=True)
    assert diff == {}


def test_read_file_with_error() -> None:
    """Тест обработки исключения при чтении файла"""

    with patch('pandas.read_excel') as mock_read:
        mock_read.side_effect = Exception("File read error")
        result = read_from_xlcx('invalid.xlsx')

    assert result == []


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


@pytest.mark.parametrize('mock, name_exception', [
    ('requests.get', Exception('File read error')),
    ('builtins.round', TypeError('Round error')),
    ('builtins.round', KeyError('Round error'))
])
def test_get_currency_exchange_error(mock: str, name_exception: Exception) -> None:
    codes = ['USD', 'EUR']
    expected_rates = [
        {
            'currency': codes[0],
            'rate': None
        },
        {
            'currency': codes[1],
            'rate': None
        }
    ]
    with patch(mock) as mock_get:
        mock_get.side_effect = name_exception
        result = get_currency_exchange_rates(codes)
        assert result == expected_rates


@patch('yfinance.download')
def test_get_stock_prices(mock_download: Mock) -> None:
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


@pytest.mark.parametrize('mock, name_exception', [
    ('yfinance.download', Exception('File read error')),
    ('builtins.round', TypeError('Round error')),
    ('builtins.round', KeyError('Round error'))
])
def test_get_stock_prices_error(mock: str, name_exception: Exception) -> None:
    tickers = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    expected_error_stock = [
        {'stock': 'AAPL', 'price': None},
        {'stock': 'AMZN', 'price': None},
        {'stock': 'GOOGL', 'price': None},
        {'stock': 'MSFT', 'price': None},
        {'stock': 'TSLA', 'price': None}
    ]
    with patch(mock) as mock_get:
        mock_get.side_effect = name_exception
        result = get_stock_prices(tickers)
        assert result == expected_error_stock


@pytest.mark.parametrize('file_name, expected', [(PATH_USER_SETTINGS, expected_json), ('invalid.json', [])])
def test_read_from_json(file_name: str, expected: list) -> None:
    assert read_from_json(file_name) == expected


@pytest.mark.parametrize('file_name, name_exception', [
    (PATH_USER_SETTINGS, FileNotFoundError('File not found')),
    (PATH_USER_SETTINGS, json.JSONDecodeError('File read error', '{"x": }', 3))])
def test_read_from_json_error(file_name: str, name_exception: Exception) -> None:
    with patch('json.load') as mock_get:
        mock_get.side_effect = name_exception
        assert read_from_json(file_name) == []
