# importing sys
import sys
import pygame
sys.path.insert(0, './juego')
from juego.main import mafapacris_juego
from constantes import SCREEN_RES


def juego(avatarHue=55):
    mafapacris_juego(avatarHue=avatarHue)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    juego(avatarHue=0)
