import pygame
import sys
from pygame.math import Vector2 
# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horizontal Acceleration Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball parameters
ball_radius = 20
ball_color = RED
ball_position = Vector2(10, HEIGHT // 2)  # Start at the center of the screen
ball_velocity = Vector2(0, 0)  # Initial velocity
horizontal_acceleration = 0.9  # Horizontal acceleration

# Main loop
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate elapsed time
    dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds

    # Update horizontal velocity and position
    ball_velocity.x += horizontal_acceleration * dt
    ball_position += ball_velocity * dt
    #ball_position.x += ball_velocity.x * dt + 0.5 * horizontal_acceleration * dt**2 
    
    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_position.x), int(ball_position.y)), ball_radius)

    # Update the display
    pygame.display.flip()