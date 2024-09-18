#!/bin/bash

# Establecer la ruta base del proyecto
PROJECT_DIR="/home/tadeofiorini/Documents/la-gregoneta/el_switcher_backend/app"

# Ejecutar pytest sobre todos los archivos en el directorio tests
PYTHONPATH=$PROJECT_DIR pytest -s $PROJECT_DIR/tests --disable-warnings
