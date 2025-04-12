# main.py
import pygame
from src.game import Game

# Initialize Pygamew
pygame.init()

# Create the game instance
game = Game()

# Run the game
game.run()

# Quit Pygame
pygame.quit()
