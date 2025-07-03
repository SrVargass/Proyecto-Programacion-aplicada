import pygame
import pygame_gui
from sys import exit
from constantes import *
import sys
from pathlib import Path
from importarJuego import juego
from ajustes import Ajustes
from color_por_usuario import cargar_color_usuario

sys.path.append(str(Path(__file__).parent / "juego"))

def cuentaIniciada(screen, usuario,color_fondo):  
    manager = pygame_gui.UIManager(SCREEN_RES)
    background = pygame.Surface(SCREEN_RES)
    background.fill(color_fondo)
    
    button_height = 50
    button_width = 200
    spacing = 20  # Espacio entre botones
    start_y = 250  # Altura inicial del primer botón

    # Botón Jugar
    jugar_boton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (SCREEN_WIDTH//2 - button_width//2, start_y),
            (button_width, button_height)
        ),
        text=f'Jugar (Usuario: {usuario.nombre})',
        manager=manager
    )
    
    # Botón Ajustes
    ajuste_boton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (SCREEN_WIDTH//2 - button_width//2, start_y + button_height + spacing),
            (button_width, button_height)
        ),
        text='Ajustes',
        manager=manager
    )

    # Botón Cerrar sesión
    cerrar_sesion_boton = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (SCREEN_WIDTH//2 - button_width//2, start_y + 2 * (button_height + spacing)),
            (button_width, button_height)
        ),
        text='Cerrar sesión',
        manager=manager
    )

    # Etiqueta de mensaje
    message_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH//2 - 150, start_y + 3 * (button_height + spacing)), (300, 40)),
        text='',
        manager=manager
    )
    message_label.text_colour = pygame.Color('#00FF00')
    message_label.visible = False
    
    clock = pygame.time.Clock()
    running = True
    result = None
    
    while running:
        time_delta = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result = "QUIT"
                running = False
                
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == jugar_boton:
                    if usuario.sesionIniciada:
                        game_result = juego()
                        if game_result == False:
                            result = "QUIT"
                            running = False
                    else:
                        message_label.set_text("Sesión expirada")
                        message_label.visible = True
                        
                elif event.ui_element == ajuste_boton:
                    nuevo_color = Ajustes(screen,color_fondo,usuario.nombre)
                    if nuevo_color == "QUIT":
                        running = False
                    else:
                        color_fondo=nuevo_color

                elif event.ui_element == cerrar_sesion_boton:
                    usuario.cerrar_sesion()
                    message_label.set_text("Sesión cerrada correctamente")
                    message_label.visible = True
                    color_fondo=cargar_color_usuario("invitado")
                    result = "LOGOUT"
                    running = False
                    
            manager.process_events(event)
            
        manager.update(time_delta)
        background.fill(color_fondo)
        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()

    return result,color_fondo

#if __name__ == "__main__":
    #class MockUser:
     #   def __init__(self, nombre):
      #      self.nombre = nombre
       #     self.sesionIniciada = True
        #def cerrar_sesion(self):
         #   self.sesionIniciada = False

    #pygame.init()
    #screen = pygame.display.set_mode(SCREEN_RES)
    #cuentaIniciada(screen, MockUser("UsuarioPrueba"))
