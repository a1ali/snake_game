import sys, pygame, random, time

from settings import Settings
from button import Button
from scoreboard import Scoreboard

class Snake_game:
    '''Main  class to maintain game assets and behavior '''

    def __init__(self):
        '''Init game and create game resourses'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                        self.settings.screen_height))
        pygame.display.set_caption('Snake Game')

        self.screen_rect = self.screen.get_rect()

        self.button = Button(self, 'Play')
        self.sb = Scoreboard(self)

        self.rect_x = self.screen_rect.centerx
        self.rect_y = self.screen_rect.centery
        self.rect_width = 20
        self.rect_height = 20
        self.snake_speed = 20
        

        # apple settings
        self.apple_dim = 20
        '''
        self.apple_x = random.randrange(0, self.settings.screen_width - self.rect_width, self.rect_width)
        self.apple_y = random.randrange(0, self.settings.screen_height - self.rect_height, self.rect_width)
        '''
        self.apple_x = random.randrange(self.settings.game_start_x, self.settings.game_end_x - self.rect_width, self.rect_width)
        self.apple_y = random.randrange(self.settings.game_start_y, self.settings.game_end_y - self.rect_height, self.rect_width)
        
        self.last_key = pygame.K_w
        self.direction = None
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.grey = (100, 100, 100)

        self.clock = pygame.time.Clock()
        self.FPS = 20 #10

        #collision check
        self.collide = False

        self.snakelist = []
        self.snake_len = 1
        self.snake_lives = 3

        self.game_active = False
        #self.score = 0
        

    def run_game(self):
        '''Main game loop'''
        while True:
            self._intro_screen()

            while self.game_active:
                self._update_screen() # update graphics
                self._check_events() #check for inputs and increase snake positions
                self._update_snake_head() #update snake list and head positions, we store all positions deleting the first position to keep same with snake length    
                self._collision() # determine 


    def _check_events(self):
        ''' Determine when to change directions and not allow the snake to go over its own body
            do this by storing direction and not allowing to go left than right etc.'''
        # last_key is the key pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and self.direction != 'left':
                    self.last_key = event.key
                    self.direction = 'right'
                    #self.rect_x += 5
                
                elif event.key == pygame.K_a and self.direction != 'right':
                    self.last_key = event.key
                    self.direction = 'left'
                elif event.key == pygame.K_w and self.direction != 'down':
                    self.last_key = event.key
                    self.direction = 'up'
                elif event.key == pygame.K_s and self.direction != 'up':
                    self.last_key = event.key
                    self.direction = 'down'
                elif event.key == pygame.K_q:
                    sys.exit()

            
        # allow the snake to stay in the game board and allow continous movement by using self.last_key to store direction
        if self.last_key == pygame.K_d and (self.rect_x + self.rect_width) < self.settings.game_end_x: #self.screen_rect.right:
                
            self.rect_x += self.snake_speed

        elif self.last_key == pygame.K_a and (self.rect_x) > self.settings.game_start_x: #0:
            
            self.rect_x -= self.snake_speed

        elif self.last_key == pygame.K_w and (self.rect_y) > self.settings.game_start_y: #0:
            
            self.rect_y -= self.snake_speed

        elif self.last_key == pygame.K_s and (self.rect_y + self.rect_height) < self.settings.game_end_y: #self.settings.screen_height:
           
            self.rect_y += self.snake_speed


    def _draw_rect(self, color, x, y, width, height):
        pygame.draw.rect(self.screen, color, [x, y, width, height])

    def _draw_apple(self):
        
        self._draw_rect(self.red, self.apple_x, self.apple_y, self.apple_dim, self.apple_dim)

    def _collision(self):
        '''Determine collision of the snake and apple'''

        if self.rect_x == self.apple_x and self.rect_y == self.apple_y:

            self.apple_loc = [self.apple_x, self.apple_y]
            #have to make sure the apple is not placed within the snake position
            while True:
                if self.apple_loc in self.snakelist:

                    self.apple_x = random.randrange(self.settings.game_start_x, self.settings.game_end_x - self.rect_width, self.rect_width)
                    self.apple_y = random.randrange(self.settings.game_start_y, self.settings.game_end_y - self.rect_height, self.rect_width)

                    # set new postion of the apple location
                    self.apple_loc[0] = self.apple_x
                    self.apple_loc[1] = self.apple_y

                else:
                    break

            #self.collide = True
            self.snake_len += 1
            self.settings.score += 10
            self.sb.prep_score() 
        

    def _draw_grid(self):
       
        for i in range(self.settings.game_start_y, self.settings.game_end_y + 1, self.rect_height):
            pygame.draw.line(self.screen, self.grey, [self.settings.game_start_x, i], [self.settings.game_end_x, i], 1)
        
        for j in range(self.settings.game_start_x, self.settings.game_end_x + 1, self.rect_height):
            pygame.draw.line(self.screen, self.grey, [j, self.settings.game_start_y], [j, self.settings.game_end_y], 1)

    def _update_snake_head(self):
        self.snake_head = []
        self.snake_head.append(self.rect_x)
        self.snake_head.append(self.rect_y)

        if self.snake_head not in self.snakelist:
            self.snakelist.append(self.snake_head)
        else:
            self._game_rules()
  
    def snake(self, snakelist):
        '''Snake is gonna be contolled by a list of lists [[x1,y1], [x2, y2]] storing all positions of 
            the snake until the length of the snake_len'''
        
        if len(self.snakelist) > self.snake_len:
            del self.snakelist[0]
        
        for xy in snakelist:
            self._draw_rect(self.green, xy[0], xy[1], self.rect_height, self.rect_height)

    def _game_rules(self):
        '''reset the snake in the middle and reduce the amount of lives'''
        if self.snake_len > 1:
            #print('Cross Over')
            self.rect_x = self.screen_rect.centerx
            self.rect_y = self.screen_rect.centery
            self.snakelist.clear()
            self.snake_lives -= 1
            time.sleep(1)


            if self.snake_lives == 0:
                self.game_active = False  
                self.snakelist.clear()
                self.snake_len = 1 
                self.settings.score = 0
                self.sb.prep_score()
                self.snake_lives = 3

    def _update_screen(self):
        # update and draw graphic items and control FPS
        self.screen.fill((0, 0, 0))
        self.snake(self.snakelist)
        self._draw_apple()
        self._draw_grid()
        self.sb.show_score()  
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def _intro_screen(self):
        #self.screen.fill((0, 0, 0))
        self.button.draw_button()
        self.button._credit()
        self._start_click()
        pygame.display.flip()

    def _start_click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        ''' detemine when player clicks and enter game.'''
        if self.button.rect.collidepoint(mouse_pos):
            self.game_active = True

if __name__ == "__main__":
    game = Snake_game()
    game.run_game()