import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Import grid settings
gameSize = 500
padding = 50
displaySize = gameSize + padding * 2   # = 600, same as grid board

# Constants
WINDOW_WIDTH = displaySize             # match grid width
HEADER_HEIGHT = 150                    # keep header height
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, HEADER_HEIGHT))
pygame.display.set_caption("Nautical Minesweeper Header")
clock = pygame.time.Clock()

# Load images
planks_img = pygame.image.load("assets/planks.png").convert_alpha()
planks_img = pygame.transform.smoothscale(planks_img, (WINDOW_WIDTH, HEADER_HEIGHT))

wheel_img = pygame.image.load("assets/wheel.png").convert_alpha()
wheel_img = pygame.transform.smoothscale(wheel_img, (100, 100))

compass_img = pygame.image.load("assets/compass.png").convert_alpha()
compass_img = pygame.transform.smoothscale(compass_img, (100, 100))

buoy_img = pygame.image.load("assets/buoy.png").convert_alpha()
buoy_img = pygame.transform.smoothscale(buoy_img, (40, 80))  # adjust as needed

# Fonts
font_buoys = pygame.font.SysFont("arial", 36, bold=True)   # large for buoy count
font_timer = pygame.font.SysFont("arial", 24, bold=True)   # smaller for timer

# Example variables
buoys_left = 5
start_time = time.time()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw plank background
    screen.blit(planks_img, (0, 0))

    # Draw wheel in the center
    screen.blit(
        wheel_img,
        (WINDOW_WIDTH // 2 - wheel_img.get_width() // 2,
         HEADER_HEIGHT // 2 - wheel_img.get_height() // 2)
    )

    # Draw compass on the right
    compass_x = WINDOW_WIDTH - compass_img.get_width() - 30
    compass_y = HEADER_HEIGHT // 2 - compass_img.get_height() // 2
    screen.blit(compass_img, (compass_x, compass_y))

    # Draw timer directly under compass (smaller font, white)
    elapsed_time = int(time.time() - start_time)
    timer_text = font_timer.render(str(elapsed_time), True, WHITE)
    timer_x = compass_x + (compass_img.get_width() // 2 - timer_text.get_width() // 2)
    timer_y = compass_y + compass_img.get_height() - 5
    screen.blit(timer_text, (timer_x, timer_y))

    # Draw buoy + number on the left (white)
    buoy_x = 10
    buoy_y = HEADER_HEIGHT // 2 - buoy_img.get_height() // 2
    screen.blit(buoy_img, (buoy_x, buoy_y))

    buoys_text = font_buoys.render(str(buoys_left), True, WHITE)
    buoys_text_x = buoy_x + buoy_img.get_width() + 5
    buoys_text_y = HEADER_HEIGHT // 2 - buoys_text.get_height() // 2
    screen.blit(buoys_text, (buoys_text_x, buoys_text_y))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
