import pygame
from src.base import BaseEntity

class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60, 5)
        self.jump_power = -12

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
        if keys[pygame.K_SPACE]:
            self.jump()

    def update(self, platforms, keys):
        self.handle_input(keys)
        super().update(platforms)