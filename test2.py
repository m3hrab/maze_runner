import pygame

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Movement speed
MOVE_SPEED = 0.1

def create_empty_maze(rows, cols):
    return [[0] * cols for _ in range(rows)]

def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_maze(screen, maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_character(screen, x, y, color):
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def save_maze(maze, filename):
    with open(filename, 'w') as f:
        for row in maze:
            f.write(''.join(map(str, row)) + '\n')

def load_maze(filename):
    with open(filename, 'r') as f:
        maze = [list(map(int, line.strip())) for line in f]
    return maze

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Generator")

    maze = create_empty_maze(ROWS, COLS)
    start_pos = (1, 1)
    destination_pos = (COLS - 2, ROWS - 2)
    player_pos = start_pos
    dx, dy = 0, 0

    running = True
    drawing = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                elif event.button == 3:  # Right mouse button
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        maze[row][col] = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        maze[row][col] = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_maze(maze, 'maze.txt')
                elif event.key == pygame.K_l:
                    maze = load_maze('maze.txt')
                elif event.key == pygame.K_UP:
                    dx, dy = 0, -MOVE_SPEED
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, MOVE_SPEED
                elif event.key == pygame.K_LEFT:
                    dx, dy = -MOVE_SPEED, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = MOVE_SPEED, 0

        # Move the character
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        # Ensure the new position does not intersect with walls
        new_x_cell = int(new_x)
        new_y_cell = int(new_y)
        if 0 <= new_x_cell < COLS and 0 <= new_y_cell < ROWS and maze[new_y_cell][new_x_cell] == 0:
            player_pos = (new_x, new_y)

        screen.fill(WHITE)
        draw_grid(screen)
        draw_maze(screen, maze)
        draw_character(screen, player_pos[0], player_pos[1], RED)
        draw_character(screen, start_pos[0], start_pos[1], GREEN)
        draw_character(screen, destination_pos[0], destination_pos[1], GREEN)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
