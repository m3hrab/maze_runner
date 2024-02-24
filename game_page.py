import pygame

class GamePage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Game variables
        self.level = 1
        self.lives = 3

        # Timer variables
        self.start_time = pygame.time.get_ticks()
        self.timer_duration = 20  # 20 seconds timer
        self.is_game_over = False

        # Map variables
        self.map_data = self.load_map()
        self.start_cell = (0, 0)
        self.destination_cell = (0, 0)

        # Player variables
        self.player = pygame.Rect(0, 0, self.settings.cell_size, self.settings.cell_size)
        self.initialize_position()

        # Direction variables
        self.movement_flag = {'up': False, 'down': False, 'left': False, 'right': False}

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
                    self.start_cell = (x, y)
                    self.player.x = x * self.settings.cell_size
                    self.player.y = y * self.settings.cell_size
                elif self.map_data[y][x] == 4:
                    self.destination_cell = (x, y)

    def next_level(self):
        self.map_data = self.load_map()

    def show_level_completion_screen(self):
        pass

    def show_game_over_screen(self):
        pass

    def change_direction(self, x, y):    
        self.dx = x
        self.dy = y

    def next_position(self):
        self.player.x += self.dx
        self.player.y += self.dy

    def is_next_position_valid(self, flag):
        # Check if the next position is not a wall
        n = self.player.y // self.settings.cell_size
        m = self.player.x // self.settings.cell_size

        if flag == 'up':
            n -= 1
            if n < 0 or self.map_data[n][m] == 1 or self.map_data[n][m] == 2:
                print(f'Invalid position: {n, m}')
                print(f'Map data: {self.map_data[n][m]}')
                return False
        elif flag == 'down':
            n += 1
            if n >= self.settings.rows or self.map_data[n][m] == 1 or self.map_data[n][m] == 2:
                print(f'Invalid position: {n, m}')
                print(f'Map data: {self.map_data[n][m]}')
                return False
        elif flag == 'left':
            m -= 1
            if m < 0 or self.map_data[n][m] == 1 or self.map_data[n][m] == 2:
                print(f'Invalid position: {n, m}')
                print(f'Map data: {self.map_data[n][m]}')
                return False
        elif flag == 'right':
            m += 1
            if m >= self.settings.columns or self.map_data[n][m] == 1 or self.map_data[n][m] == 2:
                print(f'Invalid position: {n, m}')
                print(f'Map data: {self.map_data[n][m]}')
                return False
        
        # update the player position
        
        return True
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return 0
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'start_page'
                
                elif event.key == pygame.K_UP:
                    self.movement_flag['up'] = True
                    self.movement_flag['down'] = False
                    self.movement_flag['left'] = False
                    self.movement_flag['right'] = False
                elif event.key == pygame.K_DOWN:
                    self.movement_flag['up'] = False
                    self.movement_flag['down'] = True
                    self.movement_flag['left'] = False
                    self.movement_flag['right'] = False
                elif event.key == pygame.K_LEFT:
                    self.movement_flag['up'] = False
                    self.movement_flag['down'] = False
                    self.movement_flag['left'] = True
                    self.movement_flag['right'] = False
                elif event.key == pygame.K_RIGHT:
                    self.movement_flag['up'] = False
                    self.movement_flag['down'] = False
                    self.movement_flag['left'] = False
                    self.movement_flag['right'] = True

    
    def update(self):
        if self.movement_flag['up']:
            # Check if the next position is not a wall
            if self.is_next_position_valid('up'):
                # Update the player x positio
                self.player.y -= 1
        elif self.movement_flag['down']:
            if self.is_next_position_valid('down'):
                self.player.y += 1
        elif self.movement_flag['left']: 
            if self.is_next_position_valid('left'):
                self.player.x -= 1
        elif self.movement_flag['right']:
            if self.is_next_position_valid('right'):
                self.player.x += 1



    def draw_map(self):
        for y in range(self.settings.rows):
            for x in range(self.settings.columns):
                if self.map_data[y][x] == 1:
                    pygame.draw.rect(self.screen, self.settings.color1, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size), 2)
                elif self.map_data[y][x] == 2:
                    pygame.draw.rect(self.screen, self.settings.color2, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size), 2)
                elif self.map_data[y][x] == 4:
                    pygame.draw.rect(self.screen, self.settings.color3, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                elif self.map_data[y][x] == 5:
                    pygame.draw.rect(self.screen, self.settings.color4, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                elif self.map_data[y][x] == 0:
                    pygame.draw.rect(self.screen, "#ffffff", (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size), 2)
    def draw_player(self):
        pygame.draw.rect(self.screen, self.settings.GREEN, self.player)

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        self.draw_map()
        self.update()
        self.draw_player()

    
    