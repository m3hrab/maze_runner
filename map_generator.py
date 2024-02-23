import pygame

# Constants
WIDTH, HEIGHT = 960, 540
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

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
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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

    running = True
    drawing = False
    drawing_wall = False
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
                elif event.button == 2:  # Middle mouse button
                    drawing_wall = True  # Add 2 to the cell, capped at 2
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                elif event.button == 3:
                    drawing_wall = False

            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        maze[row][col] = 1

                if drawing_wall:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        maze[row][col] = 2

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_maze(maze, 'maze.txt')
                elif event.key == pygame.K_l:
                    maze = load_maze('maze.txt')


        screen.fill(WHITE)
        draw_grid(screen)
        draw_maze(screen, maze)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()