import pygame
from scripts.settings import Button

class InstructionPage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Load the background image and get its rect.
        self.background_img = pygame.image.load('assets/Images/instruction_page.png')
        self.background_img_rect = self.background_img.get_rect()

        self.screen_rect = screen.get_rect()
        self.background_img_rect.center = self.screen_rect.center


        # Buttons
        self.back_button = Button(self.screen_rect.right - 95, 65 , 40, 42)
    
    def handle_events(self, events):
        # handle keyboard and mouse events
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.back_button.rect.collidepoint(mouse_pos): 
                    self.settings.button_click_sound.play() 
                    return 'main_page'
                
    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_img, self.background_img_rect)
        # self.back_button.draw(self.screen)    