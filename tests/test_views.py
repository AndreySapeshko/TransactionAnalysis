import json

import pytest
from freezegun import freeze_time

from src.views import get_start_date, get_data_home_page


@pytest.mark.parametrize('date, expected', [
    ('2021-01-23', '01.01.2021'),
    ('2022-12-01', '01.12.2022'),
    ('2023-03-02', '01.03.2023')
])
def test_get_start_date(date: str, expected: str) -> None:
    with freeze_time("2024-05-15"):
        assert get_start_date().strftime('%d.%m.%Y') == '01.05.2024'


def test_get_data_home_page(data_home_page: json) -> None:
    assert get_data_home_page('21.06.2025') == data_home_page
