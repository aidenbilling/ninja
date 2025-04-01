# game.py
import pygame
from src.player import Player
from src.game_platform import Platform
from src.sword import Sword
from src.enemies import Ninja

class Game:
    def __init__(self):
        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        
        # Create the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ninja Man Prototype")

        # Clock for controlling FPS
        self.clock = pygame.time.Clock()

        # Create player, platforms, and sword
        self.player = Player(self.WIDTH // 2, self.HEIGHT - 100)
        self.platforms = [
            Platform(200, 400, 200, 20),
            Platform(400, 300, 200, 20),
            Platform(100, 500, 200, 20),
            Platform(0, self.HEIGHT - 20, self.WIDTH, 20)  # Floor
        ]
        self.sword = Sword(350, 350)  # Sword placed on the ground
        self.ninja = Ninja(100, 100, 50, 50, 2)

    def run(self):
        # Game loop
        running = True
        while running:
            self.clock.tick(self.FPS)  # Control frame rate

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update game objects
            self.update()

            # Draw everything to the screen
            self.draw()

            pygame.display.flip()  # Refresh screen

    def update(self):
        # Update the player and check interactions
        self.player.update(self.platforms, self.sword)

        self.ninja.update(self.platforms, self.player)  # Update ninja
        self.ninja.follow_player(self.player)

    def draw(self):
        # Fill the screen with the background color
        self.screen.fill(self.WHITE)

        # Draw the platforms
        for platform in self.platforms:
            platform.draw(self.screen)

        # Draw the sword if not picked up
        if not self.sword.picked_up:
            self.sword.draw(self.screen)

        # Draw the player
        self.player.draw(self.screen)

        self.ninja.draw(self.screen)