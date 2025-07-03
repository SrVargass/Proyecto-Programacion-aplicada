import sys
import pygame
import pygame_gui
from constantes import *
from color_fondo import fondo_color
from color_avatar import fondo_color_h,obtener_color_inicial_h
from fondo_juego import fondo_juego
from musica_juego import musica_juego  # NUEVO IMPORT

def Ajustes(screen,color_inicial,nombre_usuario):
    manager = pygame_gui.UIManager(SCREEN_RES)
    background = pygame.Surface(SCREEN_RES)
    current_color=color_inicial
    background.fill(current_color)

    # Creación de botones
    buttons = []
    button_labels = ['Color de fondo','Música de fondo','Fondo de juego','Color personaje','Volver']
    button_width, button_height = 200, 50
    spacing = 10
    
    for index, label in enumerate(button_labels):
        button_rect = pygame.Rect(0, 0, button_width, button_height)
        button_rect.midtop = (SCREEN_WIDTH//2, 300 + index*(button_height + spacing))
        button = pygame_gui.elements.UIButton(relative_rect=button_rect, text=label, manager=manager)
        buttons.append(button)

    clock = pygame.time.Clock()
    running = True
    should_quit = False
    
    while running:
        time_delta = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                should_quit = True
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttons[0]:  
                    result = fondo_color(screen,current_color,nombre_usuario)
                    
                    if result == "QUIT":  # Si el juego retorna False, salir
                        running = False
                        should_quit = True
                    else:
                        current_color=result
                if event.ui_element == buttons[1]:  # Iniciar sesión
                    ruta_musica = musica_juego(screen)
                    if ruta_musica == "QUIT":
                        running = False
                        should_quit = True
                    elif ruta_musica:
                        try:
                            pygame.mixer.music.load(ruta_musica)
                            pygame.mixer.music.play(-1)  # Repetir indefinidamente
                        except Exception as e:
                            print(f"Error cargando música: {e}")
                if event.ui_element == buttons[2]:  # Registrar usuario
                      result = fondo_juego(screen)
                      if result == "QUIT":
                         running = False
                         should_quit = True
                if event.ui_element == buttons[3]: #color personaje
                    color_inicial_personaje = obtener_color_inicial_h(nombre_usuario)
                    result = fondo_color_h(screen,color_inicial_personaje,nombre_usuario)
                    if result == "QUIT":
                        running=False
                        should_quit=True
                if event.ui_element == buttons[4]:  # Volver
                    running = False
                    should_quit = True

            manager.process_events(event)

        manager.update(time_delta)
        background.fill(current_color)
        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()

    return current_color

#if __name__ == "__main__":

    #pygame.init()
    #screen = pygame.display.set_mode(SCREEN_RES)
    #Ajustes(screen)