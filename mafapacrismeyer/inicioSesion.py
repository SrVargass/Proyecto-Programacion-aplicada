import pygame
import pygame_gui
from constantes import *

from basededatos import Usuario


def inicio_sesion_ventana():
    screen = pygame.display.get_surface()

    background = pygame.Surface(SCREEN_RES)
    background.fill(pygame.Color('#FFFFFF'))

    manager = pygame_gui.UIManager(SCREEN_RES)


    # boton de volver
    button_rect = pygame.Rect((20, 20), (100, 50))
    volver_boton = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                            text='Volver',
                                            manager=manager)

    spacing = 10
    button_width = 150
    button_height = 30    
    total_width = 2*button_width + spacing
    total_height = (3*button_height) + (2*spacing)
    left = (SCREEN_WIDTH-total_width)//2
    top = (SCREEN_HEIGHT-total_height)//2

    # Create a label and a text input field
    username_label = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((left, top), (button_width, button_height)),
    html_text="Usuario",
    manager=manager
)

    username_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((left+button_width+spacing, top), (button_width, button_height)),
    manager=manager
)
###
    password_label = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((left, top+button_height+spacing), (button_width, button_height)),
    html_text="Contraseña",
    manager=manager
)

    password_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((left+button_width+spacing, top+button_height+spacing), (button_width, button_height)),
    manager=manager
)

    iniciar_boton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((left, top+2*(button_height+spacing)), (total_width, button_height)),
    text='Iniciar sesión',
    manager=manager)

    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60)/1000.0  # Delta: diferencia de tiempo entre cada frame(segundos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Evento: cerrar/salir. Cerrar ventana apretando la X superior o la tecla f4. 
                pygame.quit()   # Cerrar la ventana
                exit()          # Terminar el proceso

            if event.type == pygame_gui.UI_BUTTON_PRESSED: #Evento: boton de la interfaz presionado.
                if event.ui_element == volver_boton:                    
                    running = False
                    
                if event.ui_element == iniciar_boton:
                    nombre = username_input.get_text()
                    if base_Usuarios.existe(nombre):           
                        clave = password_input.get_text()
                        user = Usuario(base_Usuarios, nombre)
                        if user.iniciar_sesion(clave):
                            print("Sesión iniciada")
                            running = False
                        else:
                            print("Contraseña incorrecta")
                    else:
                        print("El nombre de usuario no existe")

                

            manager.process_events(event)
            
        manager.update(time_delta)

        screen.blit(background)
        manager.draw_ui(screen)

        pygame.display.update()


    

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    inicio_sesion_ventana()
