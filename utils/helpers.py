# Funciones de fechas y tamaños
import datetime
from pathlib import  Path

def get_size(path_file : Path):
    return path_file.stat().st_size

def get_modification_time(path_file : Path):
    return datetime.datetime.fromtimestamp(
        path_file.stat().st_mtime
    )

def get_change_time(path_file : Path):
    return datetime.datetime.fromtimestamp(
        path_file.stat().st_ctime
    )