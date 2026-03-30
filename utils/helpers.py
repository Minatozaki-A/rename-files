# Funciones de fechas y tamaños
import datetime
from pathlib import  Path

def get_change_time(last_change: float):
    return datetime.datetime.fromtimestamp(last_change)

def format_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def get_directory_stats(path_directory: Path):
    total_size = 0
    file_count = 0
    last_mod = 0.0

    # Iteramos solo sobre archivos para el reporte de peso
    for item in path_directory.rglob('*'):
        if item.is_file():
            stats = item.stat()
            total_size += stats.st_size
            file_count += 1
            if stats.st_mtime > last_mod:
                last_mod = stats.st_mtime

    return {
        "total_size": format_size(total_size),
        "file_count": file_count,
        "last_modified": get_change_time(last_mod) if last_mod > 0 else "N/A"
    }