import pygame

class Sword:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 10)  # Small rectangle representing the sword
        self.picked_up = False  # Flag to track if it's picked up

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Red sword
