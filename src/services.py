import json
import datetime
import logging

from config import PATH_SERVICES_LOG


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_SERVICES_LOG, 'w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s-%(name)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def analysis_categories_for_cashback(data: list[dict], year: str, month: str) -> str:
    """ из списка операций за выбранный месяц в выбранном году подсчитываем размер кешбека
    по каждой категории. Результат возвращает словарь в json формате. """

    logger.info('Запущена функция analysis_categories_for_cashback')
    try:
        start_date = datetime.datetime(int(year), int(month), 1)
        filtered_data = [x for x in data if x.get('Дата платежа')
                         and x.get('Дата платежа')[3:] == f'{start_date.month}.{start_date.year}']
        logger.info('Выбраны операции за указанный переиод')
    except Exception as e:
        logger.error(f'Ошибка при обработке даты: {e}')
        print(f'Ошибка при обработке даты: {e}')
        filtered_data = []
    categories = set([x.get('Категория') for x in filtered_data if x.get('Категория')])
    result = {}
    logger.info('Суммируем кешбек по категориям')
    for category in sorted(categories):
        total_cashback = 0
        for operation in filtered_data:
            if operation.get('Сумма платежа') and operation.get('Категория') == category:
                total_cashback += operation.get('Сумма платежа') / -100
        result[category] = round(total_cashback, 2)
    logger.info('Работа функции analysis_categories_for_cashback завершена успешно')
    return json.dumps(result, ensure_ascii=False)
