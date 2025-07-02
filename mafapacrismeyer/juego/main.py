import pygame
from constantes import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_RES
from clases import Level
from levelloader import load_level

def mafapacris_juego():
    screen = pygame.display.get_surface()

    background = pygame.Surface(SCREEN_RES)
    background.fill(pygame.Color('#FFFFFF'))
    
    #definiciones

     #Eventos de usuario
    VICTORIA = pygame.event.Event(pygame.USEREVENT + 1, {"mensaje":"wawa"})
    DERROTA = pygame.event.Event(pygame.USEREVENT + 2)

     ###    

    #cicloPrincipal
    clock = pygame.time.Clock()
    running = True
    loaded = False
    nivel_n = 0
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Evento: cerrar/salir. Cerrar ventana apretando la X superior o la tecla f4. 
                pygame.quit()   # Cerrar la ventana
                exit()          # Terminar el proceso
            if event == VICTORIA:
                #print(nivel)
                nivel_n += 1
                if nivel_n > 6:
                    nivel_n = 0
                loaded = False
            if event == DERROTA:
                loaded = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        if not loaded:
            #BorrarTodo()
            #CargarNivel(int:Nivel)
            #pygame.event.post(VICTORIA)
            nivel = load_level(nivel_n)
            loaded = True
        nivel.update()
                
        screen.blit(background)
        nivel.draw(screen)        

        pygame.display.update()
        


#if __name__ == "__main__":
    #pygame.init()
    #screen = pygame.display.set_mode(SCREEN_RES)
    #mafapacris_juego()
