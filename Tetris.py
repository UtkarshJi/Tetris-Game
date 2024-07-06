import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetris shapes (Tetrominoes)
tetrominoes = [
    [[1, 1, 1, 1]],    # I
    [[1, 1, 1], [0, 1, 0]],    # T
    [[1, 1, 1], [1, 0, 0]],    # L
    [[1, 1, 1], [0, 0, 1]],    # J
    [[1, 1], [1, 1]],    # O
    [[1, 1, 0], [0, 1, 1]],    # Z
    [[0, 1, 1], [1, 1, 0]]     # S
]

# Initialize game variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
current_piece = None
piece_x, piece_y = 0, 0
score = 0
last_move_time = 0

# Functions
def new_piece():
    global current_piece, piece_x, piece_y
    current_piece = random.choice(tetrominoes)
    piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
    piece_y = 0

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_piece():
    for y in range(len(current_piece)):
        for x in range(len(current_piece[y])):
            if current_piece[y][x] != 0:
                pygame.draw.rect(screen, WHITE, ((piece_x + x) * GRID_SIZE, (piece_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def check_collision():
    for y in range(len(current_piece)):
        for x in range(len(current_piece[y])):
            if current_piece[y][x] != 0:
                if piece_y + y >= GRID_HEIGHT or piece_x + x < 0 or piece_x + x >= GRID_WIDTH or grid[piece_y + y][piece_x + x] != 0:
                    return True
    return False

def merge_piece():
    global grid, current_piece, score, piece_x, piece_y
    
    # Merge the current piece into the grid
    for y in range(len(current_piece)):
        for x in range(len(current_piece[y])):
            if current_piece[y][x] != 0:
                grid[piece_y + y][piece_x + x] = 1
    
    # Check for completed lines and clear them
    clear_lines = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0] * GRID_WIDTH)
            clear_lines += 1
    
    # Update the score based on cleared lines
    score += clear_lines * 100

# Main game loop
new_piece()
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and piece_x > 0:
                piece_x -= 1
                if check_collision():
                    piece_x += 1
            elif event.key == pygame.K_RIGHT and piece_x < GRID_WIDTH - len(current_piece[0]):
                piece_x += 1
                if check_collision():
                    piece_x -= 1
            elif event.key == pygame.K_DOWN:
                piece_y += 1
                if check_collision():
                    piece_y -= 1
            elif event.key == pygame.K_UP:
                rotated_piece = [[current_piece[y][x] for y in range(len(current_piece))] for x in range(len(current_piece[0])-1, -1, -1)]
                old_piece = current_piece
                current_piece = rotated_piece
                if check_collision():
                    current_piece = old_piece
    
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > 500:  # Move piece down every 500ms
        last_move_time = current_time
        piece_y += 1
        if check_collision():
            piece_y -= 1
            merge_piece()
            new_piece()
            if check_collision():
                running = False
    
    draw_grid()
    draw_piece()
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(60)  # Adjust speed by changing tick value

pygame.quit()
print(f"Game over! Score: {score}")
