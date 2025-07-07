from functools import wraps
from typing import Optional
from dateutil.relativedelta import relativedelta
from config import PATH_REPORTS_LOG
from typing import Callable, Any
from pathlib import Path

import pandas as pd
import datetime
import logging
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_REPORTS_LOG, 'w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s-%(name)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def save_report_to_file(func: Callable) -> Callable:
    """ Декоратор сохраняет резултать обернутой функции в файл с именем
    дата+имя функции в деректорию reports в корне проекта """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info('Запущен декоратор save_report_to_file')
        current_date = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        file_name = Path(__file__).parent.parent / 'reports' / f'{current_date}_{wrapper.__name__}.json'
        result = func(*args, *kwargs)
        with open(file_name, 'w', encoding='utf-8') as file:
            try:
                if isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
                    file.write(result.to_json(force_ascii=False))
                else:
                    file.write(json.dumps(result, ensure_ascii=False))
            except Exception as e:
                message = f'Сбой при попытки конвертации данных в json: {e}'
                print(message)
                logger.error(message)
                file.write(json.dumps(message, ensure_ascii=False))
        logger.info('Работа декоратора успещно завершена')
        return result
    return wrapper


@save_report_to_file
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.Series:
    """ возвращает pd Series суммы расходов по категориям за три месяца до
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
    return result
