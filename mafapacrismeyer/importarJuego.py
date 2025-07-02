# importing sys
import sys
import pygame
sys.path.insert(0, './juego')
from juego.main import mafapacris_juego
from constantes import SCREEN_RES


def juego():
    mafapacris_juego()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    juego()
