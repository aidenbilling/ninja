import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Representing sword with a simple rectangle
        self.image.fill((255, 0, 0))  # Red for visibility
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.picked_up = False

    def draw(self, screen, camera):
        # Ensure that the sword is treated as a sprite with a rect
        if not self.picked_up:
            # Apply the camera transformation (camera.apply() expects an object with a 'rect' attribute)
            screen.blit(self.image, camera.apply(self))  # Correctly using 'camera.apply(self)'
