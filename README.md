# File Organizer & Scanner

Este proyecto es una herramienta para el escaneo, renombrado seguro de archivos y directorios, y la generación de estructuras en formato JSON. Su enfoque principal es la manipulación de nombres evitando colisiones y el soporte para identificar puntos de montaje en discos SSD.

## Características Principales

*   **Renombrado Seguro y Limpieza:**
    *   `resolve_name_file` y `resolve_name_directory`: Renombra archivos y carpetas eliminando caracteres especiales, tildes (usando normalización Unicode) y espacios extra, convirtiéndolos en formatos uniformes (en minúsculas, separados por guiones).
    *   Gestión automática de colisiones agregando sufijos numéricos (ej: `nombre-(1).txt`) para evitar sobrescribir archivos existentes.
*   **Escaneo y Generación de Estructuras (JSON):**
    *   Escanea de forma recursiva un directorio y genera una representación en árbol (diccionario) de toda su estructura.
    *   Soporte para listas de exclusión (ignorar ciertas carpetas) cargadas desde un archivo de configuración JSON.
    *   Cacheo de configuraciones (`config_loader.py`) para optimizar múltiples accesos de lectura.
    *   Guardado automático de la estructura escaneada en un archivo de configuración (`save_structure_to_config`).
*   **Soporte de Almacenamiento SSD:**
    *   `find_ssd_mount_point`: Utiliza la librería `psutil` para encontrar puntos de montaje específicos en discos basándose en etiquetas SSD.

## Arquitectura y Entorno

Este proyecto ha sido desarrollado con los siguientes requisitos en mente:

*   **Python >= 3.13:** Utiliza las características más recientes de Python.
*   **Gestor de Paquetes `uv`:** Las dependencias del proyecto se gestionan de manera ultrarrápida utilizando `uv`.
*   **Librerías Estándar:** Se prioriza el uso de la biblioteca estándar, especialmente `pathlib` (para manejo avanzado de rutas multiplataforma) y `json` (para las estructuras de directorios y configuración).
*   **`psutil`:** La única dependencia externa requerida (`psutil>=7.2.2`) utilizada para la enumeración de particiones y puntos de montaje.
*   **Optimizado para Btrfs:** Este proyecto fue hecho y se ha probado exclusivamente en el sistema de archivos Btrfs para aprovechar sus características únicas.

## Instalación y Uso

1.  **Requisitos:**
    *   Tener instalado Python 3.13 o superior.
    *   Tener instalado `uv` en el sistema.

2.  **Instalar dependencias:**
    Clona el repositorio y, dentro del directorio raíz, ejecuta:
    ```bash
    uv sync
    ```

3.  **Ejecutar el proyecto:**
    Dependiendo de cómo esté estructurado el punto de entrada principal (actualmente en construcción en `main.py`), puedes ejecutarlo directamente usando `uv`:
    ```bash
    uv run main.py
    ```
