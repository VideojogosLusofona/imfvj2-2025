import pygame
import math

pygame.init()

# Set up display
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Floor Force Visualization")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Ball parameters
ball_radius = 20
ball_x = ball_radius
ball_y = height // 2
ball_speed = 40

ball_mass = 20  # kg
floor_y = height // 2
force_applied = 0
force_increment = 10

gravity = 9.8

running = True
clock = pygame.time.Clock()

# Draw arrow helper
def draw_arrow(surface, color, start, end, width=2):
    pygame.draw.line(surface, color, start, end, width)
    rotation = math.atan2(start[1]-end[1], end[0]-start[0])
    arrow_length = 10
    angle = math.pi / 6
    pygame.draw.line(surface, color, end, (end[0]-arrow_length*math.cos(rotation-angle),
                                           end[1]+arrow_length*math.sin(rotation-angle)), width)
    pygame.draw.line(surface, color, end, (end[0]-arrow_length*math.cos(rotation+angle),
                                           end[1]+arrow_length*math.sin(rotation+angle)), width)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                force_applied += force_increment
            elif event.key == pygame.K_DOWN:
                force_applied -= force_increment

    t = 0.05
    normal_force = ball_mass * gravity
    coefficient_of_static_friction = 0.2
    static_friction = coefficient_of_static_friction * normal_force
    net_force = force_applied - static_friction

    if net_force > 0:
        coefficient_of_kinetic_friction = 0.05
        kinetic_friction = coefficient_of_kinetic_friction * normal_force
        net_force = force_applied - kinetic_friction
        acceleration = net_force / ball_mass
        velocity_x = acceleration * t
    else:
        velocity_x = 0

    if ball_x < width - ball_radius:
        ball_x += velocity_x

    if ball_y > floor_y - ball_radius:
        ball_y = floor_y - ball_radius

    screen.fill(BLACK)

    # Draw floor
    pygame.draw.line(screen, BLUE, (0, floor_y), (width, floor_y), 3)

    # Draw ball
    pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), ball_radius)

    # --- Draw forces as arrows ---
    origin = (int(ball_x), int(ball_y))  # center of ball

    # Weight (mg) downward – RED
    draw_arrow(screen, RED, origin, (origin[0], origin[1] + 50), 3)

    # Normal force upward – GREEN
    draw_arrow(screen, GREEN, origin, (origin[0], origin[1] - 50), 3)

    # Net force – horizontal – YELLOW
    arrow_length = net_force * 0.5  # scaling factor for visualization   
    pygame.draw.line(screen, YELLOW, origin, (origin[0] + int(arrow_length), origin[1]), 3)

    
    # Labels
    font_small = pygame.font.Font(None, 20)
    screen.blit(font_small.render(" Normal", True, GREEN), (origin[0]+25, origin[1]-50))
    screen.blit(font_small.render(" Gravity", True, RED), (origin[0]+25, origin[1]+40))
    screen.blit(font_small.render(" Net Force", True, YELLOW), (origin[0]+40, origin[1]-10))


    # Force values and explanation text
    font = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 22)

    lines = [
        f"Applied Force: {force_applied:.2f} N",

        f"Net_force = force_applied - static_friction = {force_applied:.2f} - {static_friction:.2f} = {net_force:.2f} N",
        f"Normal Force = mass * gravity = {ball_mass} * {gravity} = {normal_force:.2f} N",
        f"Static Friction = μs * N = 0.2 * {normal_force:.2f} = {static_friction:.2f} N"
    ]

    for i, line in enumerate(lines):
        text = font_small.render(line, True, (255, 255, 255))
        screen.blit(text, (20, 20 + i * 25))

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
