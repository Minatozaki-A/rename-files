# Mueve, renombra y lista archivos
from pathlib import Path
import hashlib as hlib
import psutil
from core.config_loader import get_cached_config_value
from utils.text_utils import clean_file_name, clean_directory_name

def find_ssd_mount():
    for part in psutil.disk_partitions():
        if '/media' in part.mountpoint or '/run/media' in part.mountpoint:
            print(f"Name: {part.device}")
            print(f"Mountpoint: {part.mountpoint}")
            print(f"File System: {part.fstype}")
            return Path(part.mountpoint)
    return None

def rename_file(path_file : Path ):
    new_name = clean_file_name(path_file)
    path_directory = path_file.parent
    final_name = path_directory / new_name

    if final_name.exists():
        stem = final_name.stem
        suffix = final_name.suffix

        hash_suffix = hlib.md5(str(final_name).encode()).hexdigest()[:8]

        candidate = path_directory / f"{stem}_{hash_suffix}{suffix}"

        final_name = candidate

    return final_name

def find_ssd_mount():
    for part in psutil.disk_partitions():
        if '/media' in part.mountpoint or '/run/media' in part.mountpoint:
            print(f"Name: {part.device}")
            print(f"Mountpoint: {part.mountpoint}")
            print(f"File System: {part.fstype}")
            return Path(part.mountpoint)
    return None

def show_files(path_directory, config_path: Path, depth: int = 0):
    indent = "  " * depth
    ignore_dir = []

    if config_path:
        cached_ignore = get_cached_config_value(config_path, "ignore")
        if cached_ignore:
            ignore_dir = cached_ignore

    print(f"{indent}[{clean_directory_name(path_directory)}]")

    for item in sorted(path_directory.iterdir()):
        if item.is_dir():
            if item.name in ignore_dir:
                continue
            show_files(item, config_path, depth + 1)

        elif item.is_file():
            new_name = clean_file_name(item)
            changed = item.name != new_name
            marker = f"-> {new_name}" if changed else ""
            print(f"{indent}  {item.name} {marker}")