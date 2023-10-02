import pygame

class Ship():
   
   def __init__(self, ai_settings, screen):
      """ Init the ship and set starting position """
      self.screen = screen
      
      #Load ship image
      self.image = pygame.image.load("ship.bmp")
      self.rect = self.image.get_rect()
      self.screen_rect = screen.get_rect()
      self.ai_settings = ai_settings
      
      #Start each new ship at the bottom center of the screen
      self.rect.centerx = self.screen_rect.centerx
      self.rect.bottom = self.screen_rect.bottom
      
      #Store value for ships center
      self.center = float(self.rect.centerx)
      
      #Move Flags
      self.moving_right = False
      self.moving_left = False
      
   def update(self):
      """Update the ship's position on the movement flags"""
      if self.moving_right and self.rect.right < self.screen_rect.right:
         self.rect.centerx += self.ai_settings.ship_speed_factor
         
      if self.moving_left and self.rect.left > 0:
         self.rect.centerx -= self.ai_settings.ship_speed_factor
      
      #Update rect object from self.center
      #self.rect.centerx = self.center
      
   def blitme(self):
      """Draw ship at current location"""
      self.screen.blit(self.image, self.rect)
      
   def center_ship(self):
      """Center the ship on the screen"""
      self.center = self.screen_rect.centerx