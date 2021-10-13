## install pip module with: python3 -m pip install --user pygame
import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
            print(len(self.bullets))
        
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
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2* alien_width)

        #Create the first row of aliens
        for alien_number in range(number_aliens_x):
            #Create an alien and place it in the row
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.xself.aliens.add(alien)

            # Make the most recently drawn screen available
        pygame.display.flip()

if __name__ == '__main__':
    #make a game instance, and run the game
    ai =AlienInvasion()
    ai.run_game()
