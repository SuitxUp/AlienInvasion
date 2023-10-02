import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from game_stats import Gamestats

def run_game():
   #Initialize game and create a screen object
   pygame.init()
   ai_settings = Settings()
   screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
   pygame.display.set_caption("Alien Invasion")
   
   #Instance to store stats
   stats = Gamestats(ai_settings)
   
   #Clock
   clock = pygame.time.Clock()
   
   #Make a ship
   ship = Ship(ai_settings, screen)
   
   #Group to store bullets in
   bullets = Group()
   
   #Group to store aliens in
   aliens = Group()
   
   #Make an alien fleet
   gf.create_fleet(ai_settings, screen, ship, aliens)
   
   #Start the main loop for the game
   while True:
      
      clock.tick(100)
      gf.check_events(ai_settings, screen, ship, bullets)
      
      if stats.game_active:
         ship.update()
         gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
         gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
         
      gf.update_screen(ai_settings, screen, ship, aliens, bullets)
      
run_game()