import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill((139, 69, 19))  # Brown color for a wooden door
        self.rect = self.image.get_rect(topleft=(x, y))
        self.locked = True

    def update(self, player):
        if self.locked and player.holding_key and self.rect.colliderect(player.rect):
            self.locked = False
            print("Door unlocked!")

    def draw(self, screen, camera):
        if self.locked:
            screen.blit(self.image, camera.apply(self))
        else:
            # Show an open door or nothing at all when unlocked
            open_door = pygame.Surface((50, 80), pygame.SRCALPHA)
            pygame.draw.rect(open_door, (0, 255, 0, 150), open_door.get_rect())  # Transparent "open" marker
            screen.blit(open_door, camera.apply(self))
