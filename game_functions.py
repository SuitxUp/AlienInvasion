import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
   """Respond to keypresses and mouse events"""

   #key inputs
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
         
      elif event.type == pygame.KEYDOWN:
         check_keydown_events(event, ai_settings, screen, ship, bullets)
            
      elif event.type == pygame.KEYUP:
         check_keyup_events(event, ship)
         
      elif event.type == pygame.MOUSEBUTTONDOWN:
         mouse_x, mouse_y = pygame.mouse.get_pos()
         check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
         
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
   """Start a new game when the player clicks Play"""
   button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
   if button_clicked and not stats.game_active:
      #Reset the game settings
      ai_settings.initilize_dynamic_settings()
      
      #Hide the mouse cursor
      pygame.mouse.set_visible(False)
      
      #Reset the game stats
      stats.reset_stats()
      stats.game_active = True
      
      #Reset the scoreboard images
      sb.prep_score()
      sb.prep_high_score()
      sb.prep_level()
      sb.prep_ships()
      
      #Empty lists
      aliens.empty()
      bullets.empty()
      
      #Create a new fleet and center the ship
      create_fleet(ai_settings, screen, ship, aliens)
      ship.center_ship()
      
            
def check_keydown_events(event, ai_settings, screen, ship, bullets):
   """Respond to Keypresses"""
   if event.key == pygame.K_RIGHT:
      #Move the shit to the right
      ship.moving_right = True
   elif event.key == pygame.K_LEFT:
      ship.moving_left = True
   elif event.key == pygame.K_SPACE:
      fire_bullet(ai_settings, screen, ship, bullets)
      
def check_keyup_events(event, ship):
   """Respond to key releases"""
   if event.key == pygame.K_RIGHT:
      ship.moving_right = False
   elif event.key == pygame.K_LEFT:
      ship.moving_left = False
      
def fire_bullet(ai_settings, screen, ship, bullets):
   """Fire a bullet if limit not reached"""
   if len(bullets) < ai_settings.bullets_allowed:
      new_bullet = Bullet(ai_settings, screen, ship)
      bullets.add(new_bullet)
      
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
   """Update Position of bullets and get rid of fold bullets"""
   bullets.update()
   
   #Get rid of old bullets for memory consumption
   for bullet in bullets.copy():
      if bullet.rect.bottom <= 0:
         bullets.remove(bullet)
   #print(len(bullets)) debug statement
   
   check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
   
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
   """Respond to bullet-alien collisions"""
   #check for bullets that have hit
   collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

   if collisions:
      for aliens in collisions.values():
         stats.score += ai_settings.alien_points * len(aliens)
         sb.prep_score()
      check_high_score(stats, sb)

   if len(aliens) == 0:
      #Destroy existing bullets and create a new fleet
      bullets.empty()
      ai_settings.increase_speed()
      
      #Increase Level 
      stats.level += 1
      sb.prep_level()
      
      create_fleet(ai_settings, screen, ship, aliens)
   
def get_number_aliens_x(ai_settings, alien_width):
   """Determine number of aliens that fit in a row"""
   available_space_x = ai_settings.screen_width - 2*alien_width
   number_aliens_x = int(available_space_x / (2*alien_width))
   return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
   """Determine the number of rows of aliens that fit on the screen"""
   available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
   number_rows = int(available_space_y / (2*alien_height))
   return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
   """Create an alien and place it in a row"""
   alien = Alien(ai_settings, screen)
   alien_width = alien.rect.width
   alien.x = alien_width + 2*alien_width * alien_number
   alien.rect.x = alien.x
   alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
   aliens.add(alien)
   
def create_fleet(ai_settings, screen, ship, aliens):
   """Create a full fleet of aliens"""
   #Create an alien and find the number of aliens in a row
   #Spacing between each alien is equal to one alien width
   alien = Alien(ai_settings, screen)
   number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
   number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
   
   #Create rows of aliens
   for row_number in range(number_rows):
      for alien_number in range(number_aliens_x):
         #Create an alien and place it in the row
         create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
   """Respond to aliens reaching edge"""
   for alien in aliens.sprites():
      if alien.check_edges():
         change_fleet_direction(ai_settings, aliens)
         break
      
def change_fleet_direction(ai_settings, aliens):
   """Drop the entire fleet and change direction"""
   for alien in aliens.sprites():
      alien.rect.y += ai_settings.fleet_drop_speed
   ai_settings.fleet_direction *= -1
   
def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
   """Respond to ship being hit by alien"""
   
   if stats.ships_left > 0:
      #Decrement ships_left
      stats.ships_left -= 1
      
      #Update scoreboard
      sb.prep_ships()
      
      #Empty the list of aliens and bullets
      aliens.empty()
      bullets.empty()
      
      #Create a new fleet and center the ship
      create_fleet(ai_settings, screen, ship, aliens)
      ship.center_ship()
      
   else:
      stats.game_active = False
      pygame.mouse.set_visible(True)
   
   #Pause
   sleep(0.5)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
   """Check if any aliens have reached the bottom of the screen"""
   screen_rect = screen.get_rect()
   for alien in aliens.sprites():
      if alien.rect.bottom >= screen_rect.bottom:
         #Treat this the same as if the ship got hit
         ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
         break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
   """Update the position of all aliens in the fleet"""
   check_fleet_edges(ai_settings, aliens)
   aliens.update()
   
   #Look if alien ship collided
   if pygame.sprite.spritecollideany(ship, aliens):
      ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
      
   #Look for aliens hitting bottom of screen
   check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
            
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
   """Update images on the sceen and flip to the new screen"""
   #Redraw Screen during each pass
   screen.fill(ai_settings.bg_color)
   
   for bullet in bullets.sprites():
      bullet.draw_bullet()
      
   ship.blitme()
   aliens.draw(screen)
   
   #Draw scoreboard
   sb.show_score()
   
   #Draw the play button
   if not stats.game_active:
      play_button.draw_button()
      
   #Make Visible
   pygame.display.flip()
   
def check_high_score(stats, sb):
   """Check for new high score"""
   if stats.score > stats.high_score:
      stats.high_score = stats.score
      sb.prep_high_score()