from pathlib import Path
import psutil
from itertools import count
from core.config_loader import get_cached_config_value
from utils.text_utils import (clean_file_name,
                            clean_directory_name)

def _resolve_config(config_path: Path, key_config: str,
                    config_value: list | None) -> list:

    if config_value is not None:
        return config_value
    if config_path:
        return get_cached_config_value(config_path, key_config) or []
    return []

def _unique_path(base_path: Path)-> Path | None:
    if not base_path.exists():
        return base_path
    stem, suffix = base_path.stem, base_path.suffix
    for n in count(1):
        candidate = base_path.parent / f"{stem}({n}){suffix}"
        if not candidate.exists():
            return candidate
    return None


def find_ssd_mount_point(label_ssd: str = None)-> Path | None:
    if not label_ssd:
        raise ValueError("label_ssd is empty")

    for part in psutil.disk_partitions():
        mount_point = part.mountpoint.rstrip('/')
        if mount_point.endswith(label_ssd):
            # print(f"Name: {part.device}")
            # print(f"Mountpoint: {part.mountpoint}")
            # print(f"File System: {part.fstype}")
            return Path(part.mountpoint)
    return None


def resolve_name_file(path_file: Path) -> Path:
    new_name = clean_file_name(path_file)

    if not new_name:
        raise ValueError(f"new name is empty: {path_file}")

    final_name = path_file.parent / new_name

    if  final_name.name == path_file.name:
        return final_name

    if final_name.exists() and final_name.samefile(path_file):
        return final_name

    return _unique_path(final_name)


def resolve_name_directory(path_dir: Path)-> Path:
    new_name = clean_directory_name(path_dir)

    if not new_name:
        raise ValueError(f"new name is empty: {path_dir}")

    final_name = path_dir.parent / new_name

    if final_name.name == path_dir.name:
        return final_name

    if final_name.exists() and final_name.samefile(path_dir):
        return final_name

    return _unique_path(final_name)

def organize_for_depth_and_alphabetical(list_items)-> list:
    return sorted(list(list_items), key=lambda part: (-len(part.parts), part))


def get_name_files(source_path: Path, config_path: Path,
                key: str, config_value: list = None):

    ignore_dir = _resolve_config(config_path, key, config_value)

    for item in source_path.iterdir():
        if item.is_dir():
            if item.name in ignore_dir:
                continue

            yield from get_name_files(item, config_path,
                                    key, ignore_dir)

        elif item.is_file():
            yield item


def get_name_directories(source_path: Path, config_path: Path,
                        key: str, config_value: list = None):

    ignore_dir = _resolve_config(config_path,
                                key, config_value)

    for item in source_path.iterdir():
        if item.is_dir():
            if item.name in ignore_dir:
                continue

            yield item

            yield from get_name_directories(item, config_path,
                                            key, ignore_dir)