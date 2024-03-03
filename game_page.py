import pygame
import math

class GamePage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        self.bg = pygame.image.load('assets/Images/bg.png')
        # Game variables
        self.level = 1
        self.lives = 3

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
        self.time_left = 30


                    
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
    
    # check if the player has reached the destination
    def check_destination(self):
        if self.player.rect.x == self.destination_cell[0] * self.settings.cell_size and self.player.rect.y == self.destination_cell[1] * self.settings.cell_size:
            return True
        return False
    def show_level_completion_screen(self):
        pass

    def show_game_over_screen(self):
        pass
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 0
            
            if event.type == self.timer_event:
                self.time_left -= 1
                if self.time_left == 0:
                    return 'start_page'
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'start_page'
                

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
            self.next_level()
            self.level += 1
            self.initialize_position()
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
        timer_text = self.settings.timer_font.render(f"Time left: {self.time_left} Seconds", True, self.settings.WHITE)
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.center = (self.settings.screen_width // 2, 50)
        self.screen.blit(timer_text, timer_text_rect)

    def draw(self):
        self.update()

        self.screen.fill(self.settings.bg_color)
        self.draw_map()
        self.player.draw()
        self.draw_timer()


class Player():

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        self.image = pygame.surface.Surface((self.settings.cell_size, self.settings.cell_size))
        self.image.fill(self.settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


        # Player movement flags
        self.moving = {'up': False, 'down': False, 'left': False, 'right': False}
        self.direction = None
        self.pos = {'x': float(self.rect.x), 'y': float(self.rect.y)}

    def update(self, map_data):
        for direction, moving in self.moving.items():
            if moving:
                new_pos = self.rect.copy()
                if direction == 'left':
                    new_pos[0] -= self.settings.player_speed
                    self.direction = 'left'
                elif direction == 'right':
                    new_pos[0] += self.settings.player_speed
                    self.direction = 'right'
                elif direction == 'up':
                    new_pos[1] -= self.settings.player_speed
                    self.direction = 'up'
                elif direction == 'down':
                    new_pos[1] += self.settings.player_speed
                    self.direction = 'down'

                if direction == 'down' or direction == 'right':
                    n = math.ceil(new_pos[0] / self.settings.cell_size)
                    m = math.ceil(new_pos[1] / self.settings.cell_size)
                
                elif direction == 'up' or direction == 'left':
                    n = math.floor(new_pos[0] / self.settings.cell_size)
                    m = math.floor(new_pos[1] / self.settings.cell_size)

                # check if the next position is on the wall
                if map_data[m][n] == 1 or map_data[m][n] == 2:
                    self.moving[direction] = False
                else:
                    # Update the player's position
                    self.rect.x = round(new_pos[0])
                    self.rect.y = round(new_pos[1])

    def draw(self):
        self.screen.blit(self.image, self.rect)
                