class Settings:
    '''A class to store all settings for Alient Invasion'''

    def __init__(self):
        '''Initialize the game's statistic settings'''
        #screen settings
        self.screen_width = 12000
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

    
        self.ship_limit = 3
        

        #Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 10

        #How quickly the game speeds up
        self.speedup_scale = 1.1
        
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initalize_dynamic_settings()

    def initalize_dynamic_settings(self):
        '''Initalize settings that change throughout the game'''
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1.0

        #Scoring
        self.alien_points = 50

        #fleet direction of 1 represent rights; represents left
        self.fleet_direction = 1

    def increase_speed(self):
        '''Increase speed settings and alien points value'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)