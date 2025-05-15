import pygame
import sys
import math
WIDTH=800
HEIGHT=400
BOUNCINESS=0.3
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aula 10")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLUE  = (0, 100, 255)
GREEN = (0, 255, 0)




# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # Draw
    screen.fill(WHITE)

    pygame.display.flip()

pygame.quit()
sys.exit()
