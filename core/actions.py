# Mueve, renombra, comprime o lista archivos
from pathlib import Path
import re
import os

def rename(path_file : Path):
    name, ext = os.path.splitext(path_file.name)
    clean_name = re.sub(r'[^\w\s]', ' ', name)
    clean_name = re.sub(r'\s+', ' ', clean_name).lower().strip()
    final_name = clean_name.replace(" ", "_")
    return f"{final_name}{ext}"


def list_files(path_directory : Path):
    if not path_directory.exists():
        raise FileNotFoundError(IsADirectoryError)
    for find_file in path_directory.iterdir():
        if find_file.is_dir():
            print(f"{path_directory.name}/{find_file.name}")
            list_files(find_file)
        if find_file.is_file():
            print(f"File: {rename(find_file)}")

def move_file(path_file : Path, path_destination : Path):
    print(f"Moviendo {path_file.name} a {path_destination.name}")

HOME = Path.home()
print(list_files(HOME/ "Downloads"))