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
        raise ValueError(f"{zip_file.name} no es un archivo ZIP válido")

    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            destination_abs = path_destination.resolve()

            for member in zip_ref.namelist():
                # Forma más robusta de prevenir Path Traversal usando resolve()
                target_path = (path_destination / member).resolve()

                if not str(target_path).startswith(str(destination_abs)):
                    raise ValueError(f"Intento de Path Traversal detectado en: {member}")

            zip_ref.extractall(path_destination)

    except zipfile.BadZipFile:
        raise ValueError(f"El archivo {zip_file.name} está corrupto o no es un ZIP")

