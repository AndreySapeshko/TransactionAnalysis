import datetime
import json
import requests

from src.utils import read_from_xlcx
from config import PATH_TEST_XLSX
from tests.conftest import DATA_FROM_XLCX

cards = [
    {
        "last_digits": "5814",
        "total_spent": 1262.00,
        "cashback": 12.62
    },
    {
        "last_digits": "7512",
        "total_spent": 7.94,
        "cashback": 0.08
    }
]

top_transaction = [
    {
        "date": "21.12.2021",
        "amount": 1198.23,
        "category": "Переводы",
        "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
        "date": "20.12.2021",
        "amount": 829.00,
        "category": "Супермаркеты",
        "description": "Лента"
    },
    {
        "date": "20.12.2021",
        "amount": 421.00,
        "category": "Различные товары",
        "description": "Ozon.ru"
    },
    {
        "date": "16.12.2021",
        "amount": -14216.42,
        "category": "ЖКХ",
        "description": "ЖКУ Квартира"
    },
    {
        "date": "16.12.2021",
        "amount": 453.00,
        "category": "Бонусы",
        "description": "Кешбэк за обычные покупки"
    }
]

currency_rates = [
    {
        "currency": "USD",
        "rate": 73.21
    },
    {
        "currency": "EUR",
        "rate": 87.08
    }
]

stock_prices = [
    {
        "stock": "AAPL",
        "price": 150.12
    },
    {
        "stock": "AMZN",
        "price": 3173.18
    },
    {
        "stock": "GOOGL",
        "price": 2742.39
    },
    {
        "stock": "MSFT",
        "price": 296.71
    },
    {
        "stock": "TSLA",
        "price": 1007.08
    }
]


def get_start_date(current_date: str) -> datetime:
    """ принимает дату в формате YYYY-MM-DD HH:MM:SS
    и возвращает дату начала отбора операций """

    str_start_date = current_date[:8] + '01'
    return datetime.datetime.strptime(str_start_date, '%Y-%m-%d')


def get_cards_expenses(operations: list[dict], start_date: datetime) -> list[dict]:
    """ принимает дату в формате YYYY-MM-DD HH:MM:SS и возвращает
    все расходы  и весь кешбек с начала месяца по каждой карте """

    result = []
    card_numbers = set([x.get('Номер карты') for x in operations if x.get('Номер карты')])
    for card_number in card_numbers:
        total_spent: float = 0
        cashback: float = 0
        for operation in operations:
            if start_date <= datetime.datetime.strptime(operation.get('Дата платежа'),'%d.%m.%Y'):
                if operation.get('Сумма операции') and operation.get('Номер карты') == card_number:
                    total_spent += operation.get('Сумма операции')
                if operation.get('Кэшбэк') and operation.get('Номер карты'):
                    cashback += operation.get('Кэшбэк')
        result.append(
            {
                'last_digits': card_number,
                'total_spent': total_spent * -1,
                'cashback': cashback
            }
        )
    return result


def get_top_transactions(operations: list[dict], start_date: datetime) -> list[dict]:
    top_transactions = []
    operations = [operation for operation in operations if operation.get('Дата операции') and
                  start_date <= datetime.datetime.strptime(operation.get('Дата операции'), '%d.%m.%Y %H:%M:%S')]
    sorted_operations = sorted(operations, key=lambda x: x.get('Сумма операции'), reverse=False)
    for i in range(len(sorted_operations)):
        if i == 5:
            break
        top_transactions.append(
            {
                'date': sorted_operations[i].get('Дата платежа'),
                'amount': sorted_operations[i].get('Сумма операции'),
                'category': sorted_operations[i].get('Категория'),
                'description': sorted_operations[i].get('Описание')
            }
        )
    return top_transactions


def get_currency_exchange_rates(codes_currencies: list) -> list[dict]:
    currencies = []
    rates = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    for code in codes_currencies:
        currencies.append(
            {
                'currency': code,
                'rate': rates['Valute'][code]['Value']
            }
        )
    return currencies

# print(get_currency_exchange_rates(['USD', 'EUR']))

def get_greeting(current_date: str) -> str:
    """ принимает дату в формате YYYY-MM-DD HH:MM:SS
    и возвращает соответствующее времени суток приветствие """

    hour = int(current_date.split()[1][:2])
    greeting = 'Доброй ночи'
    if 5 <= hour < 12:
        greeting = 'Доброе утро'
    elif 12 <= hour < 17:
        greeting = 'Добрый день'
    elif 17 <= hour < 23:
        greeting = 'Добрый вечер'
    return greeting


def get_data_home_page(current_date: str) -> json:
    """ функция принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными:
    Приветствие в формате
    — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
    По каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    Топ-5 транзакций по сумме платежа.
    Курс валют.
    Стоимость акций из S&P500. """
    result = {}
    result['greeting'] = 'Добрый день'
    result['cards'] = cards
    result['top_transactions'] = top_transaction
    result['currency_rates'] = currency_rates
    result['stock_prices'] = stock_prices
    return json.dumps(result, indent=4)
