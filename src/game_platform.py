import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))  # Blue for floor visibility

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
