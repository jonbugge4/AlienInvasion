## install pip module with: python3 -m pip install --user pygame
import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game, and create game resources'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height


        #self.screen = pygame.display.set_mode(
            #(self.settings.screen_width, self.settings.screen_height))
            
        #This appeared on page 231 (line below)
        pygame.display.set_caption("Alien Invasion")


        #Create an instance to store game statistics
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.__create_fleet()

        #Set the background color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self.__check_events()
            self.ship.update()
            self.__update_bullets()
            self.__update_aliens()
            self.__update_screen()
            

    def __check_events(self):
        '''Respond to keypresses and mouse events.'''
            # watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.__check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.__check_keyup_events(event)

    def __check_keydown_events(self, event):
        '''Respond to keypresses'''
        if event.type == pygame.K_RIGHT:
            #move the ship to the right.
            self.ship.rect.x += 1
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.__fire_bullet()

    def __check_keyup_events(self, event):
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.type == pygame.K_LEFT:
                self.ship.moving_left = False

    def __fire_bullet(self):
        '''Create a new bullet and add it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def __update_bullets(self):
        '''Update position of bullets and get rid of old bullets.'''
        #Update bullet positions
        self.bullets.update()
        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            self.__check_bullet_alien_collisions()

    def __check_bullet_alien_collision(self):
        '''Respond to bullet-alien collisions'''
        #remove any bullets that have collided with aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

    
        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self.create_fleet()

    def __update_aliens(self):
        '''Check if the fleet is at an edge,
        then update the postion of all aliens in the fleet'''
        self.__check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collsions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.__ship_hit()
        
    def __update_screen(self):
            '''Update images on the screen, and flip to the new screen'''
            # Redraw the screen during each pass through the loop
            self.screen.fill (self.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

    def __create_fleet(self):
        '''Create the fleet of aliens'''
        #Make an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2* alien_width)

        #Determin the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                        (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens.
        for row_number in range (number_rows):
            for alien_number in range(number_aliens_x):
                self.__create_alien(alien_number, row_number)

    def __create_alien(self, alien_number, row_number):
            #Create an alien and place it in the row
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.xself.aliens.add(alien)
            alien.rect.y = alien_height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def __check_fleet_edges(self):
        '''Respond appropraitley if any aliens have reached an edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.__change_fleet_direction()
                break

    def __change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def __ship_hit(self):
        '''Respond to the ship being hit by an alien'''

        #Decrememnt ships left
        self.stats.ships_left -= 1

        #Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet and center the ship
        self.__create_fleet()
        self.ship.center_ship()

        #Pause.
        sleep(0.5)

            # Make the most recently drawn screen available
    pygame.display.flip()

if __name__ == '__main__':
    #make a game instance, and run the game
    ai =AlienInvasion()
    ai.run_game()
