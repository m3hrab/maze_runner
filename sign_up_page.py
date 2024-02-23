import pygame
import sqlite3
import os

class SignUpPage():

    def __init__(self, screen, settings):
        # Initialize the login page attributes
        self.screen = screen
        self.settings = settings

        self.username_active = False
        self.email_active = False
        self.password_active = False
        self.username = ''
        self.email = ''
        self.password = ''
        self.font = pygame.font.Font(None, 32)
        self.message_font = pygame.font.Font(None, 18)

        
        self.username_rect = pygame.Rect(245, 105, 470, 50)
        self.email_rect = pygame.Rect(245, 190, 470, 50)
        self.password_rect = pygame.Rect(245, 282, 470, 50)

        self.sign_up_button_rect = pygame.Rect(415, 390, 133, 50)
        self.login_button_rect = pygame.Rect(415, 480, 133, 50)

        self.background = pygame.image.load('assets/Images/sign_up_page.png')
        

        self.message = ''

        # Connect to or create SQLite database
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()

        # Create table if not exists
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                          (username TEXT, email TEXT, password TEXT)''')
        self.conn.commit()

    def reset(self):
        self.username = ''
        self.email = ''
        self.password = ''
        self.message = ''

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicks on the input box rect
                if self.username_rect.collidepoint(event.pos):
                    self.username_active = True
                    self.email_active = False
                    self.password_active = False
                else:
                    self.username_active = False

                if self.email_rect.collidepoint(event.pos):
                    self.email_active = True 
                    self.username_active = False 
                    self.password_active = False
                else:
                    self.email_active = False 

                if self.password_rect.collidepoint(event.pos):
                    self.password_active = True
                    self.username_active = False
                    self.email_active = False
                else:
                    self.password_active = False

                # Check if the user clicks on the login button or sign up button

                if self.login_button_rect.collidepoint(event.pos):
                    return 'login_page'

                elif self.sign_up_button_rect.collidepoint(event.pos):
                    if self.sign_up_user():
                        self.reset()
                        return 'login_page'
                    

            elif event.type == pygame.KEYDOWN:
                if self.username_active or self.password_active or self.email_active:
                    if event.key == pygame.K_RETURN:
                        return self.username, self.password
                    elif event.key == pygame.K_BACKSPACE:
                        if self.username_active:
                            self.username = self.username[:-1]
                        elif self.email_active:
                            self.email = self.email[:-1]
                        elif self.password_active:
                            self.password = self.password[:-1]
                    else:
                        if self.username_active:
                            self.username += event.unicode
                        elif self.email_active:
                            self.email += event.unicode 
                        elif self.password_active:
                            self.password += event.unicode


    def sign_up_user(self):
        if self.username == '' or self.email == '' or self.password == '':
            self.message = "Please fill in all fields to sign up"
            return False
        
        self.c.execute("SELECT * FROM users WHERE username=?", (self.username,))
        if self.c.fetchone():
            self.message = "Username already exists"
            return False
        else:
            self.c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (self.username, self.email, self.password))
            self.conn.commit()
            self.message = "Sign up Successful"
            return True


    def draw(self):
        self.screen.blit(self.background, (0, 0))

        text_surface = self.font.render(self.username, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.username_rect.x + 20, self.username_rect.y + 10))

        if self.username_active:
            pygame.draw.line(self.screen, (255, 255, 255), (self.username_rect.x + 20 + text_surface.get_width(), self.username_rect.y + 10), (self.username_rect.x + 20 + text_surface.get_width(), self.username_rect.y + 10 + text_surface.get_height()), 2)

        
        text_surface = self.font.render(self.email, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.email_rect.x + 20, self.email_rect.y + 10))

        if self.email_active:
            pygame.draw.line(self.screen, (255, 255, 255), (self.email_rect.x + 20 + text_surface.get_width(), self.email_rect.y + 10), (self.email_rect.x + 20 + text_surface.get_width(), self.email_rect.y + 10 + text_surface.get_height()), 2)

        text_surface = self.font.render((len(self.password)*"*"), True, (255, 255, 255))
        self.screen.blit(text_surface, (self.password_rect.x + 20, self.password_rect.y + 10))

        if self.password_active:
            pygame.draw.line(self.screen, (255, 255, 255), (self.password_rect.x + 20 + text_surface.get_width(), self.password_rect.y + 10), (self.password_rect.x + 20 + text_surface.get_width(), self.password_rect.y + 10 + text_surface.get_height()), 2)

        text_surface = self.font.render(self.message, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.password_rect.x + 30, self.password_rect.y + 70))