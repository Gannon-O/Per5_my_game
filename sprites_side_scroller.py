# This file was created by: Gannon O'Leary

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
import time
import os
from math import floor
from utils import Cooldown
vec = pg.math.Vector2


# create the player class with a superclass of Sprite
class Player(Sprite):
    # this initializes the properties of the player class including the x y location, and the game parameter so that the the player can interact logically with other elements in the game...
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((32, 32))
        # self.image.fill((255, 0, 0))
        self.image = self.game.player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.pos= vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        # self.vx, self.vy = 0, 0
        self.coin_count = 0
        self.coins = 0
        self.jump_power = 15
        self.jumping = False
        self.powerup_cd = Cooldown()
        self.cd = Cooldown()
        self.can_collect_powerup = True
    def get_keys(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.vy -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        # if keys[pg.K_s]:
        #     self.vy += self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_snd.play()
            self.jumping = True
            self.vel.y = -self.jump_power
     
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
            
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits [0].__class__.__name__) == "Powerup" and self.can_collect_powerup:
                self.speed = 10
                self.can_collect_powerup = False
                self.powerup_cd.event_time = floor(pg.time.get_ticks()/1000)
        
            if str(hits[0].__class__.__name__) == "Coin":
                self.coin_count += 1
            if str(hits[0].__class__.__name__) == "Portal":
                self.game.load_next_level()
    def update(self):
        self.powerup_cd.ticking()
        if self.powerup_cd.delta > 1:
            self.can_collect_powerup = True
        if self.can_collect_powerup:
            self.collide_with_stuff(self.game.all_powerups, True)

        self.acc = vec(0, GRAVITY)
        self.get_keys()
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc
    
        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        # teleport the player to the other side of the screen
        self.collide_with_stuff(self.game.all_coins, True)
        if self.collide_with_stuff(self.game.all_portals, False) and self.coins > 7:
            self.game.load_next_level()
        

    

# added Mob - moving objects
# it is a child class of Sprite
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image = self.game.mob_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 25

    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

        if self.rect.colliderect(self.game.player):
            self.speed *= -1

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.wall_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(PINK)
        self.image = self.game.powerup_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GOLD)
        self.image = self.game.coin_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Portal(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_portals
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.portal_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE   
