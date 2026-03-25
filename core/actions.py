from pathlib import Path
import psutil
from core.config_loader import get_cached_config_value
from utils.text_utils import clean_file_name, clean_directory_name

def _resolve_config(config_path: Path, key_config: str , config_value: list | None) -> list:
    if config_value is not None:
        return config_value
    if config_path:
        return get_cached_config_value(config_path, key_config) or []
    return []


def find_ssd_mount():
    for part in psutil.disk_partitions():
        if '/media' in part.mountpoint or '/run/media' in part.mountpoint:
            print(f"Name: {part.device}")
            print(f"Mountpoint: {part.mountpoint}")
            print(f"File System: {part.fstype}")
            return Path(part.mountpoint)
    return None

def resolve_name_file(path_file : Path):
    new_name = clean_file_name(path_file)
    if not new_name:
        raise ValueError(f"new name is empty: {path_file}")

    if Path(new_name).stem == path_file.stem:
        return None

    final_name = path_file.parent / new_name

    if not final_name.exists():
        return final_name

    name = Path(new_name).stem
    suffix = Path(new_name).suffix
    counter = 1

    while True:
        candidate = path_file.parent / f"{name}_({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1

def resolve_name_directory(path_dir: Path):
    new_name = clean_directory_name(path_dir)
    if not new_name:
        raise ValueError(f"new name is empty: {path_dir}")


    if new_name == path_dir.name:
        return None

    final_name = path_dir.parent / new_name

    """if  final_name.exists():
        raise FileExistsError(f"Directory already exists: {final_name}")
"""
    return final_name

def _resolve_config(config_path: Path, config_value: list | None) -> list:
    if config_value is not None:
        return config_value
    if config_path:
        return get_cached_config_value(config_path, "ignore") or []
    return []

def get_name_files(source_path, config_path : Path, ignore_dir : list = None):
    """ if ignore_dir is None and config_path:
        ignore_dir = get_cached_config_value(config_path, "ignore") or []
    elif ignore_dir is None:
        ignore_dir = []"""
    ignore_dir = _resolve_config(config_path, ignore_dir)
    name_files = []
    for item in sorted(source_path.iterdir()):
        if item.is_dir():
            if item.name in ignore_dir:
                continue
            name_files.extend(get_name_files(item, config_path, ignore_dir))
        elif item.is_file():
            name_files.append(item)
    return name_files

def get_name_directories(source_path, config_path : Path, ignore_dir : list = None):
    """if ignore_dir is None and config_path:
        ignore_dir = get_cached_config_value(config_path, "ignore") or []
    elif ignore_dir is None:
        ignore_dir = []"""
    ignore_dir = _resolve_config(config_path, ignore_dir)
    name_directories = []
    for item in sorted(source_path.iterdir()):
        if item.is_dir():
            if item.name in ignore_dir:
                continue
            name_directories.append(item)
            name_directories.extend(get_name_directories(item, config_path, ignore_dir))
    return name_directories



def show_files(path_directory, config_path: Path, depth: int = 0, ignore_dir: list = None):
    indent = "  " * depth
    ignore_dir = _resolve_config(config_path, ignore_dir)
    """if ignore_dir is None and config_path:
        ignore_dir = get_cached_config_value(config_path, "ignore") or []
    elif ignore_dir is None:
        ignore_dir = []
    print(f"{indent}[{clean_directory_name(path_directory)}]")"""

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