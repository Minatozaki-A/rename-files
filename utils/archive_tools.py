# Manejo de archivos comprimidos
import zipfile
from pathlib import Path

def show_zip_content(zip_file: Path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.printdir()

def extract_zip(zip_file: Path, path_destination: Path):
    if not path_destination.exists():
        raise FileNotFoundError(f"Not exists the directory {path_destination.name}")
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


