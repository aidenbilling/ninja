import pygame

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = speed
        direction = pygame.math.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
        self.vel = self.direction * self.speed

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

    def draw(self, screen, camera):
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self))

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= 10
            return True
        return False

class BowDrop:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 10)
        self.collected = False

    def draw(self, screen, camera):
        if not self.collected:
            pygame.draw.rect(screen, (150, 75, 0), camera.apply(self))

    def check_pickup(self, player):
        if self.rect.colliderect(player.rect):
            self.collected = True
            player.has_bow = True
