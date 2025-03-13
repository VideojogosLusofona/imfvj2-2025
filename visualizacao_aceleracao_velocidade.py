import pygame
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set up the Pygame window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Acceleration/Velocity")

# Shared variables for time, velocity, and acceleration values
time_values = []
velocity_values = []
acceleration_values = []

# Function to display a matplotlib chart
def show_matplotlib_chart():
    fig, ax = plt.subplots()
    line_velocity, = ax.plot(time_values, velocity_values, label='Velocity')
    line_acceleration, = ax.plot(time_values, acceleration_values, 'r', label='Acceleration')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Magnitude')
    ax.set_title('Time vs Velocity and Acceleration')
    ax.legend()

    def update_chart(frame):
        line_velocity.set_xdata(time_values)
        line_velocity.set_ydata(velocity_values)
        line_acceleration.set_xdata(time_values)
        line_acceleration.set_ydata(acceleration_values)
        ax.relim()
        ax.autoscale_view()
        return line_velocity, line_acceleration

    ani = animation.FuncAnimation(fig, update_chart, interval=100)
    plt.show()

# Run the matplotlib chart in a separate thread
chart_thread = threading.Thread(target=show_matplotlib_chart)
chart_thread.start()

# Initial conditions
position = Vector2(10, screen.get_height() // 2)
velocity = Vector2(0, 0)
horizontal_acceleration = 0

clock = pygame.time.Clock()
start_time = time.time()
running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        horizontal_acceleration += 1 
    if keys[pygame.K_DOWN]:
        horizontal_acceleration -= 1
        if horizontal_acceleration <= 0:
            horizontal_acceleration = 0

    print(velocity.length(), horizontal_acceleration)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Calculate deltaTime
    dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    elapsed_time = time.time() - start_time

    # Update horizontal velocity and position
    velocity.x += horizontal_acceleration * dt
    position.x += velocity.x * dt

    # Update the plot data
    time_values.append(elapsed_time)
    velocity_values.append(velocity.length())
    acceleration_values.append(horizontal_acceleration)

    # Draw the car body (two rectangles)
    pygame.draw.rect(screen, (0, 0, 255), (int(position.x) - 40, int(position.y) - 20, 80, 40))  # Main body
    pygame.draw.rect(screen, (0, 0, 255), (int(position.x) - 20, int(position.y) - 40, 40, 20))  # Top part

    # Draw the wheels (two circles)
    pygame.draw.circle(screen, (0, 0, 0), (int(position.x) - 30, int(position.y) + 20), 10)  # Left wheel
    pygame.draw.circle(screen, (0, 0, 0), (int(position.x) + 30, int(position.y) + 20), 10)  # Right wheel
    # Reset the circle position if it goes off the screen
    if position.x > screen.get_width():
        position = Vector2(0, screen.get_height() // 2)

    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
