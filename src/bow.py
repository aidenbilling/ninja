# bow.py
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
        self.alive = True  # Add a flag for deletion

    def update(self, platforms):
        if not self.alive:
            return

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        # Check for collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.alive = False  # Mark for removal on collision
                break

    def draw(self, screen, camera):
        if self.alive:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self))

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= 10  # Damage the player
            self.alive = False  # Destroy the projectile
            return True
        return False


class Bow(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # Placeholder size for the Bow
        self.image.fill((255, 0, 255))  # Placeholder color for the Bow
        self.rect = self.image.get_rect()
        self.rect.topleft = pos  # Set position using a tuple (x, y)
        self.projectile_speed = 10  # Speed of the projectile

    def shoot(self, player, projectiles_group):
        direction = player.facing_direction  # Get the direction player is facing
        # Determine target coordinates for the projectile
        target_x = player.rect.centerx + direction * 100  # Fire 100 units ahead in facing direction
        target_y = player.rect.centery
        # Create and add the projectile to the projectiles group
        projectile = Projectile(player.rect.centerx, player.rect.centery, target_x, target_y, self.projectile_speed)
        projectiles_group.add(projectile)
