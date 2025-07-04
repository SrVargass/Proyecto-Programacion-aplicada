import os
import pygame
from constantes import SCREEN_RES

background_images_path = []

def es_imagen_valida(nombre_archivo):
    extensiones_validas = ['.png', '.jpg', '.jpeg', '.bmp']
    return any(nombre_archivo.lower().endswith(ext) for ext in extensiones_validas)

def recargar_imagenes_fondo():
    background_images_path.clear()
    path = os.path.join(os.path.dirname(__file__), 'resource/background')
    if os.path.exists(path):
        for image in os.listdir(path):
            full_path = os.path.join(path, image)
            if os.path.isfile(full_path) and es_imagen_valida(image):
                background_images_path.append(full_path)
    else:
        print("[Advertencia] No existe el directorio 'resource/background'")

# Carga inicial de imágenes
recargar_imagenes_fondo()

def load_background(i_index):
    # Revalidar en caso de que se hayan borrado imágenes
    if len(background_images_path) == 0:
        recargar_imagenes_fondo()

    if len(background_images_path) > 0:
        try:
            if len(background_images_path) == 1:
                background_path = background_images_path[0]
            else:
                index = i_index % len(background_images_path)
                background_path = background_images_path[index]

            background_image = pygame.image.load(background_path)
            resized_surface = pygame.transform.scale(background_image, SCREEN_RES)
        except Exception as e:
            print(f"[Error al cargar imagen de fondo]: {e}")
            recargar_imagenes_fondo()
            resized_surface = pygame.Surface(SCREEN_RES)
            resized_surface.fill(pygame.Color('#FFFFFF'))
    else:
        print("[Advertencia] No se encontraron imágenes de fondo. Usando color blanco.")
        resized_surface = pygame.Surface(SCREEN_RES)
        resized_surface.fill(pygame.Color('#FFFFFF'))
    return resized_surface
