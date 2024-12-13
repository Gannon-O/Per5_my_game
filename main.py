# this file was created by: Gannon O'Leary

# this is where we import libraries and modules
import pygame as pg
from settings import *
# from sprites import *
from sprites_side_scroller import *
from tilemap import *
from os import path
import sys
from utils import *

# we are editing this file after installing git

'''
GOALS: Add lives, shooting mobs, death, more levels 5 or 10, must collect all coins
RULES:
FEEDBACK:
FREEDOM:

What's the sentence: Player 1 collides with enemy and enemy bounces off...

'''

'''
Sources: 
Chat GPT - Prompt: make me a 32x24 videogame map similar to the one I have where P = Player,M=Mob,1=Wall
Base Code
Mr. Cozort Lectures
'''
# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    # sound mixer...
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Gannon's Coolest Game Ever...")
    self.playing = True
    self.currentLevel = 1
    self.score = 0
    self.time_to_complete = 0
    self.running = True
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    

    # with open(path.join(self.game_folder, HS_FILE), 'w') as f:
    #   f.write(str(0))
    # try:
    #   with open(path.join(self.game_folder,HS_FILE), 'r') as f:
    #     self.best_time = int(f.read())
    # except:
    #   with open(path.join(self.game_folder, HS_FILE), 'w') as f:
    #     f.write(str(0))
    self.check_highscore()
      
    self.snd_folder = path.join(self.game_folder, 'sounds')
    self.img_folder = path.join(self.game_folder, 'images')
    self.player_img = pg.image.load(path.join(self.img_folder, 'sprite.png'))
    self.coin_img = pg.image.load(path.join(self.img_folder, 'coin.png'))
    self.powerup_img = pg.image.load(path.join(self.img_folder, 'powerup.png'))
    self.portal_img = pg.image.load(path.join(self.img_folder, 'portal.png'))
    self.mob_img = pg.image.load(path.join(self.img_folder, 'mob.png'))
    self.wall_img = pg.image.load(path.join(self.img_folder, 'wall.png'))
  # select the map file 
    self.game_folder = path.dirname(__file__)
  # selects the map folder we want to use
    self.map = Map(path.join(self.game_folder,'level1.txt'))
  # loads the new level when checkpoint is reached
  # load sounds
    self.jump_snd = pg.mixer.Sound(path.join(self.snd_folder, 'boing.ogg'))
    pg.mixer.music.load(path.join(self.snd_folder, 'bckgrd.ogg'))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(loops=-1)
  def load_next_level(self):
    # kills all sprites to free memory
    self.currentLevel +=1
    for s in self.all_sprites:
      s.kill()
      print(len(self.all_sprites))
      # from load data to create new map object with level parameter
    self.map = Map(path.join(self.game_folder,"level" + str(self.currentLevel) + ".txt")) 
  
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'U':
          Powerup(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
        if tile == 'E':
           Portal(self, col, row)
  def check_highscore(self):
 # if the file exists
        if path.exists(HS_FILE):
          print("this exists...")
          with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                self.best_time = int(f.read())
        else:
          with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                self.best_time =  100000
                f.write(str(100000))
        print("File created and written successfully.")
  def new(self):
    self.load_data()
    print(self.map.data)
    self.game_timer = Timer(self)

    # create the all sprites group to allow for batch updates and draw methods

    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_portals = pg.sprite.Group()
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'U':
          Powerup(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
        if tile == 'E':
           Portal(self, col, row)
    
    
    for i in range(1000):
      Powerup(self,randint(0, WIDTH),randint(0, HEIGHT))
# this is a method
# methods are like functions that are part of a class
# the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()

    pg.quit()
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          print(self.game_timer.current_time)
          if self.game_timer.current_time < self.best_time:
            print("i got a best time")
            print(self.game_timer.current_time)
            print(self.best_time)
            self.best_time = self.game_timer.current_time
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
              f.write(str(self.game_timer.current_time))
          if self.playing:
            self.playing = False
          self.running = False
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites...and I MEAN ALL OF THEM
    self.all_sprites.update()
    self.game_timer.ticking()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect) 
  # output
  def draw(self):
    self.screen.fill((BLACK))
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, "Coins:" + str(self.player.coin_count), 24, WHITE, WIDTH/30, HEIGHT/15)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.game_timer.current_time), 24, WHITE, WIDTH/30, HEIGHT/10)
    self.draw_text(self.screen, "Best time is " + str(self.best_time), 24, WHITE, WIDTH-900, HEIGHT/200)

    pg.display.flip()
if __name__ == "__main__":
  # instantiate
  print("main is running...")
  g = Game()
  print("main is running...")
  g.new()
  g.run()
 