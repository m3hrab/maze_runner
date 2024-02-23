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

    def load_map(self):
        try:
            with open(f'level{self.level}.txt', 'r') as file:
                lines = file.readlines()
            map_data = []
            for line in lines:
                line_data = line.strip().split(',')
                map_data.append([int(item) for item in line_data])
            return map_data
        
        except FileNotFoundError:
            print("File not found")
            return None

    def next_level(self):
        pass

    def show_level_completion_screen(self):
        pass

    def show_game_over_screen(self):
        pass

    def update(self):
        pass 
        for event in events:
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_page'
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_UP:
                    self.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.change_direction(1, 0)

    def handle_events(self):
        pass

    def draw_map(self):
        for row in range(self.settings.rows):
            for col in range(self.settings.cols):
                tile = self.map[row][col]
                if tile == 1:
                    pygame.draw.rect(self.screen, self.settings.wall_color, (col*self.settings.tile_size, row*self.settings.tile_size, self.settings.tile_size, self.settings.tile_size))
                elif tile == 2:
                    pygame.draw.rect(self.screen, self.settings.coin_color, (col*self.settings.tile_size, row*self.settings.tile_size, self.settings.tile_size, self.settings.tile_size))
    def draw(self):
        pass
