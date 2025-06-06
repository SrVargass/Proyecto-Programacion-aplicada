import pygame
import pygame_gui
from constantes import *
from juego.main import mafapacris_juego
from inicioSesion import inicio_sesion_ventana
from registro import registro_ventana

def menuPrincipal(screen):
    
    manager = pygame_gui.UIManager(SCREEN_RES)
    background = pygame.Surface(SCREEN_RES)
    background.fill(pygame.Color('#FFFFFF'))

    # Creación de botones
    buttons = []
    button_labels = ['Jugar como invitado', 'Iniciar sesión', 'Registrar usuario', 'Salir']
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
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttons[0]:  # Jugar como invitado
                    result = mafapacris_juego(screen)
                    if result == "QUIT":  # Si el juego retorna False, salir
                        running = False
                        should_quit = True
                    
                if event.ui_element == buttons[1]:  # Iniciar sesión
                    result = inicio_sesion_ventana(screen)
                    if result == "QUIT":
                        running = False
                        should_quit = True
                    
                if event.ui_element == buttons[2]:  # Registrar usuario
                    registro_ventana(screen)
                    
                if event.ui_element == buttons[3]:  # Salir
                    running = False
                    should_quit = True

            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()

    return "QUIT" if should_quit else None