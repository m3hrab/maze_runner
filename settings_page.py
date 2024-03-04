import pygame
from settings import Button

class SettingsPage():
    """Main menu page for Maze Runner"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Load the background image and get its rect.
        self.background_img = pygame.image.load('assets/Images/settings_page.png')
        self.background_img_rect = self.background_img.get_rect()

        self.screen_rect = screen.get_rect()
        self.background_img_rect.center = self.screen_rect.center


        # Buttons
        self.back_button = Button(self.screen_rect.right - 106, 64 , 42, 43)

        # Timer settings
        self.timer_duration = self.settings.timer_duration / 100
        self.timer_scroll_bar = pygame.Rect(self.screen_rect.centerx - 170, self.screen_rect.centery - 70, 430, 5)
        self.timer_indicator_x = self.timer_scroll_bar.x + self.timer_scroll_bar.width * self.timer_duration
        self.timer_dragging = False

    
    def handle_events(self, events):
        # handle keyboard and mouse events
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.back_button.rect.collidepoint(mouse_pos):  
                    return 'main_page'
                
                if self.timer_scroll_bar.collidepoint(mouse_pos):
                    self.timer_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.timer_dragging = False


        if self.timer_dragging:
            mouse_pos_x, _ = pygame.mouse.get_pos()
            if mouse_pos_x < self.timer_scroll_bar.left + 10:
                self.timer_duration = 0.10
            elif mouse_pos_x > self.timer_scroll_bar.right:
                self.timer_duration = 1
            else:
                self.timer_duration = (mouse_pos_x - self.timer_scroll_bar.left) / self.timer_scroll_bar.width

            
        self.settings.timer_duration = self.timer_duration


    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_img, self.background_img_rect)
        
        # Draw the timer minutes
        # Draw the timer percentage
        if self.timer_duration <= 0.10:
            self.timer_text = self.settings.sub_title_font.render(f"{int(self.timer_duration * 100)} seconds", True, "red")
        else:
            self.timer_text = self.settings.sub_title_font.render(f"{int(self.timer_duration * 100)} seconds", True, "#4CAEC0")
        
        self.timer_text_rect = self.timer_text.get_rect()
        self.timer_text_rect.right = self.timer_scroll_bar.right + 200
        self.timer_text_rect.centery = self.timer_scroll_bar.centery
        self.screen.blit(self.timer_text, self.timer_text_rect)

        # Draw the timer bar
        pygame.draw.rect(self.screen, "#4CAEC0", self.timer_scroll_bar)
        self.timer_indicator_x = self.timer_scroll_bar.x + self.timer_scroll_bar.width * self.timer_duration
        pygame.draw.circle(self.screen, "#4CAEC0", (int(self.timer_indicator_x), int(self.timer_scroll_bar.centery)), 10)