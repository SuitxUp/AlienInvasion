class Settings():
   """A class to store settings for the Alien invasion"""
   
   def __init__(self):
      self.screen_width = 1200
      self.screen_height = 800
      self.bg_color = (230,230,230)
      
      #Ship settings
      self.ship_speed_factor = 1.5
      self.ship_limit = 3
      
      #Bullet Settings
      self.bullet_speed_factor = 3
      self.bullet_width = 3
      self.bullet_height = 15
      self.bullet_color = 60, 60, 60
      self.bullets_allowed = 3
      
      #Alien settings
      self.alien_speed_factor = 1
      self.fleet_drop_speed = 10
      #fleet direction 1 represent right and -1 represent left
      self.fleet_direction = 1