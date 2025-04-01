# camera.py
import pygame

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)  # Camera bounds (initially the entire world)
        self.world_size = pygame.Rect(0, 0, world_width, world_height)  # Define your larger world size here
        self.scale = 1  # Scale for zoom, if you need it later (default 1 for no zoom)

    def apply(self, entity):
        """Move an entity's rect according to the camera position."""
        return entity.rect.move(self.camera.topleft)

    def apply_to_surface(self, surface):
        """Move a surface (or sprite) according to the camera position."""
        return surface.get_rect(topleft=self.camera.topleft)

    def update(self, target_rect):
        """Update the camera position to follow the target (player)."""
        x = -target_rect.centerx + int(self.camera.width / 2)
        y = -target_rect.centery + int(self.camera.height / 2)

        # Keep the camera within the world bounds
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_size.width - self.camera.width), x)
        y = max(-(self.world_size.height - self.camera.height), y)

        self.camera = pygame.Rect(x, y, self.camera.width, self.camera.height)
