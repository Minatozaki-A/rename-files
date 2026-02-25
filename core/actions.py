# Mueve, renombra y lista archivos
import unicodedata as udd
from pathlib import Path
import re
import hashlib as hlib
import psutil


def clean_name(name : str):
    clean = udd.normalize('NFD', name)

    without_accents = "".join(
        c for c in clean if udd.category(c) != 'Mn'
    )

    clean = re.sub(r'[^\w\s]', ' ', without_accents)
    clean = re.sub(r'\s+', ' ', clean).lower().strip()
    final_name = re.sub(r'[\s_-]+', '-', clean)
    # re.sub(r'-+', '-', clean.replace(" ", "-").replace("_", "-"))
    return final_name

def clean_file_name(path_file : Path):
    name = path_file.stem.lower()
    ext = path_file.suffix.lower()

    final_name = clean_name(name)

    return f"{final_name}{ext}"

def clean_directory_name(filename: Path):
    name = filename.stem
    title = re.sub(r'^[\d\s-]+|[\d\s-]+\.pdf$', '', name,
                flags=re.IGNORECASE).strip()
    cleaned_title = clean_name(title)
    return cleaned_title

def rename_file(path_file : Path ):
    new_name = clean_file_name(path_file)
    path_directory = path_file.parent
    final_name = path_directory / new_name

    if final_name.exists():
        stem = final_name.stem
        suffix = final_name.suffix
        candidate = path_directory / f"{stem}_1{suffix}"

        if candidate.exists():
            hash_suffix = hashl.md5(str(final_name).encode()).hexdigest()[:8]
            candidate = path_directory / f"{stem}_{hash_suffix}{suffix}"

        final_name = candidate

    return final_name


def show_files(path_directory : Path, depth: int = 0):
    indent = "  " * depth
    print(f"{indent}[{path_directory.name}]")

    for item in sorted(path_directory.iterdir()):
        if item.is_dir():
            show_files(item, depth + 1)
        if item.is_file():
            new_name = clean_file_name(item)
            changed = item.name != new_name
            marker = f"-> {new_name}" if changed else ""
            print(f"{indent}  {item.name} {marker}")