from typing import Optional
from dateutil.relativedelta import relativedelta
from config import PATH_REPORTS_LOG

import pandas as pd
import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_REPORTS_LOG, 'w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s-%(name)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


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
    return result
