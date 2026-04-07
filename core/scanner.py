from pathlib import  Path
from core.config_loader import (get_cached_config_value,
                                build_directory_tree,
                                save_structure_directories)
from utils.text_utils import clean_directory_name


def scanner_structure_directories(base_path: Path, config_path: Path = None, structure_path: Path = None):
    if not base_path.exists() or not base_path.is_dir():
        raise FileNotFoundError(f"La ruta no existe o no es un directorio: {base_path}")

    ignore_dir = []
    if config_path:
        cached_ignore = get_cached_config_value(config_path, "ignore")
        if cached_ignore:
            ignore_dir = cached_ignore

    final_structure = {
            clean_directory_name(base_path): build_directory_tree(base_path, ignore_dir)
    }

    if config_path:
        save_structure_directories(structure_path, final_structure)

