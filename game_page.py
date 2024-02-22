import pygame
from settings import Button

class GamePage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Load the background image and get its rect.
        self.background_img = pygame.image.load('assets/Images/game.png')
        self.background_img_rect = self.background_img.get_rect()

        self.screen_rect = screen.get_rect()
        self.background_img_rect.center = self.screen_rect.center

        # Maze map
        self.maze = self.load_map('maze.txt')
        self.start_pos = (1, 1)
        self.destination_pos = (17, 22)
        self.move_speed = 0.1
        self.dx, self.dy = 0, 0
        self.player_pos = self.start_pos

        # Timer variables
        self.start_time = pygame.time.get_ticks()
        self.timer_font = pygame.font.Font(None, 36)

        self.is_game_over = False

    def handle_events(self, events):
        # handle keyboard and mouse events
        for event in events:
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_page'
            
                elif event.key == pygame.K_UP:
                    self.dx, self.dy = 0, -self.move_speed
                elif event.key == pygame.K_DOWN:
                    self.dx, self.dy = 0, self.move_speed
                elif event.key == pygame.K_LEFT:
                    self.dx, self.dy = -self.move_speed, 0
                elif event.key == pygame.K_RIGHT:
                    self.dx, self.dy = self.move_speed, 0

    def check_finish(self):
        if int(self.player_pos[0]) == self.destination_pos[0] and int(self.player_pos[1]) == self.destination_pos[1]:
            print('You win!')
            # Stop the timer
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            print(f"Time: {elapsed_time} seconds")
            self.is_game_over = True
            self.player_pos = self.start_pos

    def check_game_over(self):
        if self.is_game_over:
            print('Game over!')
            # Stop the timer
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            print(f"Time: {elapsed_time} seconds")

    def update_player_position(self):
        # Move the character
        new_x = self.player_pos[0] + self.dx
        new_y = self.player_pos[1] + self.dy
        # Ensure the new position does not intersect with walls
        new_x_cell = int(new_x)
        new_y_cell = int(new_y)
        
        if 0 <= new_x_cell < self.settings.columns and 0 <= new_y_cell < self.settings.rows and self.maze[new_y_cell][new_x_cell] == 0:
            self.player_pos = (new_x, new_y)

    def load_map(self, filename):
        with open(filename, 'r') as f:
            maze = [list(map(int, line.strip())) for line in f]
        return maze

    def draw_map(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, self.settings.BLACK, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                else:
                    pygame.draw.rect(self.screen, self.settings.WHITE, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))

    def draw_player(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x * self.settings.cell_size, y * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))

    def draw_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        timer_text = self.timer_font.render(f"Time: {elapsed_time:.2f}", True, self.settings.BLACK)
        self.screen.blit(timer_text, (self.screen.get_width() - 150, 100))

    def draw(self):

        # Draw the background image
        self.screen.blit(self.background_img, self.background_img_rect)
        self.update_player_position()
        self.draw_map()
        self.check_finish()
        self.draw_player(self.destination_pos[0], self.destination_pos[1], self.settings.RED)
        self.draw_player(int(self.player_pos[0]), int(self.player_pos[1]), self.settings.BLUE)
        self.draw_timer()
