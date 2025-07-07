import numpy as np
import pandas as pd
import os
import requests
import yfinance as yf
import json
import logging

from config import PATH_UTILS_LOG


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_UTILS_LOG, 'w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s-%(name)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def read_from_xlcx(filename: str) -> list[dict]:
    """ Читает данные из xlcx формата и возвращает список словарей.
    Если файл не существует или пустой вернет пустой список """

    logger.info('Запущена функция read_from_xlcx')
    result = []
    logger.info(f'Проверяем существует ли переданный файл {filename}')
    if os.path.exists(filename):
        try:
            logger.info(f'Читаем данные из файла {filename}')
            df = pd.read_excel(filename)
            df = df.replace([np.nan, pd.NA, pd.NaT], None)
            result = [x for x in df.to_dict(orient='records') if x.get('Дата операции')]
            logger.info('Данные по запросу получены')
            if result is None:
                logger.info('Содержимое файла None')
                result = []
        except Exception as e:
            logger.error(f'Возникла ошибка при чтении файла: {e}')
            print(f'Ошибка при чтении файла: {e}')
            return result
        logger.info('Работа функции read_from_xlcx завершена успешно')
    return result


def get_currency_exchange_rates(codes_currencies: list) -> list[dict]:
    """ получаем курсы валют к рублю по кодам из переданнгог списка по API
    с сайта ЦБР и возвращаем данные в виде списка словарей """

    logger.info('Запущена функция get_currency_exchange_rates')
    currencies = []
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        response.raise_for_status()
        rates = response.json()
        logger.info('Данные по запросу успешно получены')
    except Exception as e:
        logger.error(f'Ошибка при получении запроса: {e}')
        print(f'Ошибка при получении запроса: {e}')
        return [{'currency': code, 'rate': None} for code in codes_currencies]
    if not rates.get('Valute'):
        logger.warning('Отсутствуют данные о валютах в ответе')
        print('Отсутствуют данные о валютах в ответе')
        return [{'currency': code, 'rate': None} for code in codes_currencies]
    for code in codes_currencies:
        try:
            rate = round(rates['Valute'][code]['Value'], 2)
            currencies.append({'currency': code, 'rate': rate})
        except (KeyError, TypeError) as e:
            logger.error(f'Ошибка обработки валюты {code}: {e}')
            print(f'Ошибка обработки валюты {code}: {e}')
            currencies.append({'currency': code, 'rate': None})
    logger.info('Функция get_currency_exchange_rates успешно завершила работу')
    return currencies


def get_stock_prices(tickers: list) -> list:
    """ получаем курсы акций по тикерам из переданнгог списка по API с
    Yahoo financevи возвращаем данные в виде списка словарей """

    logger.info('Запущена функция get_stock_prices')
    stocks = []
    try:
        data = yf.download(tickers, period="1d", auto_adjust=False)
        data_list = json.loads(data['Close'].to_json(orient="records"))
        logger.info('Данные по запросу получены')
    except Exception as e:
        logger.error(f'Ошибка при получении запраса: {e}')
        print(f'Ошибка при получении запраса: {e}')
        return [{'stock': ticker, 'price': None} for ticker in tickers]
    if not data_list or len(data_list) == 0:
        logger.info('Список пустой или None')
        return [{'stock': ticker, 'price': None} for ticker in tickers]
    for ticker in tickers:
        if data_list[0].get(ticker):
            try:
                stocks.append({'stock': ticker, 'price': round(data_list[0].get(ticker), 2)})
            except (KeyError, TypeError) as e:
                logger.error(f'Ошибка при обработке акций: {e}')
                print(f'Ошибка при обработке акций: {e}')
                stocks.append({'stock': ticker, 'price': None})
        else:
            stocks.append({'stock': ticker, 'price': None})
    logger.info('Функция get_stock_prices успешно завершила работу')
    return stocks


def read_from_json(filename: str) -> list[dict]:
    """ конвертирует json файл в python, если файла нет или пустой вернет пустой список """

    logger.info('Запущена функция read_from_json')
    json_data: list[dict] = []
    logger.info(f'проверяем существует ли файл {filename}')
    if os.path.exists(filename):
        try:
            logger.info('открываем файл для чтения')
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as jde:
            logger.error(f'произошла ошибка при открытии файла {jde}')
            return json_data
        except FileNotFoundError as fnf:
            logger.error(f'произошла ошибка при открытии файла {fnf}')
            return json_data
        if type(data) is dict and len(data) != 0:
            json_data = [data]
        logger.info('конвертация успешно завершена')
    return json_data
