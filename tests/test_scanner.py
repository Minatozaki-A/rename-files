import pytest
from pathlib import Path
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from core.scanner import scanner_structure_directories

def test_scanner_structure_directories_not_exists(mocker: MockerFixture) -> None:
    base_path = MagicMock(spec=Path)
    base_path.exists.return_value = False

    with pytest.raises(FileNotFoundError, match="La ruta no existe o no es un directorio"):
        scanner_structure_directories(base_path)

def test_scanner_structure_directories_not_dir(mocker: MockerFixture) -> None:
    base_path = MagicMock(spec=Path)
    base_path.exists.return_value = True
    base_path.is_dir.return_value = False

    with pytest.raises(FileNotFoundError, match="La ruta no existe o no es un directorio"):
        scanner_structure_directories(base_path)

def test_scanner_structure_directories_success(mocker: MockerFixture, mock_config_json: None) -> None:
    base_path = MagicMock(spec=Path)
    base_path.exists.return_value = True
    base_path.is_dir.return_value = True
    base_path.name = "01. Mi Proyecto"

    config_path = Path("/mock/config.json")
    structure_path = Path("/mock/structure.json")

    mocker.patch("core.scanner.get_cached_config_value", return_value=[".git"])
    mock_build = mocker.patch("core.scanner.build_directory_tree", return_value={"src": {}})
    mock_save = mocker.patch("core.scanner.save_structure_directories")

    scanner_structure_directories(base_path, config_path, structure_path)

    # Se debió llamar a build_directory_tree con base_path y la lista ignore_dir
    mock_build.assert_called_once_with(base_path, [".git"])

    # Se debió llamar a save_structure_directories
    expected_structure = {
        "mi-proyecto": {"src": {}}
    }
    mock_save.assert_called_once_with(structure_path, expected_structure)

def test_scanner_structure_directories_no_config(mocker: MockerFixture) -> None:
    base_path = MagicMock(spec=Path)
    base_path.exists.return_value = True
    base_path.is_dir.return_value = True
    base_path.name = "Proyecto"

    mock_build = mocker.patch("core.scanner.build_directory_tree", return_value={"src": {}})
    mock_save = mocker.patch("core.scanner.save_structure_directories")

    # Llama sin config_path
    scanner_structure_directories(base_path)

    # Se debió llamar a build_directory_tree con base_path y lista vacía
    mock_build.assert_called_once_with(base_path, [])

    # No se debió llamar a guardar
    mock_save.assert_not_called()
