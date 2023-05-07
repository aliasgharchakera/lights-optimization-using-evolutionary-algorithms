import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Define the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

LIT = (0,0,0)
UNLIT = (255,255,255)

def partially_lit_color(intensity):
    return (255-intensity*255,255-intensity*255,255-intensity*255)

# Define the dimensions of the room
ROOM_WIDTH = 600
ROOM_HEIGHT = 400
ROOM_DEPTH = 300

# Define the dimensions of the grid
GRID_WIDTH = 20
GRID_HEIGHT = 20

# Define the position of the camera
camera_x = 0
camera_y = 0
camera_z = -50
camera_angle_x = 0
camera_angle_y = 0

# Define the position of the lights
lights = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Define a function to draw the room
def draw_room():
    # Draw the floor
    pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH//2-ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2, ROOM_WIDTH, ROOM_HEIGHT))
    
    # Draw the ceiling
    pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH//2-ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2, ROOM_WIDTH, ROOM_HEIGHT//2))
    
    # Draw the walls
    pygame.draw.line(screen, BLACK, (WINDOW_WIDTH//2-ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2), (WINDOW_WIDTH//2-ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2+ROOM_DEPTH))
    pygame.draw.line(screen, BLACK, (WINDOW_WIDTH//2-ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2), (WINDOW_WIDTH//2+ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2))
    pygame.draw.line(screen, BLACK, (WINDOW_WIDTH//2+ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2), (WINDOW_WIDTH//2+ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2+ROOM_DEPTH))
    pygame.draw.line(screen, BLACK, (WINDOW_WIDTH//2-ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2+ROOM_DEPTH), (WINDOW_WIDTH//2+ROOM_WIDTH//2, WINDOW_HEIGHT//2-ROOM_HEIGHT//2+ROOM_DEPTH))
    
    # Draw the grid
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if lights[i][j]:
                pygame.draw.rect(screen, YELLOW, (WINDOW_WIDTH//2-ROOM_WIDTH//2+i*GRID_WIDTH, WINDOW_HEIGHT//2-ROOM_HEIGHT//2+j*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
            else:
                pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH//2-ROOM_WIDTH//2+i*GRID_WIDTH, WINDOW_HEIGHT//2-ROOM_HEIGHT//2+j*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
    
# Define a function to handle events
def handle_events():
    global camera_x, camera_y, camera_z, camera_angle_x, camera_angle_y, lights
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                camera_angle_x += 5
            elif event.key == K_DOWN:
                camera_angle_x -= 5
            elif event.key == K_LEFT:
                camera_angle_y += 5
            elif event.key == K_RIGHT:
                camera_angle_y -= 5
            elif event.key == K_w:
                camera_z += 5
            elif event.key == K_s:
                camera_z -= 5
            elif event.key == K_a:
                camera_x -= 5
            elif event.key == K_d:
                camera_x += 5
            elif event.key == K_SPACE:
                lights[0][0] = not lights[0][0]
# Start the game loop
while True:
    # Handle events
    handle_events()

    # Draw the scene
    draw_room()

    # Update the display
    pygame.display.flip()

    # Wait for a short amount of time to control the frame rate
    pygame.time.wait(10)

