import pygame
from userinput import UserInput

BLOCK_SIZE=48

def draw_spriteDisplacement(sprite, displacement, Surface):
    copy  = sprite.rect.copy()

    copy.center = (sprite.rect.centerx+displacement[0] , sprite.rect.centery+displacement[1])

    Surface.blit(sprite.image, copy)
    

class Player(pygame.sprite.Sprite):
    def __init__(self, Input, collisionGroup, ladderGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((36,40))
        self.image.fill(pygame.Color('#10FF10'))
        self.rect = self.image.get_rect()
        self.centerrect = pygame.Rect((self.rect.center),(1,1))
        
        self._input = Input
        self.collisions = collisionGroup
        self.ladders = ladderGroup
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0

        self.state = "default"


    def place(self, x, y):
        self.rect.centerx = x+(BLOCK_SIZE//2)
        self.rect.bottom = y+BLOCK_SIZE

        
    def draw(self, Surface):
        Surface.blit(self.image, self.rect)

    def move_and_collide(self):
        collisionList = self.collisions.sprites()        
        
        # Colisiones comunes
        collRect = self.rect.copy()
        
        collRect.x += self.vel_x
        collision_index = collRect.collidelist(collisionList)
        if collision_index >= 0:
            if collRect.centerx < collisionList[collision_index].rect.centerx:
                collRect.right = collisionList[collision_index].rect.left
            else:
                collRect.left = collisionList[collision_index].rect.right

        collRect.y += self.vel_y
        collision_index = collRect.collidelist(collisionList)
        
        if collision_index >= 0:
            if collRect.centery < collisionList[collision_index].rect.centery:
                collRect.bottom = collisionList[collision_index].rect.top
            else:
                collRect.top = collisionList[collision_index].rect.bottom

        self.rect.x = collRect.x
        self.rect.y = collRect.y

    def on_floor(self):
        collRect = self.rect.copy()
        collRect.y += 1
        ladder_list = self.ladders.sprites()

        collision_index = collRect.collidelist(self.collisions.sprites())
        ladd_coll_index = collRect.collidelist(ladder_list)

        normal_collision = (collision_index != -1)
        ladder_collision = (ladd_coll_index != -1) and ladder_list[ladd_coll_index].is_top() and (self.rect.bottom <= ladder_list[ladd_coll_index].rect.top)
        #print(ladder_collision)
        
        if normal_collision or ladder_collision:
            return True
        else:
            return False

    def on_ladder(self):
        
        collision_index = self.rect.collidelist(self.ladders.sprites())
        return collision_index

    def center_on_ladder(self):        
        collision_index = self.centerrect.collidelist(self.ladders.sprites())
        return collision_index

    def floor_isladder(self):
        collRect = self.centerrect.copy()
        collRect.y += self.rect.height//2
        ladder_list = self.ladders.sprites()

        collision_index = collRect.collidelist(ladder_list)

        return collision_index != -1

    def update_state(self):
        if self.state == "default":
            if (self.center_on_ladder()!=-1) and self._input[1]==1 and self.on_floor():
                self.state = "ladder"
            elif (self.center_on_ladder()!=-1) and self._input[1] and not self.on_floor():
                self.state = "ladder"
            elif (self.floor_isladder()) and self._input[1]==-1 and self.on_floor():
                self.rect.y += 1
                self.state = "ladder"
                
        elif self.state == "ladder":
            if self._input[2]:
                self.state = "default"
            groundCondition = self.on_floor() and (self._input[1] == -1)
            on_ladder = self.on_ladder() != -1
            if groundCondition or not on_ladder:
                self.state = "default"
                

    def set_vel(self):
        if self.state == "default":
            if self.on_floor():
                self.vel_y = 0
                if self._input[0]:
                    self.vel_x = self._input[0]*(4)
                else:
                    self.vel_x = 0

                if self._input[2]:
                    self.vel_y = -6
            else:
                self.vel_y += 0.4
            
        elif self.state == "ladder":
            index = self.on_ladder()
            current_ladder = self.ladders.sprites()[index]
            ladderCenter = current_ladder.rect.centerx
            self.vel_x = 0
            groundCondition = self.on_floor() and (self._input[1] == -1)
            
            if (index != -1) and not groundCondition:
                self.rect.centerx = ladderCenter                
                if self._input[1] == 1:
                    self.vel_y = -3
                elif self._input[1] == -1:
                    self.vel_y = 3
                else:
                    self.vel_y = 0
            else:
                self.vel_y = 0

            
    
    def update(self):
        self.set_vel()
        self.update_state()
        self.move_and_collide()
        self.centerrect.center = self.rect.center
        self.x = self.rect.bottom
        self.y = self.rect.centery


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
        self.frame = frame
        self.margin = 48
        self._width = 920
        self._height = 690
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(0, 0, self._width, self._height)
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
        self.x = X
        self.rect.centerx = X
        
        if self.rect.right > self.frame.right+self.margin:
            self.rect.right = self.frame.right+self.margin
            self.x = self.rect.centerx
        elif self.rect.left < self.frame.left-self.margin:
            self.rect.left = self.frame.left-self.margin
            self.x = self.rect.centerx

    def track_y(self, Y):
        self.y = Y
        self.rect.centery = Y

        if self.rect.bottom > self.frame.bottom+self.margin:
            self.rect.bottom = self.frame.bottom+self.margin
            self.y = self.rect.centery
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
    def __init__(self, arrayTable):
        self.VICTORIA = pygame.event.Event(pygame.USEREVENT + 1, {"mensaje":"wawa"})
        self.DERROTA = pygame.event.Event(pygame.USEREVENT + 2)

        level_width = len(arrayTable[0])*48
        level_height = len(arrayTable)*48

        self.rect = pygame.Rect((0,0),(level_width,level_height))
        
        self._userInput = UserInput()

        
        self.enemy_group = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()
        self.ladder_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()

        self.player = Player(self._userInput.get_input(), self.block_group, self.ladder_group)

        self.camera = Camera(self.rect) #
        self.camera.add_sprite(self.enemy_group)
        self.camera.add_sprite(self.block_group)
        self.camera.add_sprite(self.ladder_group)
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

                elif arrayTable[y][x] == '$': # Moneda
                    coin = Coin(self.player)
                    coin.place(x*BLOCK_SIZE,y*BLOCK_SIZE)
                    self.coin_group.add(coin)
                    
                
                #elif arrayTable[y][x] == enemyCharacter:
                #   enemy = EnemyClass()
                #   enemy.place(x,y)
                #   add_to_enemyGroup

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
        
        
