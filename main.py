import shutil
import os
from pathlib import Path

# generar la direccion del directorio Home
HOME = Path.home()

# Ruta origen
DIRECTORIODOWNLOADS = HOME / "Downloads"

# Archivos fuera de dicionario de categorias
DIRECTORIOREVISION = DIRECTORIODOWNLOADS / "Revision"
DIRECTORIOREVISION.mkdir(parents= True,exist_ok=True)

categorias = {
        "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
        "Videos": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
        "Documentos": [".doc", ".docx", ".xlsx", ".pptx"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Ejecutables": [".exe", ".msi", ".app", ".sh", ".bat"],
        "Libros": [".pdf", ".epub"],
        "Notas": [".txt"]
    }

mapeo_directorios = {
    "Imagenes": HOME / "Pictures",
    "Videos": HOME / "Videos",
    "Documentos": HOME / "Documents",
    "Audio": HOME / "Music",
    "Comprimidos": HOME / "Tools",
    "Ejecutables": HOME / "Tools",
    "Libros": HOME / "BooksAndMore",
    "Notas": HOME / "Notes",
    "Otros": DIRECTORIOREVISION
}

# recorre y revisa si hay archivos en Downloads
for file in DIRECTORIODOWNLOADS.iterdir():
    try:
        if file.is_file():
            extension = file.suffix.lower()
            categoria_encontrada = "Otros"
      
            for categoria, extensiones in categorias.items():
                if extension in extensiones:
                    categoria_encontrada = categoria
                    print(f"Archivo {file.name} se encuentra en la categoria {categoria}")
                    break

            directorio_destino = mapeo_directorios.get(categoria_encontrada)
            direccion_final = directorio_destino / file.name

            if direccion_final.exists():
                print(f"El archivo {file.name} ya existe en {mapeo_directorios[categoria_encontrada]}")
                contador = 1
                nombre, ext = os.path.splitext(file.name)

                while direccion_final.exists():
                    nuevo_nombre = f"{nombre}_{contador}{ext}"
                    direccion_final = directorio_destino / nuevo_nombre
                    contador += 1

            shutil.move(file, direccion_final)
            print(f"Movido: {file.name} -> {categoria_encontrada}/")
    except Exception as e:
            print(f"Error: {e}")