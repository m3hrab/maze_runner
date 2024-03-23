import pygame 
import math

class Player():

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        self.image = pygame.surface.Surface((self.settings.cell_size, self.settings.cell_size))
        self.image.fill(self.settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


        # Player movement flags
        self.moving = {'up': False, 'down': False, 'left': False, 'right': False}
        self.direction = None
        self.pos = {'x': float(self.rect.x), 'y': float(self.rect.y)}

    def update(self, map_data):
        
        for direction, moving in self.moving.items():
            if moving:
                new_pos = self.rect.copy()
                if direction == 'left':
                    new_pos[0] -= self.settings.player_speed
                    self.direction = 'left'
                elif direction == 'right':
                    new_pos[0] += self.settings.player_speed
                    self.direction = 'right'
                elif direction == 'up':
                    new_pos[1] -= self.settings.player_speed
                    self.direction = 'up'
                elif direction == 'down':
                    new_pos[1] += self.settings.player_speed
                    self.direction = 'down'

                if direction == 'down' or direction == 'right':
                    n = math.ceil(new_pos[0] / self.settings.cell_size)
                    m = math.ceil(new_pos[1] / self.settings.cell_size)
                
                elif direction == 'up' or direction == 'left':
                    n = math.floor(new_pos[0] / self.settings.cell_size)
                    m = math.floor(new_pos[1] / self.settings.cell_size)

                # check if the next position is on the wall
                if map_data[m][n] == 1 or map_data[m][n] == 2:
                    self.moving[direction] = False
                else:
                    # Update the player's position
                    self.rect.x = round(new_pos[0])
                    self.rect.y = round(new_pos[1])

    def draw(self):
        self.screen.blit(self.image, self.rect)
                