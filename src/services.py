import json

from tests.conftest import DATA_FROM_XLCX


def analysis_categories_for_cashback(data: list[dict], year: str, month: str) -> str:
    filtered_data = [x for x in data if x.get('Дата платежа') and x.get('Дата платежа')[3:] == f'{month}.{year}']
    categories = set([x.get('Категория') for x in filtered_data if x.get('Категория')])
    result = {}
    for category in sorted(categories):
        total_cashback = 0
        for operation in filtered_data:
            if operation.get('Сумма платежа') and operation.get('Категория') == category:
                total_cashback += operation.get('Сумма платежа') / -100
        result[category] = round(total_cashback, 2)
    return json.dumps(result, ensure_ascii=False)


# print(analysis_categories_for_cashback(DATA_FROM_XLCX, '2021', '12'))
