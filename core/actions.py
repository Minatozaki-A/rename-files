from pathlib import Path
import psutil
from core.config_loader import get_cached_config_value
from utils.text_utils import clean_file_name, clean_directory_name

def _resolve_config(config_path: Path, key_config: str,
                    config_value: list | None) -> list:

    if config_value is not None:
        return config_value
    if config_path:
        return get_cached_config_value(config_path, key_config) or []
    return []


def find_ssd_mount_point(label_ssd: str = None):
    if not label_ssd:
        raise ValueError("label_ssd is empty")

    for part in psutil.disk_partitions():
        mount_point = part.mountpoint.rstrip('/')
        if mount_point.endswith(label_ssd):
            print(f"Name: {part.device}")
            print(f"Mountpoint: {part.mountpoint}")
            print(f"File System: {part.fstype}")
            return Path(part.mountpoint)
    return None


def resolve_name_file(path_file : Path):
    new_name = clean_file_name(path_file)
    if not new_name:
        raise ValueError(f"new name is empty: {path_file}")

    final_name = path_file.parent / new_name
    name = final_name.stem
    suffix = final_name.suffix

    if  name == path_file.stem and suffix == path_file.suffix.lower():
        return final_name

    if final_name.exists() and final_name.samefile(path_file):
        return final_name

    counter = 1

    temp_final = final_name
    while temp_final.exists():

        temp_final = path_file.parent / f"{name}-({counter}){suffix}"
        counter += 1

    return temp_final


def resolve_name_directory(path_dir: Path):
    new_name = clean_directory_name(path_dir)
    if not new_name:
        raise ValueError(f"new name is empty: {path_dir}")

    final_name = path_dir.parent / new_name

    if final_name.name == path_dir.name:
        return final_name

    if final_name.exists() and final_name.samefile(path_dir):
        return final_name

    counter = 1
    temp_final = final_name

    while temp_final.exists():

        temp_final = path_dir.parent / f"{new_name}-({counter})"
        counter += 1

    return temp_final

def organize_for_depth_and_alphabetical(list_items: list):
    return sorted(list_items, key=lambda part: (-len(part.parts), part))


def get_name_files(source_path, config_path : Path, key: str, ignore_dir : list = None):

    ignore_dir = _resolve_config(config_path, key, ignore_dir)
    name_files = []
    for item in source_path.iterdir():
        if item.is_dir():
            if item.name in ignore_dir:
                continue
            name_files.extend(get_name_files(item, config_path, key, ignore_dir))
        elif item.is_file():
            name_files.append(item)
    return name_files


def get_name_directories(source_path, config_path : Path, key: str,ignore_dir : list = None):

    ignore_dir = _resolve_config(config_path, key, ignore_dir)
    name_directories = []
    for item in source_path.iterdir():
        if item.is_dir():
            if item.name in ignore_dir:
                continue
            name_directories.append(item)
            name_directories.extend(get_name_directories(item, config_path, key, ignore_dir))
    return name_directories



def show_files(path_directory, config_path: Path, key: str, depth: int = 0, ignore_dir: list = None):
    indent = "  " * depth
    ignore_dir = _resolve_config(config_path, key, ignore_dir)

    for item in sorted(path_directory.iterdir()):
        if item.is_dir():
            if item.name in ignore_dir:
                continue
            show_files(item, config_path, key, depth + 1)

        elif item.is_file():
            new_name = clean_file_name(item)
            changed = item.name != new_name
            marker = f"-> {new_name}" if changed else ""
            print(f"{indent}  {item.name} {marker}")