import sys
import pygame
import pygame_gui
from constantes import *
from color_fondo import fondo_color
def Ajustes(screen,color_inicial):
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
                    result = fondo_color(screen,current_color)
                    
                    if result == "QUIT":  # Si el juego retorna False, salir
                        running = False
                        should_quit = True
                    else:
                        current_color=result
                if event.ui_element == buttons[1]:  # Iniciar sesión
                    #result = musica_fondo(screen)
                    #if result == "QUIT":
                    #    running = False
                    #    should_quit = True
                    pass
                if event.ui_element == buttons[2]:  # Registrar usuario
                    #fondo_juego(screen)
                    pass
                if event.ui_element == buttons[3]: #ajustes
                    pass
                    #fondo_juego(screen)    
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