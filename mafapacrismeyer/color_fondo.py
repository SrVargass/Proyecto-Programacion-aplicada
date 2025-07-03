import pygame
import pygame_gui
import sys
import json
from constantes import *
from color_por_usuario import guardar_color_usuario
# Ruta al archivo JSON
COLOR_FONDO_PATH = "color_fondo.json"

#def guardar_color_fondo(color):
##    color_rgb = [color.r, color.g, color.b]
  #  with open(COLOR_FONDO_PATH, "w") as f:
   #     json.dump({"color_fondo": color_rgb}, f)

def fondo_color(screen, color_inicial, nombre_usuario):
    manager = pygame_gui.UIManager(SCREEN_RES)
    background = pygame.Surface(SCREEN_RES)
    current_color = color_inicial
    background.fill(current_color)

    button_width, button_height = 200, 50
    margin = 10

    # Botón Volver
    button_volver_rect = pygame.Rect(0, 0, button_width, button_height)
    button_volver_rect.topright = (SCREEN_WIDTH - margin, margin)
    button_volver = pygame_gui.elements.UIButton(relative_rect=button_volver_rect, text='Volver', manager=manager)

    # Botón Seleccionar Color
    apply_button_rect = pygame.Rect(0, 0, button_width, button_height)
    apply_button_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    apply_button = pygame_gui.elements.UIButton(
        relative_rect=apply_button_rect,
        text='Seleccionar Color',
        manager=manager
    )

    # Botón Predeterminado (Color Blanco)
    default_button_rect = pygame.Rect(0, 0, button_width, button_height)
    default_button_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 170)
    default_button = pygame_gui.elements.UIButton(
        relative_rect=default_button_rect,
        text='Predeterminado',
        manager=manager
    )

    clock = pygame.time.Clock()
    running = True
    color_dialog = None

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_volver:
                    running = False

                elif event.ui_element == apply_button and color_dialog is None:
                    color_dialog = pygame_gui.windows.UIColourPickerDialog(
                        pygame.Rect(100, 100, 400, 400),
                        manager,
                        window_title="Seleccionar color"
                    )

                elif event.ui_element == default_button:
                    current_color = pygame.Color(255, 255, 255)  # Blanco
                    background.fill(current_color)
                    guardar_color_usuario(nombre_usuario, current_color)

            if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                current_color = event.colour
                background.fill(current_color)
                guardar_color_usuario(nombre_usuario, current_color)
                color_dialog = None

            if event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == color_dialog:
                color_dialog = None

            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()

    return current_color



#if __name__ == "__main__":
#    pygame.init()
#    screen = pygame.display.set_mode(SCREEN_RES)
#    color_inicial = pygame.Color('#FFFFFF')  # Define un color inicial para pasar
#    fondo_color(screen, color_inicial)
#    pygame.quit()
