import pygame
from userinput import UserInput
import os
import json

from colorchange import change_color

BLOCK_SIZE=48

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

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

    def soft_collision(self):
        left = False
        right = False
        top = False
        bottom = False
        
        collRect = self.rect.copy()
        collRect.x -= 1
        collision_index = collRect.collidelist(self.collisions.sprites())
        if collision_index != -1:
            left = True
        collRect.x += 2
        collision_index = collRect.collidelist(self.collisions.sprites())
        if collision_index != -1:
            right = True

        collRect = self.rect.copy()
        collRect.y -= 1
        collision_index = collRect.collidelist(self.collisions.sprites())
        if collision_index != -1:
            top = True
        collRect.y += 2
        collision_index = collRect.collidelist(self.collisions.sprites())        
        if collision_index != -1:
            bottom = True

        return (left, right, top, bottom)
        

    def on_floor(self):
        collRect = self.rect.copy()
        collRect.y += 1
        ladder_list = self.topLadders.sprites()

        collision_index = collRect.collidelist(self.collisions.sprites())
        ladd_coll_index = collRect.collidelist(ladder_list)

        normal_collision = (collision_index != -1)
        ladder_collision = (ladd_coll_index != -1) and ladder_list[ladd_coll_index] and (self.rect.bottom <= ladder_list[ladd_coll_index].rect.top)
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

    def draw(self, Surface):
        Surface.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, Input, collisionGroup, ladderGroup, topLadderGroup, colorHue=55):
        Entity.__init__(self)
        self.sprite = {}
        path = os.path.join(os.path.dirname(__file__), "resource/sprite/idle.png")
        self.sprite["idle"] = pygame.image.load(path)
        #self.sprite["idle"] = pygame.image.load("./resource/e/idle.png")
        change_color(self.sprite["idle"],55, colorHue)
         
        self.image = self.sprite["idle"]
        
        self.rect = self.image.get_rect()
        self.centerrect = pygame.Rect((self.rect.center),(1,1))
        
        self._input = Input
        self.collisions = collisionGroup
        self.ladders = ladderGroup
        self.topLadders = topLadderGroup
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0

        self.state = "default"


    def place(self, x, y):
        self.rect.centerx = x+(BLOCK_SIZE//2)
        self.rect.bottom = y+BLOCK_SIZE

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



######## ################ ################ ################ ########
######     ############     ############     ############     ######
####         ########         ########         ########         ####
####         ########         ########         ########         ####
######     ############     ############     ############     ######
######## ################ ################ ################ ########
######     ############     ############     ############     ######
####         ########         ########         ########         ####
####         ########         ########         ########         ####
######     ############     ############     ############     ######
######## ################ ################ ################ ########
######     ############     ############     ############     ######
####         ########         ########         ########         ####
####         ########         ########         ########         ####
######     ############     ############     ############     ######
######## ################ ################ ################ ########
######     ############     ############     ############     ######
####         ########         ########         ########         ####
####         ########         ########         ########         ####
######     ############     ############     ############     ######
######## ################ ################ ################ ########



class Enemy(Entity):
    def __init__(self, collisionGroup, ladderGroup, topLadderGroup):
        Entity.__init__(self)
        self.sprite = {}

        self.size = (30,30)
        self.image = pygame.Surface(self.size)
        self.image.fill("#FF0000")
        
        self.rect = self.image.get_rect()
        self.centerrect = pygame.Rect((self.rect.center),(1,1))
        
        self.collisions = collisionGroup
        self.ladders = ladderGroup
        self.topLadders = topLadderGroup

        self.focus_sprite = None
        
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0

        self.state = "default"
        self.R_facing = True

        self.recent_ladder = False
        self.lastladder_index = -1

    def detect_cliff(self):
        collRect = self.rect.copy()
        collRect.y += 1

        if self.R_facing:
            collRect.x += self.size[0]
        else:
            collRect.x -= self.size[0]

        collision_index = collRect.collidelist(self.collisions.sprites())
        lcollision_index = collRect.collidelist(self.topLadders.sprites())

        return (collision_index == -1) and (lcollision_index == -1)

        

    def set_focus(self, focus):
        self.focus_sprite = focus

    def focus_Xdistance(self):
        x = self.focus_sprite.rect.centerx - self.rect.centerx
        return x

    def focus_Ydistance(self):
        top = self.rect.top - self.focus_sprite.rect.bottom
        bottom = self.focus_sprite.rect.top - self.rect.bottom
        return (top, bottom)

    def place(self, x, y):
        self.rect.centerx = x+(BLOCK_SIZE//2)
        self.rect.bottom = y+BLOCK_SIZE
        

    def update_state(self):
        pass

    def set_vel(self):
        #recent_ladder = False
        if self.state == "default":
            if self.on_floor():
                self.vel_x = 5

                if self.recent_ladder:
                    collide_lastladder = (self.on_ladder() == self.lastladder_index)
                    if not collide_lastladder:
                        self.recent_ladder = False
                rl_condition = (not self.recent_ladder) or (self.lastladder_index == -1)

                if not self.R_facing:
                    self.vel_x *= -1           
    
                collisions = self.soft_collision()
                if collisions[0]:
                    self.R_facing = True
                elif collisions[1]:
                    self.R_facing = False
        
                if self.detect_cliff():
                    self.R_facing = not self.R_facing

                if (self.center_on_ladder()!=-1) and self.focus_Ydistance()[0]>10 and rl_condition:
                    self.state = "ladder"
                    self.vel_y = -2
                elif (self.floor_isladder()) and self.focus_Ydistance()[1]>10 and rl_condition:
                    self.state = "ladder"
                    self.vel_y = 2


            
        elif self.state == "ladder":
            index = self.on_ladder()
            current_ladder = self.ladders.sprites()[index]
            ladderCenter = current_ladder.rect.centerx
            self.vel_x = 0
            groundCondition = self.on_floor()
            on_ladder = (self.on_ladder() != -1)

            if (index != -1):
                self.rect.centerx = ladderCenter
                self.lastladder_index = index
                if self.focus_Xdistance() < 0:
                    self.R_facing = False
                else:
                    self.R_facing = True
                    
            if groundCondition or not on_ladder:                    
                self.state = "default"
                self.vel_y=0
                self.recent_ladder = True                
                

    def update(self):
        self.set_vel()
        self.update_state()
        self.move_and_collide()
        self.centerrect.center = self.rect.center
        self.x = self.rect.bottom
        self.y = self.rect.centery
