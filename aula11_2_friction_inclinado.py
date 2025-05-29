import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Slope with Friction and Forces")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Ball parameters
ball_radius = 20
ball_x = ball_radius + 50
ball_y = ball_radius
ball_speed = 0

ball_mass = 20  # kg

# Friction and slope
slope_angle = 15  # degrees
friction_static = 0.1
friction_kinetic = 0.05

# Environment
gravity = 9.8
floor_y = 0

# Applied force
force_applied = 0
force_increment = 10

# Timing
t = 0.05
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
running = True

# Utility to draw vectors
def draw_vector(surface, color, origin, vector, label):
    tip = (origin[0] + vector[0], origin[1] + vector[1])
    pygame.draw.line(surface, color, origin, tip, 3)
    pygame.draw.circle(surface, color, tip, 5)
    label_text = font.render(label, True, color)
    surface.blit(label_text, (tip[0] + 5, tip[1] - 5))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                force_applied += force_increment
            elif event.key == pygame.K_DOWN:
                force_applied -= force_increment

    theta = math.radians(slope_angle)

    # Forces
    weight = ball_mass * gravity
    weight_parallel = weight * math.sin(theta)
    weight_perpendicular = weight * math.cos(theta)
    normal_force = weight_perpendicular
    static_friction = friction_static * normal_force
    kinetic_friction = friction_kinetic * normal_force

    net_force = (force_applied + weight_parallel) - static_friction

    if net_force > 0:
        # Ball moves, apply kinetic friction
        net_force = (force_applied + weight_parallel) - kinetic_friction
        acceleration = net_force / ball_mass
        delta_v = acceleration * t
        ball_speed += delta_v
    else:
        ball_speed = 0

    # Update position
    if ball_x < width - ball_radius:
        dx = ball_speed * t * math.cos(theta)
        dy = ball_speed * t * math.sin(theta)
        ball_x += dx
        ball_y += dy

    # Draw
    screen.fill(BLACK)

    # Slope
    slope_start = (0, floor_y)
    slope_end = (width - ball_radius, floor_y + (width - 2 * ball_radius) * math.tan(theta))
    pygame.draw.line(screen, BLUE, slope_start, slope_end, 3)

    # Ball
    pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), ball_radius)

    # Draw vectors from ball center
    origin = (int(ball_x), int(ball_y))
    scale = 0.5  # force to pixels

    # Force vectors
   
    draw_vector(screen, RED, origin, (0, weight * scale), f"Weight (mg): {weight:.1f}N")
    draw_vector(screen, GREEN, origin, (normal_force * scale * math.sin(theta), -normal_force * scale * math.cos(theta)), f"Normal): {normal_force:.1f}N")
    friction_dir = -1 if ball_speed > 0 else 0
    draw_vector(screen, YELLOW, origin, (friction_dir * kinetic_friction * scale * math.cos(theta), friction_dir * kinetic_friction * scale * math.sin(theta)), f"Friction: {kinetic_friction:.1f}N")
    draw_vector(screen, WHITE, origin, (net_force * scale * math.cos(theta), net_force * scale * math.sin(theta)), f"Net : {net_force:.1f}N")

    # Info text
    info_lines = [
        f"Up/Down to change Force | Applied: {force_applied:.1f}N",
        f"Slope Angle: {slope_angle}°",
        f"Weight Parallel: {weight_parallel:.1f}N = (weight * math.sin(theta))",
        f"Normal Force: {normal_force:.1f}N = (weight * math.cos(theta))",
        f"Static Friction: {static_friction:.1f}N",
        f"Kinetic Friction: {kinetic_friction:.1f}N",
        f"Net Force: {net_force:.1f}N = (force_applied + weight_parallel) - static_friction",
        f"",
        f"dx = ball_speed * t * math.cos(theta)",
        f"dy = ball_speed * t * math.sin(theta)",
    ]

    for i, line in enumerate(info_lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (10, 200 + i * 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
