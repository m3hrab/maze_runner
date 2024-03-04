import pygame 

class Settings():

    def __init__(self) -> None:
        pygame.mixer.init()
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

        self.player_speed = 3
        self.total_levels = 2
        self.lives = 3

        # Timer Settings
        self.timer_duration = 30  # seconds
        self.timer_font = pygame.font.Font("assets/fonts/Dynamo/Dynamo.ttf", 28)

        # Level Settings
        self.level_font = pygame.font.Font("assets/fonts/Dynamo/Dynamo.ttf", 28)

        # Fonts
        self.title_font = pygame.font.Font("assets/fonts/Dynamo/Dynamo.ttf", 48)
        self.sub_title_font = pygame.font.Font("assets/fonts/Dynamo/Dynamo.ttf", 32)


        # Sounds
        self.background_music = pygame.mixer.Sound("assets/sounds/game_music.mp3")
        self.lose_live_sound = pygame.mixer.Sound("assets/sounds/lose_life.mp3")
        self.level_up_sound = pygame.mixer.Sound("assets/sounds/level_up.mp3")
        self.button_click_sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.mp3")

        # volume
        self.volume = 0.5
        
class Button():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect,2)