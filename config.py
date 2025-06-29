from pathlib import Path

PATH_TEST_XLSX = Path(__file__).parent / 'data' / 'test_reader_excel.xlsx'
PATH_FILE_NOT_FOUND = Path(__file__).parent.parent / 'data' / 'reader_excel.xlsx'
PATH_OPERATIONS = Path(__file__).parent / 'data' / 'operations.xlsx'
PATH_UTILS_LOG = Path(__file__).parent / 'logs' / 'utils.log'
PATH_VIEWS_LOG = Path(__file__).parent / 'logs' / 'views.log'
PATH_USER_SETTINGS = Path(__file__).parent / 'user_settings.json'
ERROR_STUB = {
    "greeting": "Добрый вечер",
    "cards": [
        {
            "last_digits": None,
            "total_spent": 0,
            "cashback": 0
        },
        {
            "last_digits": None,
            "total_spent": 0,
            "cashback": 0
        }
    ],
    "top_transactions": [
        {
            "date": "",
            "amount": 0,
            "category": "",
            "description": ""
        },
        {
            "date": "",
            "amount": 0,
            "category": "",
            "description": ""
        },
        {
            "date": "",
            "amount": 0,
            "category": "",
            "description": ""
        },
        {
            "date": "",
            "amount": 0,
            "category": "",
            "description": ""
        },
        {
            "date": "",
            "amount": 0,
            "category": "",
            "description": ""
        }
    ],
    "currency_rates": [
        {
            "currency": "USD",
            "rate": 0
        },
        {
            "currency": "EUR",
            "rate": 0
        }
    ],
    "stock_prices": [
        {
            "stock": "AAPL",
            "price": 0
        },
        {
            "stock": "AMZN",
            "price": 0
        },
        {
            "stock": "GOOGL",
            "price": 0
        },
        {
            "stock": "MSFT",
            "price": 0
        },
        {
            "stock": "TSLA",
            "price": 0
        }
    ]
}