import pygame
import pygame_gui
from constantes import *
from sesionIniciada import cuentaIniciada
from basededatos import Usuario

def inicio_sesion_ventana(screen):
    manager = pygame_gui.UIManager(SCREEN_RES)
    background = pygame.Surface(SCREEN_RES)
    background.fill(pygame.Color('#FFFFFF'))
    
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

    # Elementos de UI
    username_label = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((left, top), (button_width, button_height)),
        html_text="Usuario",
        manager=manager
    )

    username_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((left+button_width+spacing, top), (button_width, button_height)),
        manager=manager
    )

    password_label = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((left, top+button_height+spacing), (button_width, button_height)),
        html_text="Contraseña",
        manager=manager
    )

    password_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((left+button_width+spacing, top+button_height+spacing), (button_width, button_height)),
        manager=manager
    )

    # Ocultar contraseña
    if hasattr(password_input, 'set_text_hidden'):
        password_input.set_text_hidden(True)

    iniciar_boton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((left, top+2*(button_height+spacing)), (total_width, button_height)),
        text='Iniciar sesión',
        manager=manager
    )

    error_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((left, top + 3*(button_height+spacing)), (total_width, button_height)),
        text='',
        manager=manager,
        visible=False
    )  
    error_label.text_colour = pygame.Color('#FF0000') 
    error_label.rebuild()
    
    clock = pygame.time.Clock()
    running = True
    result=None
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result="QUIT"
                running=False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                print("hola")
                if event.ui_element == volver_boton:
                    running = False
                    
                if event.ui_element == iniciar_boton:
                    nombre = username_input.get_text()
                    clave = password_input.get_text()
                    if not nombre or not clave:
                        error_label.set_text("Complete ambos campos")
                        error_label.visible=True
                    elif not base_Usuarios.existe(nombre):
                        error_label.set_text("Usuario no existe")
                        error_label.visible = True
                    else:
                        user = Usuario(base_Usuarios, nombre)
                        if user.iniciar_sesion(clave):
                            result=cuentaIniciada(screen, user)
                            if result =="QUIT":
                                return "QUIT"
                            if result =="LOGOUT":
                                running = False
                        else:
                            error_label.set_text("¡Contraseña incorrecta!")
                            error_label.visible = True

            manager.process_events(event)
            
        manager.update(time_delta)
        screen.blit(background, (0,0))
        manager.draw_ui(screen)
        pygame.display.update()

    return result


    

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    inicio_sesion_ventana(screen)
