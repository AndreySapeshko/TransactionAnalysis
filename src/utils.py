import numpy as np
import pandas as pd
import os


def read_from_xlcx(filename: str) -> list[dict]:
    """ Читает данные из xlcx формата и возвращает список словарей.
    Если файл не существует или пустой вернет пустой список """

    result = []
    if os.path.exists(filename):
        try:
            df = pd.read_excel(filename)
            df = df.replace([np.nan, pd.NA, pd.NaT], None)
            result = [x for x in df.to_dict(orient='records') if x.get('Дата операции')]
            if result is None:
                result = []
        except Exception as e:
            print(f'Ошибка при чтении файла: {e}')
    return result
