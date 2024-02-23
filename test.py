import pygame 
import math
from button import Button 
import sys
import time 


class GameScreen():
    def __init__(self, screen, settings, monkey) -> None:
        self.screen = screen
        self.settings = settings
        self.monkey = monkey

        self.level = 1
        self.map_data = self.load_map() 

        # Load the banana image
        self.banana = self.load_image('assets/Images/banana.png', 25, 25)

        # play and pause button 
        self.play_button = self.load_image('assets/Images/play.png', 40, 40)
        self.pause_button = self.load_image('assets/Images/pause.png', 40, 40)
        self.is_paused = False

        # Player lives
        self.heart_image = self.load_image('assets/Images/heart.png', 30, 30)
        self.lives = 3

        # Quit button
        self.btn = Button('Ukončiť hru', screen.get_width() - 120, screen.get_height() -44, 100, 40, 
                    (255, 0, 0), (200, 200, 200))
        
        # Score board 
        self.score = 0
        self.score_rect = self.create_score_rect()
        # Level scores
        self.level_scores = []

    def show_quit_screen(self):
        """Show the quit screen with the scores and the question."""
        # Draw the background
        self.screen.fill((0, 0, 0))

        # Draw the scores
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f'Skóre: {self.score}', True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 60))
        self.screen.blit(score_text, score_rect)

        # Draw the question
        question_font = pygame.font.Font(None, 36)
        question_text = question_font.render('Naozaj chcete ukončiť hru?', True, (255, 255, 0))
        question_rect = question_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 ))
        self.screen.blit(question_text, question_rect)

        # Create the Yes and No buttons
        yes_button = Button('ÁNO', self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 40, 80, 40, 
                    (255, 0, 0), (200, 200, 200))
        no_button = Button('NIE', self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 + 40, 80, 40, 
                    (0, 255, 0), (200, 200, 200))

        # Event loop for the quit screen
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.settings.sound_on:
                        self.settings.button_clicked_sound.play()
                    if yes_button.rect.collidepoint(pygame.mouse.get_pos()):
                        # If the Yes button is clicked, quit the game
                        pygame.quit()
                        sys.exit()
                    elif no_button.rect.collidepoint(pygame.mouse.get_pos()):
                        # If the No button is clicked, return to the game
                        running = False

            # Draw the buttons
            yes_button.draw(self.screen, self.settings.font)
            no_button.draw(self.screen, self.settings.font)

            # Update the screen
            pygame.display.flip()


    def show_level_complete_screen(self):
        """Show the level complete screen with the scores and the question."""
        # Draw the background
        self.screen.fill((0, 0, 0))

        # Draw the scores
        score_font = pygame.font.Font(None, 64)
        score_text = score_font.render('Gratulujem!', True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 200))
        self.screen.blit(score_text, score_rect)

        # Level message
        score_font = pygame.font.Font(None, 40)
        score_text = score_font.render(f'Prekonali ste úroveň {self.level}', True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 140))
        self.screen.blit(score_text, score_rect)


        # Draw the level score
        level_score_font = pygame.font.Font(None, 36)
        level_score_text = level_score_font.render(f'Dosiahnuté skóre v prvom levely: {self.score}', True, (255, 255, 0))
        level_score_rect = level_score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 90))
        self.screen.blit(level_score_text, level_score_rect)

        # Draw the total score
        total_score_font = pygame.font.Font(None, 36)
        total_score_text = total_score_font.render(f'Celkové skóre: {sum(self.level_scores)}', True, (255, 255, 0))
        total_score_rect = total_score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2- 60))
        self.screen.blit(total_score_text, total_score_rect)

        # Draw the question
        question_font = pygame.font.Font(None, 36)
        question_text = question_font.render('Chcete pokračovať na další level?', True, (255, 255, 0))
        question_rect = question_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(question_text, question_rect)

        # Create the Yes and No buttons
        yes_button = Button('ÁNO', self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 40, 80, 40, 
                    (0, 255, 0), (200, 200, 200))
        no_button = Button('NIE', self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 + 40, 80, 40, 
                    (255, 0, 0), (200, 200, 200))

        # Event loop for the level complete screen
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.settings.sound_on:
                        self.settings.button_clicked_sound.play()

                    if yes_button.rect.collidepoint(pygame.mouse.get_pos()):
                        # If the Yes button is clicked, load the next level
                        # self.level_scores.append(self.score)
                        self.level += 1
                        self.next_level()
                        running = False
                    elif no_button.rect.collidepoint(pygame.mouse.get_pos()):
                        # If the No button is clicked, return to the main screen
                        running = False
                        return 3

            # Draw the buttons
            yes_button.draw(self.screen, self.settings.font)
            no_button.draw(self.screen, self.settings.font)

            # Update the screen
            pygame.display.flip()


    def show_game_over_screen(self):
        """Show the game over screen."""
        # Draw the background
        self.screen.fill((0, 0, 0))

        # Draw the game over message
        game_over_font = pygame.font.Font(None, 64)
        game_over_text = game_over_font.render('Ľutujem', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 200))
        self.screen.blit(game_over_text, game_over_rect)

        # Draw the message
        message_font = pygame.font.Font(None, 36)
        message_text = message_font.render('Hra sa skoncčila, lebo ste stratili všetky životy', True, (255, 0, 0))
        message_rect = message_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 120))        
        self.screen.blit(message_text, message_rect)

        # Draw the scores
        if len(self.level_scores) != self.level:
            total_score = sum(self.level_scores) + self.score
        else:
            total_score = sum(self.level_scores)

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f'Celkové skóre: {total_score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 80 ))
        self.screen.blit(score_text, score_rect)


        # Draw the scores for each level
        for i in range(len(self.level_scores)):
            level_score_font = pygame.font.Font(None, 36)
            level_score_text = level_score_font.render(f'Level {i+1}: {self.level_scores[i]}', True, (255, 255, 255))
            level_score_rect = level_score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + i * 40))
            self.screen.blit(level_score_text, level_score_rect)


        if len(self.level_scores) != self.level:
            level_score_font = pygame.font.Font(None, 36)
            level_score_text = level_score_font.render(f'Level {self.level}: {self.score}', True, (255, 255, 255))
            level_score_rect = level_score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + self.level * 40))
            self.screen.blit(level_score_text, level_score_rect)            


        button_image = pygame.image.load('assets/Images/delete.png')
        button_image = pygame.transform.scale(button_image, (40, 40))
        button_rect = button_image.get_rect()

        button_rect.x = self.settings.screen_width // 2 - 20
        button_rect.y = self.settings.screen_height - 50
        self.screen.blit(button_image, button_rect)
        # Update the screen
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        self.settings.button_clicked_sound.play()
                        self.level = 1
                        self.score = 0
                        self.level_scores = []
                        self.map_data = self.load_map()
                        return 3


    def show_game_completion_screen(self):
        """Show the game completion screen with the final scores."""
        # Draw the background
        self.screen.fill((0, 0, 0))

        # Draw the congratulations message
        congrats_font = pygame.font.Font(None, 64)
        congrats_text = congrats_font.render('Gratulujem!', True, (255, 255, 0))
        congrats_rect = congrats_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 200))
        self.screen.blit(congrats_text, congrats_rect)

        # Draw the level completion message
        level_complete_font = pygame.font.Font(None, 36)
        level_complete_text = level_complete_font.render('úspešne ste prešli všetkými úrovňami', True, (0, 255, 0))
        level_complete_rect = level_complete_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 120))
        self.screen.blit(level_complete_text, level_complete_rect)

        # Draw the final scores
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f'Celkové skóre: {sum(self.level_scores)}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 60))
        self.screen.blit(score_text, score_rect)

        # Draw the scores for each level
        for i in range(len(self.level_scores)):
            level_score_font = pygame.font.Font(None, 36)
            level_score_text = level_score_font.render(f'Level {i+1}: {self.level_scores[i]}', True, (255, 255, 255))
            level_score_rect = level_score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + i * 40))
            self.screen.blit(level_score_text, level_score_rect)

        button_image = pygame.image.load('assets/Images/check.png')
        button_image = pygame.transform.scale(button_image, (40, 40))
        button_rect = button_image.get_rect()

        button_rect.x = self.settings.screen_width // 2 - 20
        button_rect.y = self.settings.screen_height - 50
        self.screen.blit(button_image, button_rect)
        # Update the screen
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        self.settings.button_clicked_sound.play()
                        self.level = 1
                        self.score = 0
                        self.level_scores = []
                        self.map_data = self.load_map()
                        return 3


    def next_level(self):
        self.map_data = self.load_map()

    def load_image(self, path, width, height):
        # Load the image and scale it to the given width and height
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height))


    def load_map(self):
        """Load the map from the file."""
        try:
            with open(f'level{self.level}.txt', 'r') as file:
                lines = file.readlines()
            map_data = []
            for line in lines:
                line_data = line.strip().split(',')
                map_data.append([int(item) for item in line_data])
            return map_data
        except FileNotFoundError:
            print("File not found")
            return None


    def create_score_rect(self):
        score_text = self.settings.font.render(f'Skóre: {self.score}', True, (255, 255, 0))
        score_rect = score_text.get_rect()
        score_rect.x = self.screen.get_width() - 90
        score_rect.y = 10
        return score_rect
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.settings.sound_on:
                self.settings.button_clicked_sound.play()
            #  play and pause button
            x, y = pygame.mouse.get_pos()
            if self.settings.screen_width // 2 - 25 <= x <= self.settings.screen_width // 2 + 25 and self.settings.screen_height - 60 <= y <= self.settings.screen_height - 10:
                self.is_paused = not self.is_paused 

            # Quit button
            if self.btn.rect.collidepoint(pygame.mouse.get_pos()):
                self.show_quit_screen()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 3
            
            directions = {'right': pygame.K_RIGHT, 'left': pygame.K_LEFT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
            for direction, key in directions.items():
                if event.key == key:
                    self.monkey.moving = {dir: dir == direction for dir in directions}
                    new_pos = self.monkey.rect.copy()

                    if direction == 'left':
                        n = math.ceil(new_pos.x / self.settings.tile_size)
                        m = round(new_pos.y / self.settings.tile_size)
                    elif direction == 'right':
                        n = math.floor(new_pos.x / self.settings.tile_size)
                        m = round(new_pos.y / self.settings.tile_size)
                    elif direction == 'up':
                        n = round(new_pos.x / self.settings.tile_size)
                        m = math.ceil(new_pos.y / self.settings.tile_size)
                    elif direction == 'down':
                        n = round(new_pos.x / self.settings.tile_size)
                        m = math.floor(new_pos.y / self.settings.tile_size)

                    if self.map_data[m][n] != 1:
                        # Set the monkey's position to the tile's position
                        self.monkey.rect.x = n * self.settings.tile_size
                        self.monkey.rect.y = m * self.settings.tile_size
                        self.monkey.pos = {'x': float(self.monkey.rect.x), 'y': float(self.monkey.rect.y)}

                    # Update the monkey's image based on the direction
                    self.monkey.image = self.monkey.images[direction][0]

        return None

    
    def update(self, leopard, leopard2=None):

        if self.is_paused:
            return None
        
        if leopard2 != None:
            if self.monkey.rect.colliderect(leopard2.rect):
                if self.settings.sound_on:
                    self.settings.lose_life.play()

                self.lives -= 1
                
                self.monkey.rect.x = -25
                self.monkey.rect.y = -25
                self.display(leopard, leopard2)
                pygame.display.flip()
                time.sleep(2)

                # Reset the monkey's position
                self.monkey.rect.x = self.settings.tile_size * 18
                self.monkey.rect.y = self.settings.tile_size * 7
                self.monkey.pos = {'x': float(self.monkey.rect.x), 'y': float(self.monkey.rect.y)}
                
                # Reset the leopard's position
                leopard.rect.x = self.settings.tile_size * 1
                leopard.rect.y = self.settings.tile_size * 3

                leopard2.rect.x = self.settings.tile_size * 25
                leopard2.rect.y = self.settings.tile_size * 13

        # For level 1
        if self.monkey.rect.colliderect(leopard.rect):
            if self.settings.sound_on:
                self.settings.lose_life.play()

            self.lives -= 1
            self.monkey.rect.x = -25
            self.monkey.rect.y = -25
            self.display(leopard)
            pygame.display.flip()
            time.sleep(2)

            # Reset the monkey's start position
            self.monkey.rect.x = self.settings.tile_size * 18
            self.monkey.rect.y = self.settings.tile_size * 7
            self.monkey.pos = {'x': float(self.monkey.rect.x), 'y': float(self.monkey.rect.y)}
            
            leopard.rect.x = self.settings.tile_size * 1
            leopard.rect.y = self.settings.tile_size * 3

        # Game over
        if self.lives == 0:
            self.show_game_over_screen()
            return 3
            
        # update monkeys position
        self.monkey.update(self.map_data)

        tile_x = int(self.monkey.rect.x / self.settings.tile_size)
        tile_y = int(self.monkey.rect.y / self.settings.tile_size)

        # Issue with the monkey's position
        if self.map_data[tile_y][tile_x] == 1:
            if self.map_data[tile_y+1][tile_x] != 1:
                tile_y += 1
            elif self.map_data[tile_y][tile_x+1] != 1:
                tile_x += 1

        # Check if the monkey is on the banana
        if self.map_data[tile_y][tile_x] == 2:
            if self.settings.sound_on:
                self.settings.banana_eaten_sound.play()
            self.map_data[tile_y][tile_x] = 0
            self.score += 10

        # check if there any bananas left
        if not any(2 in row for row in self.map_data):
            # if not, the game show level completion screen
            self.level_scores.append(self.score)

            # Reset the monkey's position
            self.monkey.rect.x = self.settings.tile_size * 18
            self.monkey.rect.y = self.settings.tile_size * 7
            self.monkey.pos = {'x': float(self.monkey.rect.x), 'y': float(self.monkey.rect.y)}


            # Reset the leopard's position
            leopard.rect.x = self.settings.tile_size * 1
            leopard.rect.y = self.settings.tile_size * 3

            if leopard2 != None:
                leopard2.rect.x = self.settings.tile_size * 25
                leopard2.rect.y = self.settings.tile_size * 13


            if self.settings.sound_on:
                self.settings.level_up_sound.play()

            if self.level == 3:
                self.show_game_completion_screen()
                # Reset the level to 1
                self.level = 1
                self.score = 0
                self.level_scores = []
                self.map_data = self.load_map()
                return 3
            
            else:
                flag = self.show_level_complete_screen()
                self.score = 0
                if flag == 3:
                    # Reset the level to 1
                    self.level = 1
                    self.score = 0
                    self.level_scores = []
                    self.map_data = self.load_map()
                    return 3
        
        print("%d, %d"%(tile_x, tile_y))
        leopard.update((tile_x, tile_y), self.map_data)
        # if level more than 1
        if leopard2 != None:
            if leopard.rect.colliderect(leopard2.rect):
                pass 
            else:
                leopard2.update((tile_x, tile_y), self.map_data)


            

    def draw(self, map_data):
        # Draw the map
        for y, row in enumerate(map_data): 
            for x, cell in enumerate(row):
                if cell == 0:
                    pygame.draw.rect(self.screen, (0,0,0), (x * self.settings.tile_size, y * self.settings.tile_size, self.settings.tile_size, self.settings.tile_size))
                elif cell == 1:
                    pygame.draw.rect(self.screen, (19, 157, 245), (x * self.settings.tile_size, y * self.settings.tile_size, self.settings.tile_size, self.settings.tile_size), 0, 3)
                elif cell == 2:
                    self.screen.blit(self.banana, (x * self.settings.tile_size, y * self.settings.tile_size))

    def display(self, leopard, leopard2=None):
        self.screen.fill((0,0,0))
        self.draw(self.map_data)
        self.monkey.display()

        leopard.draw(self.screen)

        if leopard2 != None:
            leopard2.draw(self.screen)

        # Pause button
        if self.is_paused:
            self.screen.blit(self.play_button, (self.settings.screen_width // 2 - 25, self.settings.screen_height - 45))
        else:
            self.screen.blit(self.pause_button, (self.settings.screen_width // 2 - 25, self.settings.screen_height - 45))

        # Lives
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (i * 30, self.settings.screen_height - 45))
        
        # Quit button
        self.btn.draw(self.screen, self.settings.font)

        # Score board
        score_text = self.settings.font.render(f'Skóre: {self.score}', True, (255, 255, 0)) 
        self.screen.blit(score_text, self.score_rect)