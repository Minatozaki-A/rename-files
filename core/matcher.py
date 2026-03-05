from pathlib import Path
import shutil
import json
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


def organize_by_title(path_base_dir: Path, structure_path: Path):
    # Validar que exista el archivo de estructura
    if not structure_path.exists():
        print(f"Error: No se encontró el archivo de estructura en {structure_path}")
        return

    # Cargar la estructura pre-procesada
    with open(structure_path, 'r', encoding='utf-8') as f:
        try:
            full_structure = json.load(f)
        except json.JSONDecodeError:
            print("Error: El archivo structure.json está corrupto o vacío.")
            return

    # El JSON debe tener exactamente una clave raíz (el directorio base)
    if len(full_structure) != 1:
        print("Error: structure.json debe tener exactamente una clave raíz.")
        return

    root_key = next(iter(full_structure))
    tree = full_structure[root_key]

    # Aplanamos el árbol para tener búsquedas de O(1) al emparejar archivos
    directories_map = _flatten_directory_map(path_base_dir, tree)

    revision_dir = path_base_dir / "Revision"
    if not revision_dir.exists():
        revision_dir.mkdir(exist_ok=True)

    errors = []

    for item in path_base_dir.iterdir():
        if item.is_file():
            # Los nombres ya vienen limpios de la fase anterior,
            # así que el stem coincide directamente con las claves del JSON
            file_title = item.stem

            dest_folder = directories_map.get(file_title, revision_dir)

            tentative_path = dest_folder / item.name
            final_destination = resolve_name_file(tentative_path)

            try:
                shutil.move(str(item), str(final_destination))
                print(f"Organizado: {item.name} -> {final_destination.relative_to(path_base_dir)}")
            except Exception as e:
                errors.append((item.name, e))

    if errors:
        print(f"\nErrores al mover {len(errors)} archivo(s):")
        for name, err in errors:
            print(f"  {name}: {type(err).__name__}: {err}")







