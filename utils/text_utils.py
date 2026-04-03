import unicodedata as udd
import re
from pathlib import Path

def clean_name(name : str) -> str:
    """Limpia y normaliza un nombre eliminando tildes, caracteres especiales y espacios.

    Aplica un proceso de normalización Unicode NFKD para separar los caracteres base
    de sus correspondientes acentos diacríticos. Luego, filtra todos los caracteres
    que pertenecen a la categoría 'Mn' (Nonspacing Mark), eliminando efectivamente
    las tildes y otros marcadores. Finalmente, utiliza expresiones regulares para
    remover cualquier carácter no alfanumérico, sustituyendo espacios y guiones bajos
    por un único guion medio, y convierte el texto a minúsculas.

    Args:
        name (str): El nombre original a limpiar.

    Returns:
        str: El nombre limpio, normalizado y formateado con guiones.
    """
    clean = udd.normalize('NFKD', name)

    without_accents = "".join(
        c for c in clean if udd.category(c) != 'Mn'
    )

    clean = re.sub(r'[^\w\s]', ' ', without_accents)
    clean = re.sub(r'\s+', ' ', clean).lower().strip()
    final_name = re.sub(r'[\s_-]+', '-', clean)
    return final_name

def clean_file_name(path_file : Path) -> str:
    """Genera un nombre de archivo limpio preservando su extensión.

    Args:
        path_file (Path): La ruta o archivo a procesar.

    Returns:
        str: El nuevo nombre de archivo limpio con su extensión original.
    """
    name = path_file.stem
    ext = path_file.suffix.lower()

    final_name = clean_name(name)

    return f"{final_name}{ext}"

def clean_directory_name(path_dir: Path) -> str:
    """Genera un nombre de directorio limpio eliminando prefijos numéricos.

    Args:
        path_dir (Path): La ruta del directorio a procesar.

    Returns:
        str: El nuevo nombre de directorio limpio.
    """
    name = path_dir.name
    title = re.sub(r'^\d+[\s.\-]+', '', name).strip()
    cleaned_title = clean_name(title)
    return cleaned_title