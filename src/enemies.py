# src/enemy.py

import pygame
from pygame.rect import Rect

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = Rect(x, y, width, height)
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.5
        self.max_speed = 3

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > 10:  # Terminal vel
            self.vel_y = 10

    def move(self):
        # Horizontal movement is constrained by vel
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def check_collisions(self, platforms):
        self.on_ground = False
        self.rect.y += self.vel_y  # Move vertically first

        for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.vel_y > 0:  # Falling down
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Jumping up
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0

        self.rect.x += self.vel_x  # Move horizontally
        for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.vel_x > 0:  # Moving right
                        self.rect.right = platform.rect.left
                    elif self.vel_x < 0:  # Moving left
                        self.rect.left = platform.rect.right



    def update(self, platforms, player):
        self.apply_gravity()
        self.move()
        self.check_collisions(platforms)

    def follow_player(self, player):
        pass

class Ninja(Enemy):  # Inherit from the Enemy class
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, platforms, player):
        self.apply_gravity()
        self.follow_player(player)
        self.move()
        self.check_collisions(platforms)

    def follow_player(self, player):
        if self.rect.centerx < player.rect.centerx:
            self.vel_x = self.speed  # Move right if ninja is to the left of the player
        elif self.rect.centerx > player.rect.centerx:
            self.vel_x = -self.speed  # Move left if ninja is to the right of the player
        else:
            self.vel_x = 0  # Stop moving if ninja is aligned with the player

    def draw(self, screen):
        screen.blit(self.image, self.rect)
