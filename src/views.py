import datetime
import json
import logging

from src.utils import read_from_xlcx, get_currency_exchange_rates, get_stock_prices, read_from_json
from config import PATH_TEST_XLSX, PATH_VIEWS_LOG, PATH_USER_SETTINGS, ERROR_STUB


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_VIEWS_LOG, 'w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s-%(name)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_start_date(current_date: str) -> datetime.datetime:
    """ принимает дату в формате YYYY-MM-DD HH:MM:SS
    и возвращает дату начала отбора операций """

    logger.info('Запущена функция get_start_date')
    try:
        str_start_date = current_date[:8] + '01'
        start_date = datetime.datetime.strptime(str_start_date, '%Y-%m-%d')
    except Exception as e:
        logger.error(f'Произошла ошибка при обработке даты: {e}')
        print(f'Произошла ошибка при обработке даты: {e}')
    logger.info('Функция get_start_date завершена успешно')
    return start_date


def get_cards_expenses(operations: list[dict], start_date: datetime.datetime) -> list[dict]:
    """ принимает дату в формате YYYY-MM-DD HH:MM:SS и возвращает
    все расходы  и весь кешбек с начала месяца по каждой карте """

    logger.info('Запущена функция get_cards_expenses')
    result = []
    card_numbers = set([x.get('Номер карты') for x in operations if x.get('Номер карты')])
    for card_number in sorted(card_numbers):
        logger.info(f'Обрабатываем счет: {card_number}')
        total_spent: float = 0
        cashback: float = 0
        for operation in operations:
            try:
                if start_date <= datetime.datetime.strptime(operation.get('Дата платежа'), '%d.%m.%Y'):
                    if operation.get('Сумма операции') and operation.get('Номер карты') == card_number:
                        total_spent += operation.get('Сумма операции')
                    if operation.get('Кэшбэк') and operation.get('Номер карты'):
                        cashback += operation.get('Кэшбэк')
            except Exception as e:
                logger.error(f'Ошибка обработки "даты платежи" или "Сумма операции" или "Кэшбэк": {e}')
                print(f'Ошибка обработки "даты платежи" или "Сумма операции" или "Кэшбэк": {e}')
        result.append(
            {
                'last_digits': card_number,
                'total_spent': total_spent * -1,
                'cashback': cashback
            }
        )
        logger.info(f'Счет {card_number} успешно обработан')
    logger.info('Функция get_cards_expenses успешно завершена')
    return result


def get_top_transactions(operations: list[dict], start_date: datetime.datetime) -> list[dict]:
    """ Выбираем из списка транзакций пять самых крупных с начала месяца
    в переданной дате, возвращаем в виде списка словарей """

    logger.info('Запущена функция get_top_transactions')
    top_transactions = []
    filtered_operations = []
    logger.info('Отфильтровываем операции по дате')
    for operation in operations:
        try:
            date_operation = datetime.datetime.strptime(operation.get('Дата операции'), '%d.%m.%Y %H:%M:%S')
            if operation.get('Дата операции') and operation.get('Сумма операции') and start_date <= date_operation:
                filtered_operations.append(operation)
        except Exception as e:
            logger.error(f'Ошибка обработки "Дата операции": {e}')
            print(f'Ошибка обработки "Дата операции": {e}')
            continue
    logger.info('Сортеруем операции по сумме')
    sorted_operations = sorted(filtered_operations, key=lambda x: x.get('Сумма операции'), reverse=False)
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
    logger.info('Функция get_top_transactions успешно завершена')
    return top_transactions


def get_greeting(current_date: str) -> str:
    """ принимает дату в формате YYYY-MM-DD HH:MM:SS
    и возвращает соответствующее времени суток приветствие """

    logger.info('Запущена функция get_greeting')
    try:
        hour = int(current_date.split()[1][:2])
    except Exception as e:
        logger.error(f'Не верный формат даты: {e}')
        print(f'Не верный формат даты: {e}')
        return 'Добрый день'
    greeting = 'Доброй ночи'
    if 5 <= hour < 12:
        greeting = 'Доброе утро'
    elif 12 <= hour < 17:
        greeting = 'Добрый день'
    elif 17 <= hour < 23:
        greeting = 'Добрый вечер'
    logger.info('Функция get_greeting успешно завершена')
    return greeting


def get_data_home_page(current_date: str) -> str:
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

    logger.info('Запущена функция get_data_home_page')
    logger.info('Получаем данные из operations и user_settings')
    user_settings = read_from_json(PATH_USER_SETTINGS)
    try:
        user_currencies = user_settings[0].get('user_currencies')
        user_stocks = user_settings[0].get('user_stocks')
    except Exception as e:
        logger.error(f'Ошибка при обработке user_settings: {e}')
        print(f'Ошибка при обработке user_settings: {e}')
        user_currencies = ['USD', 'EUR']
        user_stocks = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    start_date = get_start_date(current_date)
    operations = read_from_xlcx(PATH_TEST_XLSX)
    result = {}
    logger.info('Формируем ответ')
    result['greeting'] = get_greeting(current_date)
    result['cards'] = get_cards_expenses(operations, start_date)
    result['top_transactions'] = get_top_transactions(operations, start_date)
    result['currency_rates'] = get_currency_exchange_rates(user_currencies)
    result['stock_prices'] = get_stock_prices(user_stocks)
    try:
        result_json = json.dumps(result, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f'Ошибка при конвертации в json: {e}')
        print(f'Ошибка при конвертации в json: {e}')
        result_json = ERROR_STUB
    logger.info('Функция get_data_home_page успешно завершена')
    return result_json
