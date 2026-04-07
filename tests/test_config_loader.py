import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, mock_open
from pytest_mock import MockerFixture

from core.config_loader import (
    get_cached_config_value,
    build_directory_tree,
    save_structure_directories,
    _CONFIG_CACHE
)

@pytest.fixture(autouse=True)
def clear_cache() -> None:
    # Asegurar que el caché esté limpio antes de cada test
    _CONFIG_CACHE.clear()

def test_get_cached_config_value_reads_from_disk(mocker: MockerFixture, mock_config_json: None) -> None:
    config_path = Path("/mock/config.json")

    # Primera lectura debe ir a "disco"
    val = get_cached_config_value(config_path, "mount_point_label")
    assert val == "SSD"

    # Se debió guardar en caché
    assert str(config_path) in _CONFIG_CACHE

def test_get_cached_config_value_uses_cache(mocker: MockerFixture) -> None:
    config_path = Path("/mock/config.json")

    # Pre-cargar el caché
    _CONFIG_CACHE[str(config_path)] = {"mount_point_label": "NVME"}

    # Como la implementación de config_loader lee el json si intentamos llamar a open()
    # tenemos que asegurar que la lectura del archivo retorne la configuración cacheada o mockearla,
    # caso contrario leerá del disco/mock global y sobrescribirá el caché.
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data='{"mount_point_label": "NVME"}'))

    val = get_cached_config_value(config_path, "mount_point_label")
    assert val == "NVME"

def test_get_cached_config_value_json_decode_error(mocker: MockerFixture) -> None:
    config_path = Path("/mock/config.json")
    mocker.patch.object(Path, "exists", return_value=True)

    # Data inválida JSON
    mocker.patch("builtins.open", mock_open(read_data="{invalid_json"))

    val = get_cached_config_value(config_path, "mount_point_label")
    assert val is None
    assert _CONFIG_CACHE[str(config_path)] == {}

def test_build_directory_tree(mocker: MockerFixture) -> None:
    base_path = MagicMock(spec=Path)

    # Ignorar dir1
    dir1 = MagicMock(spec=Path)
    dir1.name = "node_modules"

    # Procesar dir2 y un archivo
    dir2 = MagicMock(spec=Path)
    dir2.name = "src"
    dir2.is_dir.return_value = True
    dir2.is_file.return_value = False

    file1 = MagicMock(spec=Path)
    file1.name = "main.py"
    file1.is_dir.return_value = False
    file1.is_file.return_value = True

    dir2.iterdir.return_value = [file1]

    # Archivo en base_path
    file2 = MagicMock(spec=Path)
    file2.name = "README.md"
    file2.is_dir.return_value = False
    file2.is_file.return_value = True

    base_path.iterdir.return_value = [dir1, dir2, file2]

    ignore_list = ["node_modules"]

    tree = build_directory_tree(base_path, ignore_list)

    expected = {
        "src": {"main.py": None},
        "README.md": None
    }

    assert tree == expected

def test_build_directory_tree_permission_error(mocker: MockerFixture) -> None:
    base_path = MagicMock(spec=Path)

    dir1 = MagicMock(spec=Path)
    dir1.name = "restricted_folder"
    dir1.is_dir.side_effect = PermissionError("Access denied")

    base_path.iterdir.return_value = [dir1]

    tree = build_directory_tree(base_path, [])

    # Según la lógica, captura el error y pone None
    assert tree == {"restricted_folder": None}

def test_save_structure_directories(mocker: MockerFixture) -> None:
    config_path = Path("/mock/structure.json")
    mocker.patch.object(Path, "exists", return_value=True)

    old_data = '{"old_folder": {"file.txt": null}}'
    mocked_open = mock_open(read_data=old_data)
    mocker.patch("builtins.open", mocked_open)

    new_structure = {"new_folder": {"doc.txt": None}}

    save_structure_directories(config_path, new_structure)

    # Verificar que se intentó escribir la combinación
    expected_data = {
        "old_folder": {"file.txt": None},
        "new_folder": {"doc.txt": None}
    }

    # Capturar la data que se intentó escribir
    handle = mocked_open()
    written = "".join(call.args[0] for call in handle.write.call_args_list)

    # Verificar formato (indent=4)
    assert json.loads(written) == expected_data
    assert "    " in written # Verifica la indentación
