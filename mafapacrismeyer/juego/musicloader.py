import os
import pygame
#from constantes import SCREEN_RES

music_path = []
def add_musicPath(filename):
    path = os.path.join(os.path.dirname(__file__), 'resource/music', filename)
    music_path.append(path)

path = os.path.join(os.path.dirname(__file__), 'resource/music')
fileArray = os.listdir(path)

for musicfile in fileArray:
    add_musicPath(musicfile)


class MusicPlayer():
    def __init__(self):
        self.music_list = music_path
        self.current = 0
        print(self.music_list)
        
    def play(self):
        if len(self.music_list) > 0:
            music_path = self.music_list[self.current]
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
    
    def skip(self):
        self.current += 1
        if self.current >= len(self.music_list):
            self.current -= len(self.music_list)
        self.play()
        
    def update(self):
        if not pygame.mixer.music.get_busy():
            self.skip()


