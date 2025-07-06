from typing import Optional
from config import PATH_TEST_XLSX
from dateutil.relativedelta import relativedelta

import pandas as pd
import datetime


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    if date:
        try:
            end_date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        except Exception as e:
            print(f'Ошибка при обработке даты: {e}')
            end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.now()
    start_date = end_date + relativedelta(months=-3)
    transactions['Дата операции'] = transactions['Дата операции'].map(
        lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S')
    )
    filtered_transactions = transactions.loc[
        (transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] < end_date)
        ]
    result = filtered_transactions.groupby(category)['Сумма операции'].sum()
    return result
