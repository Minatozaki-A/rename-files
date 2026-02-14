# Encuentra los archivos y obtiene metadatos
from pathlib import  Path
import hashlib as hashl
import magic
from core.actions import clean_name, rename, show_files

def scan_file(path_file : Path, path_directory : Path):
    ### esta logica se remplazara despues
    name_file = clean_name(path_file)
    final_path = path_directory
    info = path_file.stat()
    type_file = magic.from_file(path_file, mime=True)
    hash_file = hashl.md5(path_file.read_bytes()).hexdigest()
    size = info.st_size
    last_modified = info.st_mtime
    last_access = info.st_atime
    metadata_change = info.st_ctime
    print(f"{name_file} {type_file} {hash_file} {size} {last_modified} {last_access} {metadata_change}")



def scan_directory(path_directory : Path):
    if not path_directory.exists():
        raise FileNotFoundError(IsADirectoryError)
    for find_file in path_directory.iterdir():
        if find_file.is_file():
            scan_file(find_file, path_directory)
        if find_file.is_dir():
            scan_directory(find_file)