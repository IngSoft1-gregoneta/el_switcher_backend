#!/bin/bash

# Ejecutar pytest sobre todos los archivos en el directorio tests
PYTHONPATH=app pytest -s app/tests --disable-warnings