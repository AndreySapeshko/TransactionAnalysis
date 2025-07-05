import pytest
import json

from tests.conftest import DATA_FROM_XLCX, expected_cashback
from src.services import analysis_categories_for_cashback


@pytest.mark.parametrize('month, year, data, expected', [
    ('12', '2021', DATA_FROM_XLCX, expected_cashback),
    ('12', '2022', DATA_FROM_XLCX, {})
])
def test_analysis_categories_for_cashback(month: str, year: str, data: list[dict], expected: dict) -> None:
    assert analysis_categories_for_cashback(data, year, month) == json.dumps(expected, ensure_ascii=False)