from pathlib import  Path
from core.config_loader import get_cached_config_value, build_directory_tree, save_structure_to_config
from utils.text_utils import clean_directory_name


def scanner_structure_directories(path_directory: Path, config_path: Path = None, structure_path: Path = None):
    """Función principal que orquesta el mapeo y el guardado."""
    if not path_directory.exists() or not path_directory.is_dir():
        raise FileNotFoundError(f"La ruta no existe o no es un directorio: {path_directory}")

    ignore_dir = []
    if config_path:
        cached_ignore = get_cached_config_value(config_path, "ignore")
        if cached_ignore:
            ignore_dir = cached_ignore

    ### path_directory_normalize = Path(str(path_directory).rstrip('/'))
    final_structure = {
            clean_directory_name(path_directory): build_directory_tree(path_directory, ignore_dir)
    }

    if config_path:
        save_structure_to_config(structure_path, final_structure)

