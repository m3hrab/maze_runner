import pygame
from settings import Button

class StartPage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Load the background image and get its rect.
        self.background_img = pygame.image.load('assets/Images/main.png')
        self.background_img_rect = self.background_img.get_rect()

        self.screen_rect = screen.get_rect()
        self.background_img_rect.center = self.screen_rect.center


        # Buttons
        self.start_button = Button(self.screen_rect.centerx - 55, self.screen_rect.centery + 62 , 110, 50)
        self.instructions_button = Button(self.screen_rect.centerx - 100, self.screen_rect.centery + 127 , 200, 50)
        self.settings_button = Button(self.screen_rect.right - 72, 40 , 40, 40)
    
    def handle_events(self, events):
        # handle keyboard and mouse events
        for event in events:
            if event.type == pygame.QUIT:
                return 0
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
        # self.start_button.draw(self.screen)
        # self.instructions_button.draw(self.screen)
        # self.settings_button.draw(self.screen)
        