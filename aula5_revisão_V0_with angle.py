import pygame
import sys
import math
from pygame.math import Vector2 

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Acceleration Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 24)

# Line parameters
line_length = 100
angle = 0  # Initial angle in radians

# Main loop
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                line_length += 10  # Increase line length
            elif event.key == pygame.K_DOWN:
                line_length = max(10, line_length - 10)  # Decrease line length, minimum 10

    # Calculate elapsed time
    dt = clock.tick(60) / 100.0  # Convert milliseconds to seconds

    # Update the angle (optional: make it rotate)
    angle += (1 * dt)  # Rotate at 1 radian per second
    angle=angle % 360  # Keep angle within 0-360 degrees
    
    # Calculate the endpoint of the line using sin and cos
    angle_radians=math.radians(angle)   
    line_end_x = WIDTH // 2 + line_length * math.cos(angle_radians)
    line_end_y = HEIGHT // 2 + line_length * math.sin(angle_radians)

    # Draw the vertical rotating line
    pygame.draw.line(screen, BLUE, (WIDTH / 2, HEIGHT / 2), (line_end_x, line_end_y), 2)

    # Draw the circle at the end of the vertical line
    pygame.draw.circle(screen, BLUE, (int(line_end_x), int(line_end_y)), 10)
    pygame.draw.circle(screen, BLUE, (int(WIDTH / 2), int(HEIGHT / 2)), line_length,1)
    label_text_R = f"R={int(line_length)}"
    label_R = font.render(label_text_R, True, BLUE)
    screen.blit(label_R, (line_end_x + 10, (line_end_y + 10)))
    
    # Draw the horizontal line at y = HEIGHT / 2
    pygame.draw.line(screen, RED, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2), 2)

    # Draw the vertical line at y = HEIGHT / 2
    pygame.draw.line(screen, RED, (WIDTH / 2, HEIGHT), (WIDTH/2, 0), 2)

    # Draw the vertical line from the ball to the horizontal line (sine visualization)
    pygame.draw.line(screen, BLACK, (line_end_x, line_end_y), (line_end_x, HEIGHT / 2), 1)

    # Draw the horizontal line from the ball to the vertical centerline (cosine visualization)
    pygame.draw.line(screen, BLACK, (line_end_x, line_end_y), (WIDTH / 2, line_end_y), 1)


    sine_value = math.sin(angle)  # Calculate the sine of the angle
    label_text_sin = f"sin({int(angle)}°) = {sine_value:.2f}"  # Include sine value
    label_sin = font.render(label_text_sin, True, BLACK)
    screen.blit(label_sin, (line_end_x + 10, (line_end_y + HEIGHT / 2) / 2))

    # Display the label with "cos" and angle information
    cosine_value = math.cos(angle)  # Calculate the cosine of the angle
    label_text_cos = f"cos({int(angle)}°) = {cosine_value:.2f}"  # Include cosine value
    label_cos = font.render(label_text_cos, True, BLACK)
    screen.blit(label_cos, ((line_end_x + WIDTH / 2) / 2, line_end_y - 20))


    info = "Up/Down changes Radius"  #
    label_info = font.render(info, True, BLACK)
    screen.blit(label_info, ((10, 10)))


    # Update the display
    pygame.display.flip()
