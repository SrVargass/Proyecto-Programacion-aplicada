import pygame
import pygame_gui
from sys import exit
from constantes import *

from inicioSesion import inicio_sesion_ventana
from registro import registro_ventana


pygame.init()

pygame.display.set_caption("MAFAPACRIS MEYER")

screen = pygame.display.set_mode(SCREEN_RES)


background = pygame.Surface(SCREEN_RES)
background.fill(pygame.Color('#FFFFFF'))

manager = pygame_gui.UIManager(SCREEN_RES)



# Define button labels
button_labels = ['Jugar', 'Iniciar sesión', 'Registrar usuario', 'Salir']

# Dimensiones de los botones
button_height = 50
button_width = 200
# Espacio entre los botones
spacing = 10

total_buttons_height = len(button_labels) * (button_height + spacing) - spacing 

# Crea una lista de botones y los ordena de acuerdo a los parámetros anteriores.
buttons = []

#for index in range(len(button_labels)):
#    label = button_labels[index]
for index, label in enumerate(button_labels):    
    if index == 0:        
        button_rect = pygame.Rect((0,0) , (button_width,button_height))
        button_rect.midtop= ((SCREEN_WIDTH//2,300))
        
    else:
        prev_x = buttons[index-1].relative_rect.x
        prev_y = buttons[index-1].relative_rect.y
        button_rect = pygame.Rect((prev_x, prev_y + (button_height+spacing)) , (button_width,button_height))
    
    button = pygame_gui.elements.UIButton(
        relative_rect=button_rect,
        text=label,
        manager=manager
    )
    
    buttons.append(button)


clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0  # Delta: diferencia de tiempo entre cada frame(segundos)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:   #Evento: cerrar/salir. Cerrar ventana apretando la X superior o la tecla f4.
            pygame.quit()   # Cerrar la ventana
            exit()          # Terminar el proceso

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == buttons[0]: # Jugar
                print("Jugar")
            if event.ui_element == buttons[1]: # Iniciar sesión
                inicio_sesion_ventana()
                
            if event.ui_element == buttons[2]: # Registrar usuario
                registro_ventana()
                
            if event.ui_element == buttons[3]: # Salir
                pygame.quit()
                exit() 
                
        manager.process_events(event)


    manager.update(time_delta)

    screen.blit(background)
    manager.draw_ui(screen)

    pygame.display.update()


#pygame.quit()
#exit()
