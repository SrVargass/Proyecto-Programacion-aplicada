import pygame
from constantes import *
from menu import menuPrincipal


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    pygame.display.set_caption("MAFAPACRIS MEYER")
    
    running = True
    while running:
        # El menú principal controla las transiciones
        action = menuPrincipal(screen)
        
        if action == "QUIT":
            running = False
    
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
