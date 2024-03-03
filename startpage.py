import pygame
from settings import Button

class StartPage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Load the background image and get its rect.
        self.background_img = pygame.image.load('assets/Images/start_page.png')
        self.background_img_rect = self.background_img.get_rect()

        self.screen_rect = screen.get_rect()
        self.background_img_rect.center = self.screen_rect.center


        # Buttons
        self.start_button = Button(self.screen_rect.centerx - 55, self.screen_rect.centery + 58 , 110, 57)
        self.instructions_button = Button(self.screen_rect.centerx - 100, self.screen_rect.centery + 124 , 200, 57)
        self.settings_button = Button(self.screen_rect.right - 80, 45 , 40, 43)
    
    def handle_events(self, events):
        # handle keyboard and mouse events
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.start_button.rect.collidepoint(mouse_pos):  
                    return 'game_page'
                elif self.instructions_button.rect.collidepoint(mouse_pos):
                    return 'instructions_page'
                elif self.settings_button.rect.collidepoint(mouse_pos):
                    return 'settings_page'
    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_img, self.background_img_rect)
        