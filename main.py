import pygame
import sys
from settings import Settings 

# Import all the game pages
from startpage import StartPage
from settings_page import SettingsPage
from instruction_page import InstructionPage
from game_page import GamePage
from login_page import LoginPage
from sign_up_page import SignUpPage

def run_game():

    """Initialize game and create a screen object."""
    pygame.init()
    pygame.mixer.init()
    settings = Settings() # Create an instance of Settings class to use its attributes

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height)) # create screen window
    pygame.display.set_caption("Maze Runner")  # set the game caption

    # Make the game pages instance
    start_page = StartPage(screen, settings)
    settings_page = SettingsPage(screen, settings)
    instruction_page = InstructionPage(screen, settings)
    game_page = GamePage(screen, settings)
    login_page = LoginPage(screen, settings)
    signup_page = SignUpPage(screen, settings)


    # Set current page
    current_page = login_page

    settings.background_music.play(-1) # play the background music
    # main game loop
    while True:
        
        # Watch for keyboard and mouse events.
        
        events = pygame.event.get() # get all events from the event queue

        flag = current_page.handle_events(events) # handle events for the current page
        if flag == 'quit':
            sys.exit() # exit the game

        elif flag == 'start_page':
            current_page = start_page 
        elif flag == 'login_page':
            current_page = login_page 
        elif flag == 'sign_up_page':
            current_page = signup_page 
        elif flag == 'main_page':
            current_page = start_page 
        elif flag == 'settings_page':
            current_page = settings_page 
        elif flag == 'instructions_page':
            current_page = instruction_page 
        elif flag == 'game_page':
            game_page.time_left = settings.timer_duration # reset the timer
            current_page = game_page 

        # Redraw the screen during each pass through the loop.
        current_page.draw()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

        # set the frame rate
        pygame.time.Clock().tick(60)

run_game()