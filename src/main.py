import pandas as pd

from src.views import get_data_home_page
from src.services import analysis_categories_for_cashback
from src.reports import spending_by_category
from tests.conftest import DATA_FROM_XLCX
from config import PATH_TEST_XLSX


if __name__ == '__main__':
    data_for_home_page = get_data_home_page('2021-01-23 22:34:55')
    print(data_for_home_page)

    cashback_by_category = analysis_categories_for_cashback(DATA_FROM_XLCX, '2021', '12')
    print(cashback_by_category)

    df_transactions = pd.read_excel(PATH_TEST_XLSX)
    result_spending_by_category = spending_by_category(df_transactions, 'Категория', '31.12.2021 01:23:42')
    print(result_spending_by_category)
