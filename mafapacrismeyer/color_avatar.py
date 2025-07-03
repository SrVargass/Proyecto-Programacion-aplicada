import pygame
import pygame_gui
import sys
import json
from constantes import *

# Nueva ruta para el archivo que guarda solo el H
COLOR_H_PATH = "color_avatar.json"

def obtener_color_inicial_h(nombre_usuario, s=100, v=100):
    """Crea un color inicial basado en el H guardado para el usuario"""
    h = cargar_h_usuario(nombre_usuario, default_h=0)
    color = pygame.Color(0)
    color.hsva = (h, s, v, 100)  # Convierte el entero a color HSV
    return color

def guardar_h_usuario(nombre_usuario, h):
    """Guarda solo el componente H para el usuario como entero"""
    try:
        # Intentar cargar datos existentes
        with open(COLOR_H_PATH, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, crear nueva estructura
        data = {}
    
    # Convertir a entero y actualizar el valor H para este usuario
    data[nombre_usuario] = int(h)
    
    # Guardar los datos actualizados
    with open(COLOR_H_PATH, 'w') as f:
        json.dump(data, f)

def cargar_h_usuario(nombre_usuario, default_h=0):
    """Carga el componente H guardado para un usuario como entero"""
    try:
        with open(COLOR_H_PATH, 'r') as f:
            data = json.load(f)
            # Convertir a entero si es necesario
            value = data.get(nombre_usuario, default_h)
            return int(value)
    except (FileNotFoundError, json.JSONDecodeError):
        return int(default_h)

def fondo_color_h(screen, color_inicial, nombre_usuario):
    manager = pygame_gui.UIManager(SCREEN_RES)
    background = pygame.Surface(SCREEN_RES)
    current_color = color_inicial
    background.fill(current_color)
    
    # Convertir color inicial a HSV y redondear a entero
    h, s, v, a = color_inicial.hsva
    h = int(round(h))

    button_width, button_height = 200, 50
    margin = 10

    # Botón Volver
    button_volver_rect = pygame.Rect(0, 0, button_width, button_height)
    button_volver_rect.topright = (SCREEN_WIDTH - margin, margin)
    button_volver = pygame_gui.elements.UIButton(relative_rect=button_volver_rect, text='Volver', manager=manager)

    # Botón Predeterminado (H=0)
    default_button_rect = pygame.Rect(0, 0, button_width, button_height)
    default_button_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 170)
    default_button = pygame_gui.elements.UIButton(
        relative_rect=default_button_rect,
        text='Predeterminado',
        manager=manager
    )

    # Slider para H (valor inicial como entero)
    slider_width = 300
    slider_rect = pygame.Rect((SCREEN_WIDTH - slider_width) // 2, SCREEN_HEIGHT // 2 - 25, slider_width, 30)
    h_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=slider_rect,
        start_value=h,  # Valor inicial como entero
        value_range=(0, 360),
        manager=manager
    )

    # Etiqueta para mostrar valor H como entero
    label_rect = pygame.Rect(0, 0, 200, 30)
    label_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
    h_label = pygame_gui.elements.UILabel(
        relative_rect=label_rect,
        text=f'Matiz (H): {h}°',  # Mostrar sin decimales
        manager=manager
    )

    # Área de muestra de color
    muestra_rect = pygame.Rect((SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT // 4, 150, 100)

    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_volver:
                    running = False

                elif event.ui_element == default_button:
                    h = 0  # Entero
                    h_slider.set_current_value(h)
                    h_label.set_text(f'Matiz (H): {h}°')
                    
                    # Crear nuevo color manteniendo S y V
                    new_color = pygame.Color(0)
                    new_color.hsva = (h, s, v, 100)
                    current_color = new_color
                    background.fill(current_color)
                    guardar_h_usuario(nombre_usuario, h)  # Guardar como entero

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == h_slider:
                    # Redondear a entero
                    h = int(round(event.value))
                    h_label.set_text(f'Matiz (H): {h}°')
                    
                    # Crear nuevo color manteniendo S y V
                    new_color = pygame.Color(0)
                    new_color.hsva = (h, s, v, 100)
                    current_color = new_color
                    background.fill(current_color)
                    guardar_h_usuario(nombre_usuario, h)  # Guardar como entero

            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
        
        # Dibujar área de muestra con borde
        pygame.draw.rect(screen, current_color, muestra_rect)
        pygame.draw.rect(screen, (0, 0, 0), muestra_rect, 2)
        
        manager.draw_ui(screen)
        pygame.display.update()

    return current_color