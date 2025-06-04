import pygame
import pygame_gui
from constantes import *


def registro_ventana(screen):

    background = pygame.Surface(SCREEN_RES)
    background.fill(pygame.Color('#FFFFFF'))

    manager = pygame_gui.UIManager(SCREEN_RES)

    # boton de volver
    button_rect = pygame.Rect((20, 20), (100, 50))
    volver_boton = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                            text='Volver',
                                            manager=manager)

    field_labels = ['Nombre de usuario', 'Contraseña', 'Confirme contraseña']

    n_fields = len(field_labels)    
    spacing = 10
    button_width = 200
    button_height = 40    
    total_width = 2*button_width + spacing
    total_height = ((n_fields+1)*button_height) + ((n_fields)*spacing)
    left = (SCREEN_WIDTH-total_width)//2
    top = (SCREEN_HEIGHT-total_height)//2
    
    fields = []
    for index, label in enumerate(field_labels):
        if index == 0:
            label_rect = pygame.Rect((left,top) , (button_width,button_height))
        else:
            prev_x = fields[index-1][0].relative_rect.x
            prev_y = fields[index-1][0].relative_rect.y
            label_rect = pygame.Rect((prev_x, prev_y + (button_height+spacing)) , (button_width,button_height))
        label_x = label_rect.x
        label_y = label_rect.y
        input_rect = pygame.Rect((label_x+button_width+spacing,label_y) , (button_width,button_height))

        label = pygame_gui.elements.UITextBox(
            relative_rect=label_rect,
            html_text=label,
            manager=manager
        )
        inputfield = pygame_gui.elements.UITextEntryLine(
            relative_rect=input_rect,
            manager=manager
        )
        # Añadir validación para evitar espacios en blanco
        inputfield.set_allowed_characters(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.!@#$%^&*()"))
        fields.append((label,inputfield))
        
    last_x = fields[n_fields-1][0].relative_rect.x
    last_y = fields[n_fields-1][0].relative_rect.y
    registrar_boton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((last_x, last_y+button_height+spacing), (total_width, button_height)),
        text='Crear usuario',
        manager=manager)
    
    error_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((left, top + 4*(button_height+spacing)), (total_width, button_height)),
        text='',
        manager=manager,
        visible=False
    )
    error_label.text_colour = pygame.Color('#FF0000') 
    error_label.rebuild()

    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == volver_boton:                    
                    running = False
                    
                if event.ui_element == registrar_boton:
                    nombre = fields[0][1].get_text()
                    clave = fields[1][1].get_text()
                    conf_clave = fields[2][1].get_text()
                    
                    # Validación adicional para asegurarse que no hay espacios
                    if ' ' in nombre or ' ' in clave:
                        print("No se permiten espacios en blanco")
                        error_label.set_text("No se permiten espacios en blanco")
                        error_label.visible = True
                    elif not nombre or not clave:
                        print("Los campos no pueden estar vacíos")
                        error_label.set_text("Los campos no pueden estar vacíos")
                        error_label.visible = True
                    elif not base_Usuarios.existe(nombre):
                        if clave == conf_clave:
                            base_Usuarios.crear_usuario(nombre,clave)
                            base_Usuarios.actualizarJson()
                            running = False
                        else:
                            print("Las contraseñas no coinciden")
                            error_label.set_text("Las contraseñas no coinciden")
                            error_label.visible = True
                    else:
                        print("El nombre de usuario ya existe")
                        error_label.set_text("El nombre de usuario ya existe")
                        error_label.visible = True

            manager.process_events(event)
            
        manager.update(time_delta)

        screen.blit(background)
        manager.draw_ui(screen)

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    registro_ventana(screen)
