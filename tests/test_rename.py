from pathlib import Path
from pytest_mock import MockerFixture
from utils.text_utils import clean_name, clean_file_name, clean_directory_name
from core.actions import resolve_name_path

def test_clean_name() -> None:
    """Verifica la normalización Unicode, eliminación de acentos, caracteres especiales y mayúsculas."""
    assert clean_name("C++ Programación") == "c-programacion"
    assert clean_name("  Espacios   Múltiples  ") == "espacios-multiples"
    assert clean_name("¿Qué es esto?!") == "que-es-esto"
    assert clean_name("Árbol_Verde-123") == "arbol-verde-123"

def test_clean_file_name() -> None:
    """Verifica que el nombre del archivo se limpie preservando su extensión."""
    assert clean_file_name(Path("C++ Programación.txt")) == "c-programacion.txt"
    assert clean_file_name(Path("Imagen_Con_Acentos_ÁÉÍ.PNG")) == "imagen-con-acentos-aei.png"
    assert clean_file_name(Path("  documento  .md")) == "documento.md"
    assert clean_file_name(Path("archivo.sin.extension")) == "archivo-sin.extension"

def test_clean_directory_name() -> None:
    """Verifica la eliminación de prefijos numéricos y limpieza en nombres de directorios."""
    assert clean_directory_name(Path("01 Directorio Inicial")) == "directorio-inicial"
    assert clean_directory_name(Path("02 - Carpeta Secundaria")) == "carpeta-secundaria"
    assert clean_directory_name(Path("123. Tercer Directorio")) == "tercer-directorio"
    assert clean_directory_name(Path("Carpeta_Normal")) == "carpeta-normal"


def test_resolve_name_path_no_collision(mocker: MockerFixture) -> None:
    """Verifica que si no hay colisión, devuelva el nombre limpio correctamente.

    Se simula pathlib.Path para evitar acceso al disco."""
    base_path = Path("/falso/directorio/C++ Programación.txt")

    # Simular is_file e is_dir
    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    # Simular que el path resultante (c-programacion.txt) no existe
    mocker.patch.object(Path, "exists", return_value=False)

    result = resolve_name_path(base_path)

    assert result == Path("/falso/directorio/c-programacion.txt")

def test_resolve_name_path_single_collision(mocker: MockerFixture) -> None:
    """Simula una colisión simple: el archivo base ya existe.

    Debe generar el nombre con el sufijo '(1)'."""
    base_path = Path("/falso/directorio/documento.txt")

    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    # exists() es llamado sobre la instancia del Path.
    # El primer exists() es para 'documento.txt', que ya existe.
    # El segundo es para 'documento(1).txt', que debe devolver False.
    def mock_exists(self: Path) -> bool:
        if self.name == "documento.txt":
            return True
        return False

    mocker.patch.object(Path, "exists", autospec=True, side_effect=mock_exists)
    mocker.patch.object(Path, "samefile", return_value=False)

    # El código hace: if final_name.name == base_path.name: return final_name
    # Para que llegue a _unique_path, el nombre base_path debe ser diferente
    # o tenemos que crear una situación de colisión real.
    # Dado que "documento.txt" limpiado es "documento.txt", retorna temprano.
    # Usemos un nombre que cambie al limpiarlo, por ejemplo:
    base_path_cambiado = Path("/falso/directorio/Documento .txt")

    result = resolve_name_path(base_path_cambiado)

    assert result == Path("/falso/directorio/documento(1).txt")

def test_resolve_name_path_multiple_collisions(mocker: MockerFixture) -> None:
    """Simula colisiones múltiples donde el original y el (1) ya existen.

    Debe generar el nombre con el sufijo '(2)'."""
    base_path = Path("/falso/directorio/documento.txt")

    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    def mock_exists(self: Path) -> bool:
        if self.name in ["documento.txt", "documento(1).txt"]:
            return True
        return False

    mocker.patch.object(Path, "exists", autospec=True, side_effect=mock_exists)
    mocker.patch.object(Path, "samefile", return_value=False)

    base_path_cambiado = Path("/falso/directorio/Documento .txt")

    result = resolve_name_path(base_path_cambiado)

    assert result == Path("/falso/directorio/documento(2).txt")

def test_resolve_name_path_collision_md_extension(mocker: MockerFixture) -> None:
    """Simula una colisión con un archivo de extensión .md.

    Debe generar el nombre con el sufijo '(1)' y conservar .md."""
    base_path = Path("/falso/directorio/documento.md")

    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    def mock_exists(self: Path) -> bool:
        if self.name == "documento.md":
            return True
        return False

    mocker.patch.object(Path, "exists", autospec=True, side_effect=mock_exists)
    mocker.patch.object(Path, "samefile", return_value=False)

    base_path_cambiado = Path("/falso/directorio/Documento .md")

    result = resolve_name_path(base_path_cambiado)

    assert result == Path("/falso/directorio/documento(1).md")
