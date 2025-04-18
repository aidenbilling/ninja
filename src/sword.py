import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.picked_up = False

    def draw(self, screen, camera):
        if not self.picked_up:
            screen.blit(self.image, camera.apply(self))
