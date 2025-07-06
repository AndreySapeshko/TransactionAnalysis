import datetime
import os
import pytest
import pandas as pd

from config import PATH_TEST_XLSX
from src.reports import spending_by_category, save_report_to_file
from unittest.mock import patch


@pytest.mark.parametrize('transactions, category, date, expected', [
    (PATH_TEST_XLSX, 'Категория', '31.12.2021 01:23:42',
     {'Каршеринг': -7.07, 'Переводы': -20800.0}),
    (PATH_TEST_XLSX, 'Категория', '31.12.2021 15:23:42',
     {'Каршеринг': -7.07, 'Переводы': -20800.0, 'Различные товары': -564.0}),
    (PATH_TEST_XLSX, 'Категория', 'invalid date', {}),
    (PATH_TEST_XLSX, 'Категория', None, {})
])
def test_spending_by_category(transactions: str, category: str, date: str, expected: dict) -> None:
    df_transactions = pd.read_excel(transactions)
    result = spending_by_category(df_transactions, category, date)
    assert result.to_dict() == expected


def test_save_report_to_file():
    @save_report_to_file
    def func_for_test():
        return pd.DataFrame({'test': ['test']})

    current_date = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    file_name = f'../reports/{current_date}_{func_for_test.__name__}.json'
    result = func_for_test()
    if os.path.exists(file_name):
        with open(file_name) as f:
            expected = f.read()
    assert result.to_json() == expected
