import pygame
from userinput import UserInput
from entities import Player
from entities import Enemy

BLOCK_SIZE=48

def draw_spriteDisplacement(sprite, displacement, Surface):
    copy  = sprite.rect.copy()

    copy.center = (sprite.rect.centerx+displacement[0] , sprite.rect.centery+displacement[1])

    Surface.blit(sprite.image, copy)
               

class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((48,48))
        self.image.fill(pygame.Color('#000000'))
        self.rect = self.image.get_rect()

    def place(self, x, y):
        self.rect.x = x
        self.rect.y = y
        


class Ladder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,48))
        self.image.fill(pygame.Color('#FFFF00'))
        self.rect = self.image.get_rect()
        self._group = pygame.sprite.Group

    def set_group(self, group):
        self._group = group

    def place(self, x, y):
        self.rect.centerx = x+(BLOCK_SIZE//2)
        self.rect.y = y

    def is_top(self):
        copy = self.rect.copy()
        copy.y -= 48
        for sprite in self._group.sprites():
            if copy.colliderect(sprite.rect):
                return False
        return True


class Camera():
    def __init__(self, frame):
        self.frame = frame #Rect contaning the level elements
        self.margin = 48
        self._width = 920
        self._height = 690
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(0, 0, self._width, self._height)
        self.trackbox = pygame.Rect(0,0, 230,230)
        self.rect.center = (self.x, self.y)
        self.sprites = []
        

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
    
    def draw(self, Surface):
        displacement = 100

        
        for item in self.sprites:
            
            if isinstance(item, pygame.sprite.Group):
                groupCopy = item.copy()
                
                spriteList = groupCopy.sprites()
                for sprite in spriteList:
                    
                    draw_spriteDisplacement(sprite,
                                        ( (self._width//2)-self.x, (self._height//2) - self.y),
                                        Surface)
            else:
                draw_spriteDisplacement(item,
                                        ( (self._width//2)-self.x, (self._height//2) - self.y),
                                        Surface)                

    def track_x(self, X):
        #self.x = X
        self.rect.centerx = self.trackbox.centerx

        if X > self.trackbox.right:
            self.trackbox.right = X
        elif X < self.trackbox.left:
            self.trackbox.left = X
        #self.x = self.trackbox.centerx           

        
        if self.rect.right > self.frame.right+self.margin:
            self.rect.right = self.frame.right+self.margin
        elif self.rect.left < self.frame.left-self.margin:
            self.rect.left = self.frame.left-self.margin
        self.x = self.rect.centerx


    def track_y(self, Y):
        #self.y = Y
        self.rect.centery = self.trackbox.centery

        if Y > self.trackbox.bottom:
            self.trackbox.bottom = Y
        elif Y < self.trackbox.top:
            self.trackbox.top = Y

        if self.rect.bottom > self.frame.bottom+self.margin:
            self.rect.bottom = self.frame.bottom+self.margin
        elif self.rect.top < self.frame.top-self.margin:
            self.rect.top = self.frame.top-self.margin
        self.y = self.rect.centery

    def update(self, target):
        #self.rect.center = (self.y,self.x)
        #print(f"self : {self.rect.height}")
        #print(f"frame: {self.frame.height}")
        if self.rect.width < self.frame.width:
            self.track_x(target[0])
            self.rect.x = self.x+ (self._width//2)            
        else:
            self.x = self.frame.centerx
            #self.rect.centerx = self.frame.centerx

        if self.rect.height < self.frame.height+2*48:
            self.track_y(target[1])
            self.rect.y = self.y+ (self._height//2)
        else:
            self.y = self.frame.centery
            #self.rect.centery = self.frame.centery

        
            
        
class Coin(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24,24))
        self.image.fill(pygame.Color('#00FFFF'))
        self.rect = self.image.get_rect()
        self.playerSprite = player

    def place(self, x, y):
        self.rect.centerx = x+(BLOCK_SIZE//2)
        self.rect.centery = y+(BLOCK_SIZE//2)

    def get_collected(self):
        print("Monea")
        self.kill()

    def update(self):
        if self.rect.colliderect(self.playerSprite.rect):
            self.get_collected()

    


class Level:
    def __init__(self, arrayTable, colorHue=55):
        self.VICTORIA = pygame.event.Event(pygame.USEREVENT + 1, {"mensaje":"wawa"})
        self.DERROTA = pygame.event.Event(pygame.USEREVENT + 2)

        level_width = len(arrayTable[0])*48
        level_height = len(arrayTable)*48

        self.rect = pygame.Rect((0,0),(level_width,level_height))
        
        self._userInput = UserInput()

        
        self.enemy_group = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()
        self.ladder_group = pygame.sprite.Group()
        self.topladder_group = pygame.sprite.Group() ##
        self.coin_group = pygame.sprite.Group()

        self.player = Player(self._userInput.get_input(), self.block_group, self.ladder_group, self.topladder_group, colorHue=colorHue)

        self.camera = Camera(self.rect)
        
        self.camera.add_sprite(self.block_group)
        self.camera.add_sprite(self.ladder_group)
        self.camera.add_sprite(self.enemy_group)
        self.camera.add_sprite(self.coin_group)
        
        self.camera.add_sprite(self.player)

        
        
        for y in range(len(arrayTable)):
            for x in range(len(arrayTable[y])):
                character = arrayTable[y][x]
                if character == '=':   # Bloque
                    block = Block()
                    block.place(x*BLOCK_SIZE,y*BLOCK_SIZE)
                    self.block_group.add(block)
                
                elif arrayTable[y][x] == '#': # Escalera
                    ladder = Ladder()
                    ladder.place(x*BLOCK_SIZE,y*BLOCK_SIZE)
                    self.ladder_group.add(ladder)
                    ladder.set_group(self.ladder_group)
                    if ladder.is_top():
                        self.topladder_group.add(ladder)

                elif arrayTable[y][x] == '$': # Moneda
                    coin = Coin(self.player)
                    coin.place(x*BLOCK_SIZE,y*BLOCK_SIZE)
                    self.coin_group.add(coin)
                    
                
                elif arrayTable[y][x] == '!':
                    enemy = Enemy(self.block_group, self.ladder_group, self.topladder_group)
                    enemy.place(x*BLOCK_SIZE,y*BLOCK_SIZE)
                    enemy.set_focus(self.player)
                    self.enemy_group.add(enemy)
                    enemy.set_focus(self.player)

                elif character == '@':
                   self.player.place(x*BLOCK_SIZE,y*BLOCK_SIZE)               
                
        self.group = pygame.sprite.Group()
        

    def update(self):
        self._userInput.update()
        self.player.update()

        self.enemy_group.update()
        self.block_group.update()
        self.ladder_group.update()
        self.coin_group.update()

        player_center = self.player.rect.center

        #self.camera.track_sprite(self.player.rect.center)
        self.camera.update(player_center)

        if len(self.coin_group.sprites())==0:
            pygame.event.post(self.VICTORIA)
        #print(self.rect.bottom)
        #print(self.player.y)
        if self.player.y > self.rect.bottom:
            pygame.event.post(self.DERROTA)
        #    pass
        
    def draw(self, Surface):
        self.camera.draw(Surface)
        
        
