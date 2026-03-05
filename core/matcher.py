from pathlib import Path
import shutil
from utils.text_utils import clean_directory_name
from core.config_loader import get_cached_config_value
from core.actions import resolve_name_file


def _flatten_directory_map(base_path: Path, structure: dict) -> dict:
    """
    Recorre el árbol de directorios del JSON recursivamente
    y devuelve un diccionario plano: { 'nombre_carpeta': Path }
    """
    dir_map = {}
    for name, subtree in structure.items():
        if isinstance(subtree, dict):
            dir_path = base_path / name
            dir_map[name] = dir_path
            dir_map.update(_flatten_directory_map(dir_path, subtree))
    return dir_map


def organize_by_title(path_base_dir: Path, config_path: Path = None):
    ignore_dir = []
    if config_path:
        cached_ignore = get_cached_config_value(config_path, "ignore")
        if cached_ignore:
            ignore_dir = cached_ignore

    directories_map = collect_directories(path_base_dir, ignore_dir, max_depth=4)

    """{
        clean_directory_name(d): d
        for d in path_base_dir.iterdir()
        if d.is_dir() and d.name not in ignore_dir
        # agregar recursion si hay sub directorios
    }"""

    revision_dir = path_base_dir / "Revision"
    if not revision_dir.exists():
        revision_dir.mkdir(exist_ok=True)

    for item in path_base_dir.iterdir():
        if item.is_file():
            file_title = clean_directory_name(item)

            if file_title in directories_map:
                dest_folder = directories_map[file_title]
            else:
                dest_folder = revision_dir

            tentative_path = dest_folder / item.name
            final_destination = resolve_name_file(tentative_path)

            try:
                shutil.move(str(item), str(final_destination))
                # Imprime el resultado para seguimiento en consola
                print(f"Organizado: {item.name} -> {final_destination.relative_to(path_base_dir)}")
            except Exception as e:
                print(f"Error al mover {item.name}: {e}")








