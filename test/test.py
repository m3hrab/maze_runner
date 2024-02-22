import pygame 


class Player():

    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("../assets/Images/spaceship.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center

        self.gravity_flag = False

    def gravity(self):
        if self.gravity_flag:
            if self.rect.bottom < 540:
                self.rect.y += 1

    def jump(self):
        if self.rect.y > 0:
            self.rect.y -= 20

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()
                self.gravity_flag = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.gravity_flag = True

    def update(self):
        self.gravity()

    def draw(self):
        self.update()
        self.screen.blit(self.image, self.rect)


class Spikes():

    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("../assets/Images/new_spikes.png")
        self.image2 = pygame.image.load("../assets/Images/new_spikes.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400

        self.rect2 = self.image2.get_rect()
        self.rect2.x = 960
        self.rect2.y = 400

    def paralox(self):
        self.rect.x -= 5
        if self.rect.right <= 0:
            self.rect.x = 960

        self.rect2.x -= 5
        if self.rect2.right <= 0:
            self.rect2.x = 960

    def draw(self):
        self.paralox()
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.image2, self.rect2)


def run_game():
    pygame.init() # Initialize the pygame module
    screen = pygame.display.set_mode((960, 540)) # Set the screen size to (960, 540) pixels
    pygame.display.set_caption("Space Jumper") # Set the title of the game window to "Space Jumper"
    clock = pygame.time.Clock() # Create a clock object to control the frame rate of the game

    player = Player(screen)
    spikes = Spikes(screen)

    while True: # Run the game loop
        for event in pygame.event.get(): # Get the event from the event queue
            if event.type == pygame.QUIT: # Check if the event is quit
                pygame.quit() # Quit the game
                quit() # Quit the game

            player.handle_event(event)
        screen.fill((255, 255, 255)) # Fill the screen with white color
        player.draw()
        spikes.draw()
        pygame.display.flip() # Update the display
        clock.tick(60) # Set the frame rate of the game to 60

run_game() # Call the run_game function to run the game