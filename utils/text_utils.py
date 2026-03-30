import unicodedata as udd
import re
from pathlib import Path

def clean_name(name : str):
    clean = udd.normalize('NFKD', name)

    without_accents = "".join(
        c for c in clean if udd.category(c) != 'Mn'
    )

    clean = re.sub(r'[^\w\s]', ' ', without_accents)
    clean = re.sub(r'\s+', ' ', clean).lower().strip()
    final_name = re.sub(r'[\s_-]+', '-', clean)
    # re.sub(r'-+', '-', clean.replace(" ", "-").replace("_", "-"))
    return final_name

def clean_file_name(path_file : Path):
    name = path_file.stem
    ext = path_file.suffix.lower()

    final_name = clean_name(name)

    return f"{final_name}{ext}"

def clean_directory_name(path_dir: Path):
    name = path_dir.name
    title = re.sub(r'^\d+[\s.\-]+', '', name).strip()
    cleaned_title = clean_name(title)
    return cleaned_title