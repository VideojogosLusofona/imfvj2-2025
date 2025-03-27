import pygame
import sys
from pygame.math import Vector2
import random

# Constants
WIDTH, HEIGHT = 800, 600
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAVITY = 9.8


class Particle:
    global WIDTH, HEIGHT, RED, GRAVITY
    # Ball parameters
    radius = 5
    color = (0, 0, 0)

    position = Vector2(0, 0)
    velocity = Vector2(0, 0)

    def __init__(self, position):
        # Initialize variables
        self.radius = random.randrange(3, 10)
        self.position = position
        self.velocity = Vector2(random.uniform(-50, 50), random.uniform(-150, -20))
        self.color = (random.randrange(256), 0, 0)

    def run(self, screen, dt):
        # Run all necessary updates and display
        self.update(dt)
        self.display(screen)

    def update(self, dt):
        # Perform calculations
        self.velocity.y += GRAVITY * dt
        self.position += self.velocity * dt

    def display(self, screen):
        # Display on the screen
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)


# Initialize Pygame
pygame.init()
# Main loop
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Acceleration Simulation")

# Create 100 particles initialized at the same location
particles = []
for _ in range(1000):
    particles.append(Particle(Vector2(WIDTH // 2, HEIGHT // 2)))

while True:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate elapsed time
    dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds

    # Update and display all particles
    for particle in particles:
        particle.run(screen, dt)

    # Update the display
    pygame.display.flip()