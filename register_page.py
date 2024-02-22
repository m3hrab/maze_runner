import pygame
import sqlite3
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Login and Sign Up")

# Font
font = pygame.font.Font(None, 32)

# Database initialization
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password TEXT)''')
conn.commit()

# Function to display text and get user input
def text_input(prompt, rect, active):
    user_text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return user_text
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY if not active else BLUE, rect, 2)
        text_surface = font.render(prompt + user_text, True, BLACK)
        screen.blit(text_surface, (rect.x + 5, rect.y + 5))
        
        # Draw cursor
        if active:
            pygame.draw.line(screen, BLACK, (rect.x + 5 + text_surface.get_width(), rect.y + 5), (rect.x + 5 + text_surface.get_width(), rect.y + 5 + text_surface.get_height()), 2)

        pygame.display.flip()

# Function for sign up
def sign_up():
    username_rect = pygame.Rect(200, 200, 400, 50)
    password_rect = pygame.Rect(200, 300, 400, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(WHITE)
        username = text_input("Enter username: ", username_rect, False)
        password = text_input("Enter password: ", password_rect, False)
        if username and password:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print("Signed up successfully!")
            return

# Function for login
def login():
    username_rect = pygame.Rect(200, 200, 400, 50)
    password_rect = pygame.Rect(200, 300, 400, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(WHITE)
        username = text_input("Enter username: ", username_rect, False)
        password = text_input("Enter password: ", password_rect, False)
        if username and password:
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if c.fetchone():
                print("Login successful!")
                return
            else:
                print("Incorrect username or password.")

# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(WHITE)
        # Display options
        sign_up_text = font.render("Press 'S' to Sign Up", True, BLACK)
        login_text = font.render("Press 'L' to Login", True, BLACK)
        screen.blit(sign_up_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        screen.blit(login_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        
        # Draw text boxes
        username_rect = pygame.Rect(200, 200, 400, 50)
        password_rect = pygame.Rect(200, 300, 400, 50)
        pygame.draw.rect(screen, GRAY, username_rect, 2)
        pygame.draw.rect(screen, GRAY, password_rect, 2)
        
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            sign_up()
        elif keys[pygame.K_l]:
            login()

if __name__ == '__main__':
    main()
