import pygame
import sys
import math
from pygame.math import Vector2 

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ToF/MaxHeight/Range/ Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 24)

# Line parameters
line_length = 100
angle = 0  # Initial angle in radians

ball_velocity = Vector2(0, 0)  # Initial velocity
ball_position = Vector2(0, 0)
GRAVITY = 9.8  # Vertical acceleration
PLAY_MODE = 0  # 0: configuration, 1: projectile
    # Update the angle (optional: make it rotate)
angle = 45
# Main loop
clock = pygame.time.Clock()
while True:
    screen.fill(WHITE)
    dt = min(clock.tick(60) / 1000.0, 0.1)  # Limit max dt for stability


    
    # Calculate the endpoint of the line using sin and cos
    line_end_x = WIDTH // 2 + line_length * math.cos(math.radians(angle))
    line_end_y = HEIGHT // 2 + line_length * -math.sin(math.radians(angle))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                line_length -= 10  # Increase line length
            elif event.key == pygame.K_RIGHT:
                line_length += 10
                line_length=max(10, line_length)  # Decrease line length, minimum 10
            elif event.key == pygame.K_UP:
                angle += 5
            elif event.key == pygame.K_DOWN:
                angle -= 5
            elif event.key == pygame.K_SPACE:
                PLAY_MODE = 1 - PLAY_MODE  # Toggle between configuration and projectile mode
                if PLAY_MODE == 1:
                    # Use angle directly (in radians)
                    ball_velocity = Vector2(math.cos(math.radians(angle)), -math.sin(math.radians(angle))) * line_length  
                    ball_position = Vector2(line_end_x, line_end_y)
                elif PLAY_MODE == 0:
                    ball_velocity = Vector2(0, 0)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()

    # Draw the vertical rotating line
    pygame.draw.line(screen, BLUE, (WIDTH / 2, HEIGHT / 2), (line_end_x, line_end_y), 2)
    pygame.draw.circle(screen, BLUE, (int(line_end_x), int(line_end_y)), 10)
    pygame.draw.circle(screen, BLUE, (int(WIDTH / 2), int(HEIGHT / 2)), line_length, 1)
    
    #draw axis 
    pygame.draw.line(screen, RED, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2), 2)
    pygame.draw.line(screen, RED, (WIDTH / 2, HEIGHT), (WIDTH / 2, 0), 2)
   # Draw horizontal scale (in meters)
    scale_length = 500  # Length of the scale in meters
    pixels_per_meter = 10  # 1 meter = 10 pixels
    scale_start_x = 0  # Starting x position of the scale
    scale_y =  line_end_y  # Y position of the scale
    for i in range(scale_length + 10):
        x_position = scale_start_x + i * pixels_per_meter # Calculate x position based on scale length and pixels per meter
        pygame.draw.line(screen, BLACK, (x_position+WIDTH/2, scale_y - 5), (x_position+WIDTH/2, scale_y + 5), 2)
        label_scale = font.render(f"{i}", True, BLACK)
       # screen.blit(label_scale, (x_position+WIDTH/2 - 5, scale_y + 10))
    pygame.draw.line(screen, BLACK, (scale_start_x+WIDTH/2, scale_y), (scale_start_x +WIDTH/2+ scale_length * pixels_per_meter, scale_y), 1)

    pygame.draw.line(screen, GREEN, (line_end_x, line_end_y), (line_end_x, HEIGHT / 2), 1)
    pygame.draw.line(screen, GREEN, (line_end_x, line_end_y), (WIDTH / 2, line_end_y), 1)    
    # Display labels
    label_text_angle = f"Angle: {int(angle)}°"
    label_angle = font.render(label_text_angle, True, BLACK)
    screen.blit(label_angle, (WIDTH // 2, HEIGHT // 2))
    
    label_text_R = f"R={int(line_length)}"
    label_R = font.render(label_text_R, True, BLUE)
    screen.blit(label_R, (line_end_x + 10, line_end_y + 10))
    
    info1 = "Up/Down changes Angle && Left/Right changes Radius"
    screen.blit(font.render(info1, True, BLACK), (10, 10))
    info2 = "Space to Shoot"
    screen.blit(font.render(info2, True, BLACK), (10, 40))
    
    if PLAY_MODE == 0:
        ball_position = Vector2(line_end_x, line_end_y)
    if PLAY_MODE == 1:
        ball_velocity.y += GRAVITY * dt  # Apply gravity
        ball_position += ball_velocity * dt  # Update position
        
        # Reset when out of bounds
        if ball_position.y > HEIGHT or ball_position.x < 0 or ball_position.x > WIDTH:
            PLAY_MODE = 0

    initial_velocity = line_length  # Assuming velocity is proportional to line length
    angle_radians = math.radians(angle)  

    # Calculate and display the MAX HEIGHT
    max_height = (initial_velocity**2 * math.sin(angle_radians)**2) / (2 * GRAVITY)
    label_max_height = font.render(f"Max Height: {max_height:.2f}m", True, BLACK)
    screen.blit(label_max_height, (10, 110))
   # Draw a horizontal line at MAX HEIGHT
    max_height_y = line_end_y - max_height 
    pygame.draw.line(screen, BLUE, (0, max_height_y), (WIDTH, max_height_y), 1)
    pygame.draw.line(screen, BLUE, (line_end_x, line_end_y), (line_end_x, max_height_y), 1)
    label_max_height_line = font.render("Max Height", True, BLUE)
    screen.blit(label_max_height_line, (WIDTH / 2 + 10, max_height_y - 20))

    # Calculate and display the time of flight (TOF) preview   
    time_of_flight = (2 * initial_velocity * math.sin(angle_radians)) / GRAVITY
    label_time_of_flight = font.render(f"Time of Flight: {time_of_flight:.2f}s", True, BLACK)
    screen.blit(label_time_of_flight, (10, 140))

    # Calculate and display the time to reach the floor (TOG) (ground at HEIGHT/2)
    time_to_floor = (initial_velocity * math.sin(angle_radians) + 
                     math.sqrt((initial_velocity * math.sin(angle_radians))**2 + 2 * GRAVITY * (HEIGHT / 2 - line_end_y))) / GRAVITY
    label_time_to_floor = font.render(f"Time to Floor: {time_to_floor:.2f}s", True, BLACK)
    screen.blit(label_time_to_floor, (10, 170))
  
    # Calculate and display the RANGE
    range_of_projectile = (initial_velocity**2 * math.sin(2 * angle_radians)) / GRAVITY
    label_range = font.render(f"Range: {range_of_projectile:.2f}m", True, BLACK)
    screen.blit(label_range, (10, 200))
    rx=line_end_x + range_of_projectile
    pygame.draw.line(screen, RED, (rx, line_end_y+10), (rx, line_end_y-10), 4)
    
    #----------------------------------------------------------------
            # Calculate the RANGE in GROUND at Height/2
    y0 = line_end_y  # Initial height
    yf = HEIGHT / 2  # Ground level
    initial_velocity_x = line_length * math.cos(math.radians(angle))
    initial_velocity_y = line_length * math.sin(math.radians(angle))

    if initial_velocity_y**2 + 2 * GRAVITY * (yf - y0) >= 0:  # Ensure the projectile can reach the line
            time_to_ground = (initial_velocity_y + 
                             math.sqrt(initial_velocity_y**2 + 2 * GRAVITY * (yf - y0))) / GRAVITY

            # Compute landing position at HEIGHT/2
            range_at_ground = initial_velocity_x * time_to_ground
          
            # Display the range in ground at HEIGHT/2
            label_range_ground = font.render(f"Range at floor: {range_at_ground:.2f}m", True, BLACK)
            screen.blit(label_range_ground, (10, 230))
            # Draw a horizontal line from line_end_x, line_end_y with length range_at_ground
            #if range_at_ground > 0:
    pygame.draw.line(screen, GREEN, (line_end_x + range_at_ground, HEIGHT/2-10), (line_end_x + range_at_ground, HEIGHT/2+10), 4)
   
    # Draw the trajectory line     
    #   
    # Calculate the trajectory points
    # time_step = 0.1  # Time step for trajectory calculation
    # trajectory_points = []        
    #   for t in range(0, int(time_of_flight / time_step) + 1):
    #       x = initial_velocity * math.cos(angle_radians) * t * time_step
    #       y = (initial_velocity * math.sin(angle_radians) * t * time_step) - (0.5 * GRAVITY * (t * time_step)**2)
    #    trajectory_points.append((x, y))
    #       
    #   # Draw the trajectory line  
    #  for i in range(len(trajectory_points) - 1):          
    #               pygame.draw.line(screen, BLACK, (WIDTH // 2 + trajectory_points[i][0], HEIGHT // 2 - trajectory_points[i][1]),
    #                                (WIDTH // 2 + trajectory_points[i + 1][0], HEIGHT // 2 - trajectory_points[i + 1][1]), 2)
    #       
    #       pygame.draw.circle(screen, BLACK, (int(WIDTH // 2 + trajectory_points[0][0]), int(HEIGHT // 2 - trajectory_points[0][1])), 5)
    #       pygame.draw.circle(screen, BLACK, (int(WIDTH // 2 + trajectory_points[-1][0]), int(HEIGHT // 2 - trajectory_points[-1][1])), 5)     
     
    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_position.x), int(ball_position.y)), 5)
    
    # Display velocity for debugging
    label_velocity = font.render(f"Velocity: {ball_velocity.x:.2f}, {ball_velocity.y:.2f}", True, BLACK)
    screen.blit(label_velocity, (10, 80))
    
    # Update the display
    pygame.display.flip()
