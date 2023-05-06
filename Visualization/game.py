import pygame
import random

# Define the size of the window and the grid
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 10

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Define the font
font = pygame.font.SysFont(None, 30)

# Define the number of solutions and the number of lights per solution
NUM_SOLUTIONS = 10
NUM_LIGHTS = 5

# Generate the solutions
solutions = []
for i in range(NUM_SOLUTIONS):
    # Generate a list of positions for the lights
    positions = []
    for j in range(NUM_LIGHTS):
        x = random.randint(0, GRID_SIZE - 1) * (WINDOW_WIDTH // GRID_SIZE) + (WINDOW_WIDTH // GRID_SIZE // 2)
        y = random.randint(0, GRID_SIZE - 1) * (WINDOW_HEIGHT // GRID_SIZE) + (WINDOW_HEIGHT // GRID_SIZE // 2)
        positions.append((x, y))
    solutions.append(positions)

# Define the current solution index
solution_index = 0

# Set the running variable to True
running = True

# Start the main loop
count = 0
while running:
    # Handle events
    if count % 50 == 0:
        solution_index = (solution_index + 1) % NUM_SOLUTIONS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         # Decrease the solution index
        #         solution_index = max(solution_index - 1, 0)
        #     elif event.key == pygame.K_RIGHT:
        #         # Increase the solution index
        #         solution_index = min(solution_index + 1, NUM_SOLUTIONS - 1)
    
    # Fill the background
    screen.fill(BLACK)
    # Draw the grid
    for x in range(0, WINDOW_WIDTH, WINDOW_WIDTH // GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_HEIGHT), 1)
    for y in range(0, WINDOW_HEIGHT, WINDOW_HEIGHT // GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WINDOW_WIDTH, y), 1)
    
    # Draw the lights for the current solution
    for light in solutions[solution_index]:
        pygame.draw.circle(screen, YELLOW, light, 10)
    
    # Draw the solution index
    text = font.render(f"Solution {solution_index + 1}", True, BLUE)
    screen.blit(text, (10, 10))
    
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
