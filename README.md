# Proyecto IR 2025A

Este proyecto es una aplicación desarrollada en Python para la materia de Información y Recuperación (IR) del periodo 2025A en la EPN.

## Estructura del proyecto
- `src/`: Contiene el código fuente principal del proyecto.
  - `ir.py`: Contiene las utilidades para el sistema de recuperacion de informacion.
  - `cli.py`: Interfaz de CLI para el programa.
- `pyproject.toml` y `poetry.lock`: Archivos de configuración y dependencias del proyecto.

## Requisitos
- Python 3.13
- [Poetry](https://python-poetry.org/) para la gestión de dependencias


## Instalación
1. Clona este repositorio.
2. Localizate en la carpeta del proyecto
3. Instala las dependencias del proyecto usando [Poetry](https://python-poetry.org/docs/#installation):
   ```bash
   poetry install
   ```

## Uso
Para ejecutar la aplicación principal:
```bash
poetry run python3 src/cli.py
```

## Licencia
Este proyecto es solo para fines educativos.
