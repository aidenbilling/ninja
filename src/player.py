import pygame
from src.base import BaseEntity

class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60, 5)
        self.jump_power = -12
        self.hotbar = [None, None, None, None]  # Initialize a hotbar with 4 slots (None for empty)
        self.selected_item = 0  # The default selected item in hotbar is 0

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
        if keys[pygame.K_UP]:
            self.jump()

        # Switching between hotbar items (use 1-4 to select items)
        if keys[pygame.K_1]:
            self.selected_item = 0
        elif keys[pygame.K_2]:
            self.selected_item = 1
        elif keys[pygame.K_3]:
            self.selected_item = 2
        elif keys[pygame.K_4]:
            self.selected_item = 3

    def update(self, platforms, keys):
        self.handle_input(keys)
        super().update(platforms)

    def draw(self, screen, color):
        # Draw the player (basic rectangle for now)
        pygame.draw.rect(screen, color, self.rect)

        # Draw the hotbar at the bottom of the screen
        hotbar_y = screen.get_height()
        slot_width = 50
        for i, item in enumerate(self.hotbar):
            color = (200, 200, 200)  # Default color for empty slots
            if i == self.selected_item:
                pygame.draw.rect(screen, (255, 0, 0), (i * slot_width, hotbar_y, slot_width, 50))  # Highlight selected
            else:
                pygame.draw.rect(screen, color, (i * slot_width, hotbar_y, slot_width, 50))

            if item:  # If there's an item, draw a placeholder (or actual image later)
                pygame.draw.rect(screen, (0, 255, 0), (i * slot_width + 10, hotbar_y + 10, 30, 30))  # Example item
