import pygame
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import time


# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Set the size of the window
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.DOUBLEBUF|pygame.OPENGL)

# Set up OpenGL
glViewport(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WINDOW_SIZE[0] / WINDOW_SIZE[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)

# Define some colors
WHITE = (1, 1, 1)
GRAY = (0.5, 0.5, 0.5)
BLACK = (0, 0, 0)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)

# Define some constants
TILE_SIZE = 1
FLOOR_WIDTH = 10
FLOOR_HEIGHT = 10
WALL_HEIGHT = 5
ROOM_WIDTH = FLOOR_WIDTH * TILE_SIZE
ROOM_HEIGHT = WALL_HEIGHT * TILE_SIZE
ROOM_DEPTH = FLOOR_HEIGHT * TILE_SIZE
# colours 
lit_color = (1, 1, 1)
unlit_color = (0.2, 0.2, 0.2)
def partial_color(color, intensity):
    return (color[0] * intensity, color[1] * intensity, color[2] * intensity)
partial_lit = partial_color(lit_color, 0.5)
# # Define the nested list that represents the floor
# floor = [[(0.647, 0.165, 0.165) for j in range(FLOOR_HEIGHT)] for i in range(FLOOR_WIDTH)]
# floor[2][3] = (1, 1, 1)  # Set a tile to be lit
# floor[4][7] = (0.4, 0.4, 0.4)  # Set a tile to be less intensely lit
# floor[6][2] = (0.8, 0.8, 0.8)  # Set a tile to be partially lit
# floor[8][5] = (0.2, 0.2, 0.2)  # Set a tile to be unlit

# Define a function to draw a tile
def draw_tile(tile_x, tile_y, color):
    glBegin(GL_QUADS)
    glColor3f(*color)
    glVertex3f(tile_x, tile_y, 0)
    glVertex3f(tile_x + TILE_SIZE, tile_y, 0)
    glVertex3f(tile_x + TILE_SIZE, tile_y + TILE_SIZE, 0)
    glVertex3f(tile_x, tile_y + TILE_SIZE, 0)
    glEnd()

# Define a function to draw the floor
def draw_floor(floor):
    for i in range(FLOOR_WIDTH):
        for j in range(FLOOR_HEIGHT):
            tile_x = i * TILE_SIZE - ROOM_WIDTH/2
            tile_y = j * TILE_SIZE - ROOM_DEPTH/2
            if floor[i][j].give_status() == True:
                color = lit_color
            elif floor[i][j].intensity > 0:
                color = partial_color(lit_color, floor[i][j].intensity)
            elif sum(floor[i][j].fill_vessel) > 0:
                color = partial_lit
            else:
                color = unlit_color
            
            # color = floor[i][j]
            draw_tile(tile_x, tile_y, color)

# Main game loop
def main_game_loop(floor_list, lens_of_chromosomes):
    count_max = len(floor_list)
    count = 0
    while True:
        # Update the floor
        floor = floor_list[count]

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set up the camera
        glLoadIdentity()
        gluLookAt(0, -10, 5, 0, 0, 0, 0, 0, 1)

        # Draw the floor
        draw_floor(floor)

        # Update the display
        pygame.display.flip()

        time.sleep(0.5)

        # Limit the framerate to 60 FPS
        clock.tick(60)
        if count < count_max:
            count += 1
# main_game_loop()
