class Settings:
    '''A class to store all settinfs for alien invasion.'''
    
    def __init__(self):
        '''Init game settings.'''
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # game board
        self.game_start_x = 100
        self.game_end_x = self.screen_width - 100

        self.game_start_y = 100
        self.game_end_y = self.screen_height - 100

        self.score = 0