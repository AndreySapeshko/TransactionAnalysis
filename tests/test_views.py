import json

import pytest
from freezegun import freeze_time

from src.views import get_start_date, get_data_home_page, get_greeting


@pytest.mark.parametrize('date, expected', [
    ('2021-01-23 22:34:55', '01.01.2021'),
    ('2022-12-01 22:34:55', '01.12.2022'),
    ('2023-03-02 22:34:55', '01.03.2023')
])
def test_get_start_date(date: str, expected: str) -> None:
    assert get_start_date(date).strftime('%d.%m.%Y') == expected


def test_get_data_home_page(data_home_page: json) -> None:
    assert get_data_home_page('21.06.2025') == data_home_page


@pytest.mark.parametrize('date, expected', [
    ('YYYY-MM-DD 06:MM:SS', 'Доброе утро'),
    ('YYYY-MM-DD 12:MM:SS', 'Добрый день'),
    ('YYYY-MM-DD 22:MM:SS', 'Добрый вечер'),
    ('YYYY-MM-DD 04:MM:SS', 'Доброй ночи')
])
def test_get_greeting(date: str, expected: str) -> None:
    assert get_greeting(date) == expected
