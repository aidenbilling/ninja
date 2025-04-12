import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        # Returns the adjusted rect of the entity based on the camera's position
        return entity.rect.move(self.camera.topleft)

    def apply_pos(self, pos):
        # Return position adjusted for camera
        return pos[0] - self.camera.x, pos[1] - self.camera.y

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.map_width - self.width), x)
        y = max(-(self.map_height - self.height), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
