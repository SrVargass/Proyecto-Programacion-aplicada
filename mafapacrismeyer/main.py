import pygame
from constantes import *
from menu import menuPrincipal
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    pygame.display.set_caption(TITULO_JUEGO)

    color_fondo = pygame.Color('#FFFFFF')

    running = True
    while running:
        action = menuPrincipal(screen, color_fondo)
        if action == "QUIT":
            running = False
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
    
