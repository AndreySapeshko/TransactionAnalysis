import pytest

from unittest.mock import patch
from deepdiff import DeepDiff
from pathlib import Path

from src.utils import read_from_xlcx
from tests.conftest import DATA_FROM_XLCX
from config import PATH_TEST_XLSX, PATH_FILE_NOT_FOUND


@pytest.mark.parametrize('path_name, expected', [
    (PATH_TEST_XLSX, DATA_FROM_XLCX),
    (PATH_FILE_NOT_FOUND, [])
])
def test_read_from_xlcx(path_name, expected: list) -> None:
    data_xlsx = read_from_xlcx(path_name)
    diff = DeepDiff(data_xlsx , expected, ignore_order=True)
    assert diff == {}


def test_read_file_with_error() -> None:
    """Тест обработки исключения при чтении файла"""

    with patch('pandas.read_excel') as mock_read:
        mock_read.side_effect = Exception("File read error")
        result = read_from_xlcx('invalid.xlsx')

    assert result == []
