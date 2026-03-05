# Manejo de archivos comprimidos
import zipfile
from pathlib import Path


def get_zip_info(zip_file: Path):
    """Retorna una lista con la información de los archivos en lugar de solo imprimir."""
    if not zip_file.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {zip_file}")

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:

        return zip_ref.infolist()


def extract_zip(zip_file: Path, path_destination: Path):
    if not zip_file.exists():
        raise FileNotFoundError(f"El archivo origen no existe: {zip_file}")

    if not path_destination.is_dir():
        raise ValueError(f"El destino debe ser un directorio: {path_destination}")

    if not zipfile.is_zipfile(zip_file):
        raise ValueError(f"{zip_file.name} is not a zip file")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for member in zip_ref.namelist():
                if '..' in member or member.startswith('/'):
                    raise ValueError(f"Path traversal attempt in {zip_file.name}: {member}")
            zip_ref.extractall(path_destination)
    except zipfile.BadZipFile:
        raise ValueError(f"{zip_file.name} is not a valid zip file")


