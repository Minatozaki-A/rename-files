# Mueve, renombra y lista archivos
import unicodedata as udd
from pathlib import Path
import re
import hashlib as hashl
import shutil

def clean_name(path_file : Path):
    if not path_file.exists():
        raise FileNotFoundError(f"Not exists the file {path_file.name}")

    name = path_file.stem.lower()
    ext = path_file.suffix.lower()

    clean = udd.normalize('NFD', name)
    clean = udd.normalize( 'NFC', clean)

    without_accents = "".join(
        c for c in clean if udd.category(c) != 'Mn'
    )

    clean = re.sub(r'[^\w\s]', ' ', without_accents)

    clean = re.sub(r'\s+', ' ', clean).lower().strip()

    final_name = re.sub(r'_+', '_', clean.replace(" ", "_"))
    return f"{final_name}{ext}"


def rename(path_directory : Path, new_name : str):
    if  not path_directory.exists():
        raise IsADirectoryError()

    final_name = path_directory / new_name

    if final_name.exists():
        # first candidate
        stem = final_name.stem
        suffix = final_name.suffix
        candidate = path_directory / f"{stem}_1{suffix}"

        if candidate.exists():
            hash_suffix = hashl.md5(str(final_name).encode()).hexdigest()[:8]
            candidate = path_directory / f"{stem}_{hash_suffix}{suffix}" # 2 fallback

        final_name = candidate

    return final_name

def show_files(path_directory : Path, depth: int = 0):
    if not path_directory.exists():
        raise FileNotFoundError(f"Not exists the directory {path_directory.name}")

    indent = "  " * depth
    print(f"{indent}[{path_directory.name}]")

    for item in sorted(path_directory.iterdir()):
        if item.is_dir():
            show_files(item, depth + 1)
        if item.is_file():
            new_name = clean_name(item)
            changed = item.name != new_name
            marker = f"-> {new_name}" if changed else ""
            print(f"{indent}  {item.name} {marker}")

def move_file(path_file : Path, path_destination : Path):
        if not path_destination.exists():
            raise FileNotFoundError(f"Not exists the directory {path_destination.name}")

        if not path_file.exists():
            raise FileNotFoundError(f"Not exists the file {path_file.name}")

        final_destination = rename(path_destination, path_file.name)
        shutil.move(path_file, final_destination)
