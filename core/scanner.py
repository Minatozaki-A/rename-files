# Encuentra los archivos y obtiene metadatos
from pathlib import  Path
from core.classifier import get_header
from utils.helpers import get_size, get_modification_time, get_change_time

def scan_file(path_file : Path):
    header = get_header(path_file)
    return {
        "path": path_file,
        "name": path_file.name,
        "mime": header,
        "extension": header.split("/")[1] if "/" in header else header,
        "size": get_size(path_file),
        "m_time": get_modification_time(path_file),
        "c_time": get_change_time(path_file)
    }


def scanner(path_directory : Path):
    if not path_directory.exists():
        raise FileNotFoundError(IsADirectoryError)
    for find_file in path_directory.iterdir():
        if find_file.is_file():
            scan_file(find_file)

        if find_file.is_dir():
            scanner(find_file)

