class Gamestats():
   """Track Stats for alien invasion"""
   
   def __init__(self, ai_settings):
      """Init Stats"""
      self.ai_settings = ai_settings
      self.reset_stats()
      
      #Start Alien Invasion in an active state
      self.game_active = False
      
      #High Score should never reset
      self.high_score = 0
      self.level = 1
      
   def reset_stats(self):
      """Init stats that can change during game"""
      self.ships_left = self.ai_settings.ship_limit
      self.score = 0
      self.level = 1