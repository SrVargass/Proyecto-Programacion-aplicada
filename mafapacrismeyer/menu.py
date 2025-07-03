import pygame
import pygame_gui
from constantes import *
from inicioSesion import inicio_sesion_ventana
from registro import registro_ventana
from importarJuego import juego
from ajustes import Ajustes
import sys
    

def menuPrincipal(screen, color_fondo):
    
    manager = pygame_gui.UIManager(SCREEN_RES)
    background = pygame.Surface(SCREEN_RES)
    background.fill(color_fondo)
    
    button_labels = ['Jugar como invitado', 'Iniciar sesión', 'Registrar usuario', 'Ajustes', 'Salir']
    button_width, button_height = 200, 50
    spacing = 10
    
    buttons = []
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
                if event.ui_element == buttons[0]:
                    result = juego()
                    if result == "QUIT":
                        running = False
                        should_quit = True
                    
                elif event.ui_element == buttons[1]:
                    result,color_fondo = inicio_sesion_ventana(screen,color_fondo)
                    if result == "QUIT":
                        pygame.quit()
                        sys.exit()
                    elif result =="LOGOUT":
                        continue
                    elif result=="BACK":
                        continue
                elif event.ui_element == buttons[2]:
                    registro_ventana(screen,color_fondo)
                
                elif event.ui_element == buttons[3]:  # Ajustes
                    result = Ajustes(screen, color_fondo,"invitado")
                    if result is not None:
                        color_fondo = result
                
                elif event.ui_element == buttons[4]:
                    running = False
                    should_quit = True

            manager.process_events(event)

        manager.update(time_delta)

        # Actualiza el color de fondo en cada frame (por si cambió)
        background.fill(color_fondo)

        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()

    if should_quit:
        pygame.quit()
        sys.exit()
