import pygame
import math

# Import the Player class 
from scripts.player import Player
from scripts.settings import Button

class GamePage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        
        # Game variables
        self.level = 1
        self.lives = self.settings.lives
        self.lives_img = pygame.image.load("assets/Images/heart.png") 
        self.lives_img = pygame.transform.scale(self.lives_img, (35, 35))

        # Player variables
        self.player = Player(self.screen, self.settings)

        # Map variables
        self.map_data = self.load_map()
        self.destination_cell = (0, 0)
        self.initialize_position()

        # Timer attributes
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT+1 # Custom event for the timer
        pygame.time.set_timer(self.timer_event, 1000) 
        self.timer_paused = False
        self.time_left = self.settings.timer_duration

        # buttons 
        self.next_level_button = Button(self.settings.screen_width // 2 + 5, self.settings.screen_height // 2 + 93, 170, 57)
        self.main_menu_button = Button(self.settings.screen_width // 2 - 180, self.settings.screen_height // 2 + 93, 170, 57)
        self.game_over_main_menu_button = Button(self.settings.screen_width // 2 - 90, self.settings.screen_height // 2 + 95, 170, 57)
        self.game_complete_main_menu_button = Button(self.settings.screen_width // 2 - 75, self.settings.screen_height // 2 + 115, 155, 55)

        # Level completion
        self.is_level_complete = False
        self.level_completion_img = pygame.image.load("assets/Images/level_complete.png")

        # Game ove
        self.is_game_over = False
        self.game_over_img = pygame.image.load("assets/Images/game_over.png")

        # Game completion
        self.total_levels = self.settings.total_levels
        self.is_game_complete = False
        self.game_complete_img = pygame.image.load("assets/Images/game_finish.png")

    def reset(self, flag):
        # Reset the game variables
        if flag == 'game_complete':
            self.time_left = self.settings.timer_duration
            self.level = 1
            self.lives = self.settings.lives
            self.is_game_over = False
            self.is_level_complete = False
            self.is_game_complete = False
            self.map_data = self.load_map()
            self.initialize_position()
            self.player.moving = {'right': False, 'left': False, 'up': False, 'down': False}
        
        elif flag == 'next_level':
            self.level += 1
            self.map_data = self.load_map() # load the next level
            self.initialize_position() # set the player start and destination position from the map
            self.is_level_complete = False
            self.time_left = self.settings.timer_duration
            self.player.moving = {'right': False, 'left': False, 'up': False, 'down': False}
    
        elif flag == 'game_over':
            self.time_left = self.settings.timer_duration
            self.level = 1
            self.lives = self.settings.lives
            self.is_game_over = False
            self.is_level_complete = False
            self.is_game_complete = False
            self.map_data = self.load_map()
            self.initialize_position()
            self.player.moving = {'right': False, 'left': False, 'up': False, 'down': False}

        elif flag == 'lose_life':
            self.time_left = self.settings.timer_duration
            self.map_data = self.load_map()
            self.initialize_position()
            self.player.moving = {'right': False, 'left': False, 'up': False, 'down': False}

    def load_map(self):
        try:
            with open(f'levels/level{self.level}.txt', 'r') as f:
                map_data = [list(map(int, line.strip())) for line in f]

            return map_data
        
        except FileNotFoundError:
            print("File not found")
            return None
 
    def initialize_position(self):
        # get the start and destination cell
        for y in range(self.settings.rows):
            for x in range(self.settings.columns):
                if self.map_data[y][x] == 5:
                    self.player.rect.x = x * self.settings.cell_size
                    self.player.rect.y = y * self.settings.cell_size
                elif self.map_data[y][x] == 4:
                    self.destination_cell = (x, y)

    def next_level(self):
        self.map_data = self.load_map()
    
    def check_destination(self):
        # check if the player has reached the destination
        if self.player.rect.x >= self.destination_cell[0] * self.settings.cell_size: # and self.player.rect.y == self.destination_cell[1] * self.settings.cell_size:
            return True
        return False
    
    def handle_events(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            
            
            if self.is_game_complete:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_complete_main_menu_button.rect.collidepoint(event.pos):
                        self.settings.button_click_sound.play()
                        self.reset('game_complete')
                        return 'start_page'
                    
            elif self.is_level_complete:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_level_button.rect.collidepoint(event.pos):
                        self.settings.button_click_sound.play()
                        self.reset('next_level')
                        # pygame.time.delay(500) # delay for 500ms

                    elif self.main_menu_button.rect.collidepoint(event.pos):
                        self.settings.button_click_sound.play()
                        self.reset('game_over')
                        return 'start_page'

            elif self.is_game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over_main_menu_button.rect.collidepoint(event.pos):
                        self.settings.button_click_sound.play()
                        self.reset('game_over')
                        return 'start_page'
        
                    
            else:
                if event.type == self.timer_event:
                    self.time_left -= 1
                    if self.time_left == 0:
                        self.lives -= 1
                        self.reset('lose_life')
                        if self.lives != 0:
                            self.settings.lose_live_sound.play()
                        pygame.time.delay(1000) # delay for 1s
                    
                if event.type == pygame.KEYDOWN:
                    
                    # Player movement flags 
                    directions = {'right': pygame.K_RIGHT, 'left': pygame.K_LEFT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}

                    for direction, key in directions.items():
                        if event.key == key:
                            self.player.moving = {dir: dir == direction for dir in directions}
                            new_pos = self.player.rect.copy()

                            if direction == 'left':
                                n = math.ceil(new_pos.x / self.settings.cell_size)
                                m = round(new_pos.y / self.settings.cell_size)
                            elif direction == 'right':
                                n = math.floor(new_pos.x / self.settings.cell_size)
                                m = round(new_pos.y / self.settings.cell_size)
                            elif direction == 'up':
                                n = round(new_pos.x / self.settings.cell_size)
                                m = math.ceil(new_pos.y / self.settings.cell_size)
                            elif direction == 'down':
                                n = round(new_pos.x / self.settings.cell_size)
                                m = math.floor(new_pos.y / self.settings.cell_size)

                            if self.map_data[m][n] != 1 or self.map_data[m][n] != 2:
                                # set the player position to the cell
                                self.player.rect.x = n * self.settings.cell_size
                                self.player.rect.y = m * self.settings.cell_size
                                self.player.pos = {'x': float(self.player.rect.x), 'y': float(self.player.rect.y)}
            
    def update(self):

        if self.check_destination():
            if self.level == self.total_levels:
                self.is_game_complete = True
                self.settings.win_sound.play()
            else:
                self.is_level_complete = True
                self.settings.level_up_sound.play()
        elif self.lives == 0:
            self.is_game_over = True
            self.settings.game_over_sound.play()
        else:
            # Update the player's position
            self.player.update(self.map_data)

    def draw_map(self):
        for y in range(self.settings.rows):
            for x in range(self.settings.columns):
                if self.map_data[y][x] == 1:
                    pygame.draw.rect(self.screen, self.settings.color1, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                elif self.map_data[y][x] == 2:
                    pygame.draw.rect(self.screen, self.settings.color2, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                elif self.map_data[y][x] == 4:
                    pygame.draw.rect(self.screen, self.settings.color3, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                elif self.map_data[y][x] == 5:
                    pygame.draw.rect(self.screen, self.settings.color4, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                # elif self.map_data[y][x] == 0:
                #     pygame.draw.rect(self.screen, "#ffffff", (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size), 1)

    def draw_timer(self):
        if self.time_left < 10:
            timer_text = self.settings.timer_font.render(f"Time left: 0{self.time_left} Seconds", True, self.settings.RED)
        else:
            timer_text = self.settings.timer_font.render(f"Time left: {self.time_left} Seconds", True, self.settings.WHITE)
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.center = (self.settings.screen_width // 2, 50)
        self.screen.blit(timer_text, timer_text_rect)

    def draw_level(self):
        level_text = self.settings.level_font.render(f"Level: {self.level}", True, self.settings.WHITE)
        level_text_rect = level_text.get_rect()
        level_text_rect.topleft = (50, 50)
        self.screen.blit(level_text, level_text_rect)

    def draw_lives(self):
        for i in range(self.lives):
            self.screen.blit(self.lives_img, (self.settings.screen_width - 50 - (i * 40), 50))

    def draw_level_completion_screen(self):
        self.screen.blit(self.level_completion_img, (0, 0))
        level_text = self.settings.sub_title_font.render(f"Level {self.level} Completed", True, self.settings.WHITE)
        level_text_rect = level_text.get_rect()
        level_text_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2)
        self.screen.blit(level_text, level_text_rect)

    def draw_game_over_screen(self):
        self.screen.blit(self.game_over_img, (0, 0))
        text = self.settings.sub_title_font.render(f"You've completed {self.level - 1}/{self.total_levels} levels", True, self.settings.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2)
        self.screen.blit(text, text_rect)

    def draw_game_complete_screen(self):
        self.screen.blit(self.game_complete_img, (0, 0))

    def draw_game_elements(self):
            self.update()
            self.screen.fill(self.settings.bg_color)
            self.draw_timer()
            self.draw_level()
            self.draw_lives()
            self.draw_map()
            self.player.draw()

    def draw(self):
        if self.is_game_complete:
            self.draw_game_complete_screen()
        elif self.is_level_complete:
            self.draw_level_completion_screen()
        elif self.is_game_over:
            self.draw_game_over_screen()
        else:
            self.draw_game_elements()



