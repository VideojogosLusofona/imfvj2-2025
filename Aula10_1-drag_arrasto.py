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
#Define a class
class Ball:
    def __init__(self, pos, vel, mass, radius, color):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.mass = mass
        self.radius = radius
        self.color = color
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), 
                           self.radius)
    def move(self, dt):
        self.pos += self.vel * dt
  # Check if ball hits the wall
        if self.pos.x >= WIDTH - self.radius:
           self.pos.x = WIDTH - self.radius
           self.vel.x = -BOUNCINESS*self.vel.x  # Reverse velocity direction with reduced magnitude
        air_density = 1.225  # kg/m^3 (density of air at sea level)
        drag_coefficient = 0.47  # Drag coefficient for a sphere
        cross_sectional_area = math.pi * (self.radius/100) ** 2  # A=pi*r^2
        drag_force_magnitude = 0.5 * air_density * self.vel.magnitude() ** 2 * drag_coefficient * cross_sectional_area 
        if self.vel.magnitude() != 0:  # Avoid division by zero during normalization
            drag_force = -drag_force_magnitude * self.vel.normalize()
        else:
            drag_force = pygame.Vector2(0, 0)
        self.vel += drag_force * dt

def check_collision(a: Ball, b: Ball):
    distance = a.pos.distance_to(b.pos)
    return distance < a.radius + b.radius
 
def resolve_collision(a: Ball, b: Ball, restitution=0.8):    
    normal = b.pos - a.pos
    if normal.length() == 0:
        return # overlapping
    normal = normal.normalize()
    rel_vel = b.vel - a.vel
    vel_along_normal = rel_vel.dot(normal)
    if vel_along_normal > 0:
        return # Balls are moving apart
    impulse_mag = -(1 + restitution) * vel_along_normal
    impulse_mag /= (1 / a.mass + 1 / b.mass)
    impulse = impulse_mag * normal
    a.vel -= impulse / a.mass
    b.vel += impulse / b.mass
   
#Instantiate a ball object
Ball1=Ball((100, 200), vel=(150, 0), mass=1, radius=20, color=RED)
Ball2=Ball((700, 200), vel=(-150, 0), mass=1, radius=20, color=BLUE)
# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # Draw
    screen.fill(WHITE)
    Ball1.draw(screen)
    Ball2.draw(screen)
    Ball1.move(dt)
    Ball2.move(dt)
    # Check for collision   
    if check_collision(Ball1, Ball2):
        resolve_collision(Ball1, Ball2, restitution=0.8)      
    pygame.display.flip()

pygame.quit()
sys.exit()
