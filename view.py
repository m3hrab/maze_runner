import pygame
import sqlite3

class DatabaseViewer:

    def __init__(self, screen):
        # Initialize the database viewer attributes
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()

    def query_database(self):
        # Execute a query to retrieve data from the database
        self.c.execute("SELECT * FROM users")
        data = self.c.fetchall()
        return data

    def draw(self):
        # Display the data retrieved from the database
        self.screen.fill((0, 0, 0))  # Clear the screen
        data = self.query_database()
        y_offset = 50
        for row in data:
            for i, value in enumerate(row):
                text_surface = self.font.render(str(value), True, (255, 255, 255))
                self.screen.blit(text_surface, (50 + i * 300, y_offset))
            y_offset += 30

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Database Viewer")
    clock = pygame.time.Clock()

    viewer = DatabaseViewer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        viewer.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
