import pygame 

class Settings():

    def __init__(self) -> None:
        self.screen_width = 960
        self.screen_height = 540

        self.cell_size = 20
        self.columns = self.screen_width // self.cell_size
        self.rows = self.screen_height // self.cell_size

        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.color1 = "#D4495C"
        self.color2 = "#4CAEC0"
        self.color3 = "#FFD662"
        self.color4 = "#2C2442"
        self.bg_color = "#2C2442"

        self.player_speed = 1

        # Timer Settings
        self.timer_duration = 60  # 60 seconds
        self.timer_font = pygame.font.Font("assets/fonts/Dynamo/Dynamo.ttf", 28)

        # Level Settings
        self.level_font = pygame.font.Font("assets/fonts/Dynamo/Dynamo.ttf", 28)

class Button():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect,2)