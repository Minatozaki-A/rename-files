# Python File Organizer

Este script de automatización organiza el directorio de descargas del usuario de forma eficiente, clasificando los archivos en carpetas específicas según su tipo y gestionando posibles duplicados.

## Características principales

* **Categorización automática:** Clasifica archivos en grupos como Imágenes, Videos, Documentos y más, basándose en una lista predefinida de extensiones.
* **Gestión de colisiones de nombres:** Implementa un bucle de validación que, al detectar un archivo con el mismo nombre en el destino, renombra el archivo entrante de forma incremental (ej. archivo_1.ext) para evitar la pérdida de información.
* **Estructura basada en el Directorio Home:** Utiliza rutas dinámicas que se adaptan al directorio personal del usuario, facilitando su ejecución en diferentes entornos sin cambios manuales de ruta.
* **Tratamiento de archivos desconocidos:** Los archivos cuyas extensiones no coinciden con las categorías definidas se mueven a una carpeta de "Revision" para su inspección manual.

## Detalles Técnicos

El desarrollo se centra en el uso de librerías estándar de Python para mantener el script ligero y compatible:

1. **Pathlib:** Se utiliza para la manipulación de rutas de archivos mediante objetos, garantizando que el script funcione correctamente tanto en sistemas basados en Unix como en Windows.
2. **Shutil:** Se emplea para realizar las operaciones de movimiento de archivos entre directorios de forma segura.
3. **Diccionarios de mapeo:** La lógica de organización depende de dos diccionarios principales: uno para agrupar extensiones en categorías y otro para asignar esas categorías a rutas físicas del sistema.
4. **Sistema de Archivos Btrfs:** El sistema fue probado y programado específicamente para el sistema de archivos Btrfs. Esto permite aprovechar sus características nativas como *Case Sensitivity* (distinción entre mayúsculas y minúsculas) y *Copy-on-Write (CoW)* para un manejo de archivos más eficiente y seguro.

## Requisitos

* **Python:** 3.13 o superior.
* **Dependencias:** Requiere la librería `psutil`. Las dependencias del proyecto se gestionan mediante `uv`.
* **Sistema de Archivos:** Se recomienda encarecidamente el uso del sistema de archivos **Btrfs** (el sistema fue programado y probado para este Filesystem).

## Instalación y uso

1. Clonar este repositorio.
2. Sincronizar las dependencias usando `uv` (recomendado):
   ```bash
   uv sync
   ```
3. Ejecutar el script principal:
   ```bash
   python main.py
   ```






   
