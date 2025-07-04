import json
import os

RUTA_COLOR_AVATAR = "color_avatar.json"

def cargar_avatar_hue(nombre_usuario):
    if not os.path.exists(RUTA_COLOR_AVATAR):
        return 55  # Valor HUE por defecto

    with open(RUTA_COLOR_AVATAR, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get(nombre_usuario, 55)
