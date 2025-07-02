import pygame
from userinput import UserInput
import os
import json

BLOCK_SIZE=48


class Player(pygame.sprite.Sprite):
    def __init__(self, Input, collisionGroup, ladderGroup):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = {}
        path = os.path.join(os.path.dirname(__file__), "resource/e/idle.png")
        self.sprite["idle"] = pygame.image.load(path)
        #self.sprite["idle"] = pygame.image.load("./resource/e/idle.png")
         
        self.image = self.sprite["idle"]
        
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

    def update_sprite(self):
        pass


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
