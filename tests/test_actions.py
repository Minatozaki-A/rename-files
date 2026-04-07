import pytest
from pathlib import Path
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from core.actions import (
    find_ssd_mount_point,
    _unique_path,
    resolve_name_path,
    organize_for_depth_and_alphabetical,
    get_name_files,
    get_name_directories
)

def test_find_ssd_mount_point(mocker: MockerFixture) -> None:
    # Usar mocking para psutil.disk_partitions
    mock_partitions = mocker.patch("psutil.disk_partitions")

    # Configurar mock data
    part1 = MagicMock()
    part1.mountpoint = "/mnt/HDD"
    part2 = MagicMock()
    part2.mountpoint = "/mnt/MyData_SSD"

    mock_partitions.return_value = [part1, part2]

    # Validar que identifique correctamente el punto de montaje basado en el sufijo
    result = find_ssd_mount_point("SSD")
    assert result == Path("/mnt/MyData_SSD")

    # Validar caso de error sin etiqueta
    with pytest.raises(ValueError, match="label_ssd is empty"):
        find_ssd_mount_point("")

    # Validar que retorna None cuando no encuentra la etiqueta
    result_not_found = find_ssd_mount_point("NVME")
    assert result_not_found is None

def test_unique_path_no_collision(mocker: MockerFixture) -> None:
    # Si la ruta no existe, debe retornar la original
    path = Path("/tmp/documento.txt")
    mocker.patch.object(Path, "exists", return_value=False)

    assert _unique_path(path) == path

def test_unique_path_with_collision(mocker: MockerFixture) -> None:
    # Simular colisiones: documento.txt existe, pero documento(1).txt no
    path = Path("/tmp/documento.txt")

    def mock_exists(self: Path) -> bool:
        if self.name == "documento.txt":
            return True
        return False

    mocker.patch.object(Path, "exists", autospec=True, side_effect=mock_exists)

    result = _unique_path(path)
    assert result == Path("/tmp/documento(1).txt")

def test_resolve_name_path_file_no_collision(mocker: MockerFixture) -> None:
    path = Path("/tmp/Documento Importante!.txt")

    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)
    mocker.patch.object(Path, "exists", return_value=False)

    result = resolve_name_path(path)
    assert result == Path("/tmp/documento-importante.txt")

def test_resolve_name_path_directory(mocker: MockerFixture) -> None:
    path = Path("/tmp/01. Mi Carpeta")

    mocker.patch.object(Path, "is_file", return_value=False)
    mocker.patch.object(Path, "is_dir", return_value=True)
    mocker.patch.object(Path, "exists", return_value=False)

    result = resolve_name_path(path)
    assert result == Path("/tmp/mi-carpeta")

def test_resolve_name_path_empty_error(mocker: MockerFixture) -> None:
    path = Path("/tmp/---")
    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    with pytest.raises(ValueError, match="new name is empty"):
        resolve_name_path(path)

def test_organize_for_depth_and_alphabetical() -> None:
    paths = [
        Path("/a/b/c/d.txt"),
        Path("/a/b.txt"),
        Path("/a/b/c.txt"),
        Path("/z/y.txt"),
        Path("/a/c.txt")
    ]

    # Validar que los elementos se ordenen primero por profundidad y luego alfabéticamente
    result = organize_for_depth_and_alphabetical(paths)

    expected = [
        Path("/a/b/c/d.txt"),  # len parts = 5
        Path("/a/b/c.txt"),    # len parts = 4
        Path("/a/b.txt"),      # len parts = 3, 'b' < 'c' < 'z'
        Path("/a/c.txt"),      # len parts = 3, 'b' < 'c' < 'z'
        Path("/z/y.txt")       # len parts = 3, 'b' < 'c' < 'z'
    ]

    assert result == expected

def test_get_name_files(mocker: MockerFixture) -> None:
    source_path = MagicMock(spec=Path)
    config_path = Path("/mock/config.json")

    # Configurar mock de iterdir para retornar una estructura mixta
    file1 = MagicMock(spec=Path)
    file1.is_dir.return_value = False
    file1.is_file.return_value = True

    dir1 = MagicMock(spec=Path)
    dir1.is_dir.return_value = True
    dir1.is_file.return_value = False
    dir1.name = ".git"

    dir2 = MagicMock(spec=Path)
    dir2.is_dir.return_value = True
    dir2.is_file.return_value = False
    dir2.name = "src"

    file2 = MagicMock(spec=Path)
    file2.is_dir.return_value = False
    file2.is_file.return_value = True

    # iterdir for dir2
    dir2.iterdir.return_value = [file2]

    # iterdir for source_path
    source_path.iterdir.return_value = [file1, dir1, dir2]

    # Mocking config para ignorar ".git"
    mocker.patch("core.actions._resolve_config", return_value=[".git"])

    result = list(get_name_files(source_path, config_path, "ignore"))

    assert file1 in result
    assert file2 in result
    assert len(result) == 2

def test_get_name_directories(mocker: MockerFixture) -> None:
    source_path = MagicMock(spec=Path)
    config_path = Path("/mock/config.json")

    dir1 = MagicMock(spec=Path)
    dir1.is_dir.return_value = True
    dir1.name = "node_modules"

    dir2 = MagicMock(spec=Path)
    dir2.is_dir.return_value = True
    dir2.name = "src"

    dir3 = MagicMock(spec=Path)
    dir3.is_dir.return_value = True
    dir3.name = "components"
    dir3.iterdir.return_value = []

    dir2.iterdir.return_value = [dir3]
    source_path.iterdir.return_value = [dir1, dir2]

    mocker.patch("core.actions._resolve_config", return_value=["node_modules"])

    result = list(get_name_directories(source_path, config_path, "ignore"))

    assert dir2 in result
    assert dir3 in result
    assert dir1 not in result
    assert len(result) == 2
