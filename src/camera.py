import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.state = (0, 0)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        # Ensure entity has a 'rect' attribute
        return entity.rect.move(self.camera.topleft)

    def apply_area(self, area):
        # Similar logic for applying the camera to an area
        return area.move(self.camera.topleft)

    def update(self, target):
        # Update the camera position based on the target (usually the player)
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Keep the camera within the bounds of the map
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.map_width - self.width), x)
        y = max(-(self.map_height - self.height), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
