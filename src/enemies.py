import pygame
from src.base import BaseEntity

class Enemy(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60, 2)
        self.vel_x = self.speed  # Enemies move automatically

    def update(self, platforms):
        super().update(platforms)
        # Reverse direction when hitting a wall
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.vel_x *= -1

class Ninja(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 255, 0))  # Green ninja

    def follow_player(self, player):
        if self.rect.centerx < player.rect.centerx:
            self.vel_x = self.speed  # Move right if ninja is to the left of the player
        elif self.rect.centerx > player.rect.centerx:
            self.vel_x = -self.speed  # Move left if ninja is to the right of the player
        else:
            self.vel_x = 0  # Stop moving if aligned

    def update(self, platforms, player):
        self.follow_player(player)
        super().update(platforms)

    def draw(self, screen):
        screen.blit(self.image, self.rect)