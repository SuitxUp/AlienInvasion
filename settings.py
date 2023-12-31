class Settings():
   """A class to store settings for the Alien invasion"""
   
   def __init__(self):
      self.screen_width = 1200
      self.screen_height = 800
      self.bg_color = (230,230,230)
      
      #Ship settings
      self.ship_limit = 3
      
      #Bullet Settings
      self.bullet_width = 300
      self.bullet_height = 15
      self.bullet_color = 60, 60, 60
      self.bullets_allowed = 3
      
      #Alien settings
      self.fleet_drop_speed = 20
      
      #Speed up per level
      self.speedup_scale = 1.1
      self.score_scale = 1.5
      
      self.initilize_dynamic_settings()
      
   def initilize_dynamic_settings(self):
      """Initilize settings that change in game"""
      self.ship_speed_factor = 1.5
      self.bullet_speed_factor = 3
      self.alien_speed_factor = 1
      
      #fleet direction 1 represent right and -1 represent left
      self.fleet_direction = 1
      
      #Scoring
      self.alien_points = 50
      
   def increase_speed(self):
      """Increase speed settings"""
      self.ship_speed_factor *= self.speedup_scale
      self.bullet_speed_factor *= self.speedup_scale
      self.alien_speed_factor *= self.speedup_scale
      self.alien_points = int(self.alien_points * self.score_scale)
         