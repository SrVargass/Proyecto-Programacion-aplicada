import json
import os
from pathlib import Path
RUTA_COLOR_USUARIOS = "colores_usuarios.json"

def cargar_color_usuario(nombre_usuario):
    if not os.path.exists(RUTA_COLOR_USUARIOS):
        return (255, 255, 255)  # color blanco por defecto

    with open(RUTA_COLOR_USUARIOS, "r") as f:
        data = json.load(f)
        if nombre_usuario in data:
            return tuple(data[nombre_usuario])
        else:
            return (255, 255, 255)

def guardar_color_usuario(nombre_usuario, color):
    # Asegurar que sea una tupla RGB simple
    color_rgb = [color.r, color.g, color.b]
    if os.path.exists(RUTA_COLOR_USUARIOS):
        with open(RUTA_COLOR_USUARIOS, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[nombre_usuario] = color_rgb

    with open(RUTA_COLOR_USUARIOS, "w") as f:
        json.dump(data, f, indent=4)
