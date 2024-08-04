import pygame
from config  import *
import math
import random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file)

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
 
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        return sprite
        

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(432, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(432, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(480, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(528, 0, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(432, 144, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(480, 144, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(528, 144, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(432, 48, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(480, 48, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(528, 48, self.width, self.height)]

        self. right_animations = [self.game.character_spritesheet.get_sprite(432, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(480, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(528, 96, self.width, self.height)]

    def update(self):
        self.movimiento()
        self.animate()
        self.colision_enemigo()
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        self.x_change = 0
        self.y_change = 0
        self.colision_Portal()
        self.colision_CofreG()
        self.colision_CofreR()

    def movimiento(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self,direcion):
        if direcion == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED      
        if direcion == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
    def colision_enemigo(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
           self.kill()
           self.game.playing = False

    def colision_Portal(self):
        hits = pygame.sprite.spritecollide(self, self.game.Portal, False)
        if hits:
            if self.game.CofreG == True: 
              if  self.game.CofreR == True: 
                 self.game.Win = True
                 self.game.playing = False
    def colision_CofreG(self):
        hits = pygame.sprite.spritecollide(self, self.game.Item1, True)
        if hits:
           self.game.CofreG = True
    def colision_CofreR(self):
        hits = pygame.sprite.spritecollide(self, self.game.Item2, True)
        if hits: 
           self.game.CofreR = True
       
           
    def animate(self):

         if self.facing == "down":
             if  self.y_change == 0:
                  self.image = self.game.character_spritesheet.get_sprite(430, 0, self.width, self.height)
             else:
                 self.image = self.down_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1

         if self.facing == "up":
             if  self.y_change == 0:
                  self.image = self.game.character_spritesheet.get_sprite(430,144, self.width, self.height)
             else:
                 self.image = self.up_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1
         if self.facing == "right":
             if  self.x_change == 0:
                  self.image = self.game.character_spritesheet.get_sprite(430, 96, self.width, self.height)
             else:
                 self.image = self.right_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1
         if self.facing == "left":
             if  self.x_change == 0:
                  self.image = self.game.character_spritesheet.get_sprite(430, 48, self.width, self.height)
             else:
                 self.image = self.left_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game. enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movimiento_loop = 0
        self.max_travel = random.randint(7,30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 48, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(288, 240, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(336, 240, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(384, 240, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(288, 288, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(336, 288, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(384, 288, self.width, self.height)]

    def update(self):

        self.movimiento()
        self.animacion()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0  

    def movimiento(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movimiento_loop -= 1
            if self.movimiento_loop <= -self.max_travel:
                self.facing = 'right'
            
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movimiento_loop += 1
            if self.movimiento_loop >= self.max_travel:
                self.facing = 'left'
            
    def animacion(self):

         if self.facing == "right":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(288, 288, self.width, self.height)
             else:
                 self.image = self.right_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1
         if self.facing == "left":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(288, 240, self.width, self.height)
             else:
                 self.image = self.left_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1 
            
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game. enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movimiento_loop = 0
        self.max_travel = random.randint(7,30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 48, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(0, 48, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(48, 48, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(96, 48, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(0, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(48, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(96, 96, self.width, self.height)]

    def update(self):

        self.movimiento()
        self.animacion()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0  

    def movimiento(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movimiento_loop -= 1
            if self.movimiento_loop <= -self.max_travel:
                self.facing = 'right'
            
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movimiento_loop += 1
            if self.movimiento_loop >= self.max_travel:
                self.facing = 'left'
            
    def animacion(self):

         if self.facing == "right":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(0, 48, self.width, self.height)
             else:
                 self.image = self.right_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1
         if self.facing == "left":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(0, 96, self.width, self.height)
             else:
                 self.image = self.left_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1 

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game. enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movimiento_loop = 0
        self.max_travel = random.randint(7,30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 48, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(144,48, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(192, 48, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(240, 48, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(144, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(192, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(240, 96, self.width, self.height)]

    def update(self):

        self.movimiento()
        self.animacion()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0  

    def movimiento(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movimiento_loop -= 1
            if self.movimiento_loop <= -self.max_travel:
                self.facing = 'right'
            
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movimiento_loop += 1
            if self.movimiento_loop >= self.max_travel:
                self.facing = 'left'
            
    def animacion(self):

         if self.facing == "right":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(144, 96, self.width, self.height)
             else:
                 self.image = self.right_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1
         if self.facing == "left":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(144,48, self.width, self.height)
             else:
                 self.image = self.left_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1 

class Enemy4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game. enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movimiento_loop = 0
        self.max_travel = random.randint(7,30)

        self.image = self.game.enemy_spritesheet.get_sprite(288, 48, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(288,48, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(336, 48, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(384, 48, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(288, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(336, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(384, 96, self.width, self.height)]

    def update(self):

        self.movimiento()
        self.animacion()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0  

    def movimiento(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movimiento_loop -= 1
            if self.movimiento_loop <= -self.max_travel:
                self.facing = 'right'
            
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movimiento_loop += 1
            if self.movimiento_loop >= self.max_travel:
                self.facing = 'left'
            
    def animacion(self):

         if self.facing == "right":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(288, 96, self.width, self.height)
             else:
                 self.image = self.right_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1
         if self.facing == "left":
             if  self.x_change == 0:
                  self.image = self.game.enemy_spritesheet.get_sprite(288,48, self.width, self.height)
             else:
                 self.image = self.left_animations[math.floor(self.animation_loop)]
                 self.animation_loop += 0.1
                 if self.animation_loop >= 3:
                     self.animation_loop = 1 

class Block(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.ground_spritesheet.get_sprite(240,144, self.width, self.height)
       

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite): 
    def __init__(self, game, x , y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(580,170, self.width, self.height)
       

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground2(pygame.sprite.Sprite): 
    def __init__(self, game, x , y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain2_spritesheet.get_sprite(0,432, self.width, self.height)
       

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Wall(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Wall_spritesheet.get_sprite(211,347, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Rock(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Bosque_spritesheet.get_sprite(0,322, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
class Walls(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Walls_spritesheet.get_sprite(672,384, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class ARBUSTO(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = 5
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Vegetacion_spritesheet.get_sprite(672,288, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enrredaderas(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 96
        
        self.image = self.game.Enrredaderas_spritesheet.get_sprite(432,336, self.width, self.height)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Arbol(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 96
        
        self.image = self.game.Vegetacion_spritesheet.get_sprite(240,528, self.width, self.height)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class JAIL(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.JAIL_spritesheet.get_sprite(720,288, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Suelo(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Suelo_spritesheet.get_sprite(211,351, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Mansion(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Mansion_spritesheet.get_sprite(408,312, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Pared1(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(288,384, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Pared2(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(312,384, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Pared3(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(336,384, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Pared4(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(288,432, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Pared5(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(312,432, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Pared6(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(336,432, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class TumbaC(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Tumbas_spritesheet.get_sprite(672,144, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TumbaL(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.Tumbas_spritesheet.get_sprite(720,144, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Fuente(pygame.sprite.Sprite):  
    def __init__(self, game, x , y):
        self.game = game
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * SIZE64
        self.y = y * SIZE64
        self.width = SIZE64
        self.height = SIZE64
        
        self.image = self.game.Bosque_spritesheet.get_sprite(0,384, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y): 
        self.s = 0

        self.game = game
        self._layer = ATTACKSIZE
        self.groups = self.game.all_sprites, self.game.attacks
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = ATTACKSIZE
        self.height = ATTACKSIZE

        self.animation_loop = 0
        self.image = self.game.attacks_spritesheet.get_sprite(0,0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_attack = [self.game.attacksR_spritesheet.get_sprite(0, 768, self.width, self.height),
                           self.game.attacksR_spritesheet.get_sprite(0, 576, self.width, self.height),
                           self.game.attacksR_spritesheet.get_sprite(0, 384, self.width, self.height)]

        self.up_attack = [self.game.attacksU_spritesheet.get_sprite(768, 576, self.width, self.height),
                         self.game.attacksU_spritesheet.get_sprite(576, 576, self.width, self.height),
                         self.game.attacksU_spritesheet.get_sprite(384, 576, self.width, self.height)]

        self.left_attack = [self.game.attacksL_spritesheet.get_sprite(576, 0, self.width, self.height),
                           self.game.attacksL_spritesheet.get_sprite(576, 192, self.width, self.height),
                           self.game.attacksL_spritesheet.get_sprite(576, 384, self.width, self.height)]

        self.down_attack = [self.game.attacks_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.attacks_spritesheet.get_sprite(192, 0, self.width, self.height),
                            self.game.attacks_spritesheet.get_sprite(384, 0, self.width, self.height)]

    def update(self,):
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    


         

     
     

    def animate(self):
        direction = self.game.player.facing




        if direction == 'up':
            self.image = self.up_attack[math.floor(self.animation_loop)]
            self.animation_loop += 0.25
            if self.animation_loop>= 3:
                self.kill()
        if direction == 'down':
            self.image = self.down_attack[math.floor(self.animation_loop)]
            self.animation_loop += 0.25
            if self.animation_loop>= 3:
                self.kill()
        if direction == 'right':
            self.image = self.right_attack[math.floor(self.animation_loop)]
            self.animation_loop += 0.25
            if self.animation_loop>= 3:
                self.kill()
        if direction == 'left':
            self.image = self.left_attack[math.floor(self.animation_loop)]
            self.animation_loop += 0.25
            if self.animation_loop>= 3:
                self.kill()

class CASCADA(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = 192
        self.groups = self.game.all_sprites
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 1830
        self.y = -20
        self.width = 192
        self.height = 192

        self.animation_loop = 0
        self.image = self.game.CASCADA_spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.CASCADA = [self.game.CASCADA_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.CASCADA_spritesheet.get_sprite(192, 0, self.width, self.height),
                           self.game.CASCADA_spritesheet.get_sprite(384, 0, self.width, self.height),
                           self.game.CASCADA_spritesheet.get_sprite(576, 0, self.width, self.height)]



    def update(self,):
        self.animate()
     
    
    
     

    def animate(self):
            self.image = self.CASCADA[math.floor(self.animation_loop)]
            self.animation_loop += 0.15
            if self.animation_loop >= 4:
                     self.animation_loop = 1 


class CofreG(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.Item1
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.Cofres_spritesheet.get_sprite(144,192, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.CofreR = [self.game.Cofres_spritesheet.get_sprite(144, 192, self.width, self.height),
                           self.game.Cofres_spritesheet.get_sprite(144, 240, self.width, self.height),
                           self.game.Cofres_spritesheet.get_sprite(144, 288, self.width, self.height),
                           self.game.Cofres_spritesheet.get_sprite(144, 336, self.width, self.height)]



    def update(self,):
        self.animate()

     


    def animate(self):
            self.image = self.CofreR[math.floor(self.animation_loop)]
            self.animation_loop += 0.09
            if self.animation_loop >= 4:
                     self.animation_loop = 1 

class CofreR(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.Item2
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.Cofres_spritesheet.get_sprite(144,192, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.CofreR = [self.game.Cofres_spritesheet.get_sprite(432, 192, self.width, self.height),
                           self.game.Cofres_spritesheet.get_sprite(432, 240, self.width, self.height),
                           self.game.Cofres_spritesheet.get_sprite(432, 288, self.width, self.height),
                           self.game.Cofres_spritesheet.get_sprite(432, 336, self.width, self.height)]



    def update(self,):
        self.animate()

     


    def animate(self):
            self.image = self.CofreR[math.floor(self.animation_loop)]
            self.animation_loop += 0.09
            if self.animation_loop >= 4:
                     self.animation_loop = 1

class Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.Portal
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.Portal_spritesheet.get_sprite(0,144, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.CofreR = [self.game.Portal_spritesheet.get_sprite(0, 144, self.width, self.height),
                           self.game.Portal_spritesheet.get_sprite(48, 144, self.width, self.height),
                           self.game.Portal_spritesheet.get_sprite(96, 144, self.width, self.height)]



    def update(self,):
        self.animate()

     


    def animate(self):
            self.image = self.CofreR[math.floor(self.animation_loop)]
            self.animation_loop += 0.3
            if self.animation_loop >= 3:
                     self.animation_loop = 1 

class boton:
    def __init__(self,x,y,width, height, fg, bg, content, fontsize):
        self.font = pygame.font.SysFont('arial', 32)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height


        self.bg = bg
        self.fg = fg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))   
        self.image.blit(self.text, self.text_rect) 
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False 
