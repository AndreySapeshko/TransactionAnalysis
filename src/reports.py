from functools import wraps
from typing import Optional
from dateutil.relativedelta import relativedelta
from config import PATH_REPORTS_LOG, PATH_TEST_XLSX

import pandas as pd
import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_REPORTS_LOG, 'w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s-%(name)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def save_report_to_file(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_date = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        file_name = f'../reports/{current_date}_{wrapper.__name__}.json'
        result = func(*args, *kwargs)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(result.to_json(force_ascii=False))
        return result
    return wrapper


@save_report_to_file
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ возвращает DataFrame суммы расходов по категориям за три месяца до
    выбранной даты, если дата не выбрана до текоущей даты """

    logger.info('Запущена функция spending_by_category')
    if date:
        try:
            end_date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        except Exception as e:
            print(f'Ошибка при обработке даты: {e}')
            end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.now()
    start_date = end_date + relativedelta(months=-3)
    logger.info('Опредлен временной интервал')
    transactions['Дата операции'] = transactions['Дата операции'].map(
        lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S')
    )
    logger.info('Отобраны транзакции за временной интервал')
    filtered_transactions = transactions.loc[
        (transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] < end_date)
        ]
    result = filtered_transactions.groupby(category)['Сумма операции'].sum()
    logger.info('Работа функции spending_by_category завершена успешно')
    print(result.to_json(force_ascii=False))
    return result
