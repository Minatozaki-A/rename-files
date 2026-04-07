import pytest
from pathlib import Path
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

@pytest.fixture
def mock_config_json(mocker: MockerFixture) -> None:
    # Fixture que simula un config.json
    mock_data = '{"mount_point_label": "SSD", "ignore": [".git", "node_modules"]}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))
    mocker.patch.object(Path, "exists", return_value=True)

@pytest.fixture
def mock_directory_structure(mocker: MockerFixture) -> MagicMock:
    # Fixture que simula una estructura de directorios básica
    source_path = MagicMock(spec=Path)

    file1 = MagicMock(spec=Path)
    file1.is_dir.return_value = False
    file1.is_file.return_value = True
    file1.name = "file1.txt"

    dir1 = MagicMock(spec=Path)
    dir1.is_dir.return_value = True
    dir1.is_file.return_value = False
    dir1.name = "src"

    file2 = MagicMock(spec=Path)
    file2.is_dir.return_value = False
    file2.is_file.return_value = True
    file2.name = "main.py"

    dir1.iterdir.return_value = [file2]

    source_path.iterdir.return_value = [file1, dir1]
    return source_path
