import json
from pathlib import Path
from typing import Dict

_CONFIG_CACHE: Dict[str, Dict] = {}

def get_cached_config_value(config_path: Path, key: str):
    path_str = str(config_path)

    if path_str not in _CONFIG_CACHE:
        if not config_path.exists():
            _CONFIG_CACHE[path_str] = {}
            return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            _CONFIG_CACHE[path_str] = json.load(f)

    except (json.JSONDecodeError, PermissionError):
        _CONFIG_CACHE[path_str] = {}

    return _CONFIG_CACHE[path_str].get(key)


def build_directory_tree(base_path: Path, ignore_list: list) -> dict:
    tree = {}
    #try:

    for item in base_path.iterdir():
        if item.name in ignore_list:
            continue
        try:
            if item.is_dir():
                tree[item.name] = build_directory_tree(item, ignore_list)

            elif item.is_file():
                tree[item.name] = None

        except PermissionError:
                tree[item.name] = None

    return tree


def save_structure_directories(config_path: Path, new_structure: dict):
    structure_data = {}

    if config_path and config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                structure_data = json.load(f)
            except json.JSONDecodeError:
                return

    structure_data.update(new_structure)

    if config_path:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(structure_data, f, indent=4, ensure_ascii=False)