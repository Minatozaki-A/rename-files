import json
from pathlib import Path
from typing import Dict

_CONFIG_CACHE: Dict[str, Dict] = {}

def get_cached_config_value(config_path: Path, key: str):
    path_str = str(config_path)
    if path_str not in _CONFIG_CACHE:
        with open(config_path, 'r', encoding='utf-8') as f:
            _CONFIG_CACHE[path_str] = json.load(f)
    return _CONFIG_CACHE[path_str].get(key)


def build_directory_tree(path_dir: Path, ignore_list: list) -> dict:
    """Función recursiva para construir el diccionario de directorios."""
    tree = {}
    try:
        # Se itera sobre el contenido del directorio actual
        for item in path_dir.iterdir():
            if item.name in ignore_list:
                continue

            if item.is_dir():
                # Si es un directorio, su valor es el resultado de explorarlo por dentro (recursión)
                tree[item.name] = build_directory_tree(item, ignore_list)
            if item.is_file():
                # Si es un archivo, asignamos None o un string vacío.
                # Si solo quieres directorios en tu JSON, elimina este bloque elif.
                tree[item.name] = None
    except PermissionError:
        # Prevención de bloqueos al escanear carpetas del sistema sin permisos
        pass

    return tree


def save_structure_to_config(config_path: Path, new_structure: dict):
    """Carga el config.json actual, inyecta la estructura y guarda."""
    config_data = {}

    # 1. Leer la configuración existente para no perder la clave "ignore"
    if config_path and config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config_data = json.load(f)
            except json.JSONDecodeError:
                pass  # Si el archivo está vacío o corrupto, empezamos de cero

    # 2. Actualizar el diccionario con la nueva estructura
    config_data.update(new_structure)

    # 3. Sobrescribir el archivo JSON con el formato correcto
    if config_path:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)