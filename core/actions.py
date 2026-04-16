from pathlib import Path
import psutil
import logging
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
    """Genera una ruta única añadiendo un sufijo numérico para evitar colisiones.

    Args:
        base_path (Path): La ruta deseada original.

    Returns:
        Path | None: La ruta única si se encuentra, o None si no hay colisión (es decir, el path base ya era válido).
    """
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
            logging.info("SSD found — device: %s | mount point: %s | filesystem: %s",
                         part.device, part.mountpoint, part.fstype)
            return Path(part.mountpoint)
    return None


def resolve_name_path(base_path: Path) -> Path | None:
    """Resuelve y limpia el nombre para un archivo o directorio.

    Detecta si la ruta proporcionada (`base_path`) corresponde a un directorio o a un
    archivo. Dependiendo del tipo, aplica la limpieza correspondiente (`clean_directory_name`
    o `clean_file_name`). Posteriormente, maneja la resolución de colisiones: si el nuevo
    nombre limpio ya existe en el directorio destino, delega en la función `_unique_path`
    para adjuntar un sufijo numérico incremental (por ejemplo, `archivo(1).txt`) garantizando
    que la ruta final sea única.

    Args:
        base_path (Path): La ruta original a resolver y renombrar.

    Returns:
        Path | None: La ruta resuelta con el nombre limpio y único, o None si hay error.

    Raises:
        ValueError: Si el nombre resultante después de la limpieza está vacío.
    """
    new_name = ""

    if base_path.is_dir():
        new_name = clean_directory_name(base_path)
    elif base_path.is_file():
        new_name = clean_file_name(base_path)

    if not new_name:
        raise ValueError(f"new name is empty: {base_path}")

    final_name = base_path.parent / new_name

    if  final_name.name == base_path.name:
        return final_name

    if final_name.exists() and final_name.samefile(base_path):
        return final_name

    return _unique_path(final_name)


def organize_for_depth_and_alphabetical(list_items)-> list:
    return sorted(list(list_items), key=lambda part: (-len(part.parts), part))


def get_name_files(source_path: Path, config_path: Path,
                key: str, config_value: list = None):

    ignore_dir = _resolve_config(config_path, key, config_value)

    try:
        for item in source_path.iterdir():

            if item.is_dir():
                if item.name in ignore_dir:
                    continue

                yield from get_name_files(item, config_path,
                                    key, ignore_dir)

            elif item.is_file():
                yield item
    except PermissionError:
        logging.error("Permission denied — cannot read directory contents: %s", source_path)


def get_name_directories(source_path: Path, config_path: Path,
                        key: str, config_value: list = None):

    ignore_dir = _resolve_config(config_path,
                                key, config_value)
    try:
        for item in source_path.iterdir():

            if item.is_dir():
                if item.name in ignore_dir:
                    continue

                yield item

                yield from get_name_directories(item, config_path,
                                            key, ignore_dir)
    except PermissionError:
        logging.error("Permission denied — cannot read directory contents: %s", source_path)

def rename_files_and_directories(list_items: list, is_dry_run: bool):
    for item in list_items:
        try:
            new_path_file = resolve_name_path(item)
            if new_path_file and new_path_file != item:
                if is_dry_run:
                    logging.info("[DRY RUN] Would rename: %s -> %s", item.name, new_path_file.name)
                else:
                    try:
                        logging.info("[RENAME] %s -> %s", item.name, new_path_file.name)
                        item.rename(new_path_file)
                    except PermissionError:
                        logging.error("Permission denied — could not rename: %s -> %s", item.name, new_path_file.name)

        except PermissionError:
            logging.error("Permission denied — cannot access item: %s", item)
        except OSError as e:
            logging.error("OS error while processing %s: %s", item, e)