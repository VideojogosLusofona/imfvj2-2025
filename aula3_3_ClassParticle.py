import pygame
import sys
from pygame.math import Vector2 
import random

#constantes
WIDTH, HEIGHT = 800, 600
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAVITY = 9.8  


class Particle:
    global WIDTH, HEIGHT, RED, GRAVITY
    # Ball parameters
    radius = 20
    color = RED
    position = Vector2(0,0)  
    velocity = Vector2(0, 0)
  
   
    
    def __init__(self, position):
        #inicializa as variaveis
        self.position = position
        self.velocity = Vector2(0, random.uniform(-50, -20))
    def run(self, screen, dt):
        #Corre tudo o que tem de correr
        self.update(dt)
        self.display(screen)

    def update(self,dt):
        #Faz os calculos que tenha a fazer 
        self.velocity.y += GRAVITY * dt
        self.position += self.velocity * dt

    def display(self, screen):
        #Mostra no ecrã
        # Draw the ball
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
   


# Initialize Pygame
pygame.init()
 # Main loop
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Acceleration Simulation")


particle = Particle(pygame.Vector2(WIDTH//2, HEIGHT//2))

while True:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate elapsed time
    dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    particle.run(screen,dt)
   
    # Update the display
    pygame.display.flip()