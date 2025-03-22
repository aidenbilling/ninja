import pygame
from src.player import Player
from src.platform import Platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Man Prototype")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Create player and platforms
player = Player(WIDTH // 2, HEIGHT - 100)
platforms = [
    Platform(200, 400, 200, 20),
    Platform(400, 300, 200, 20),
    Platform(100, 500, 200, 20),
    Platform(0, HEIGHT - 20, WIDTH, 20)  # Floor
]

# Game loop
running = True
while running:
    clock.tick(FPS)  # Control frame rate
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(platforms)

    # Draw
    screen.fill(WHITE)
    for platform in platforms:
        platform.draw(screen)
    player.draw(screen)

    pygame.display.flip()  # Refresh screen

pygame.quit()
