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

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.alive = False  # Mark for removal on collision
                break

    def draw(self, screen, camera):
        if self.alive:
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self))

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= 10
            self.alive = False  # Destroy the projectile when hitting the player
            return True
        return False

class Bow:
    def __init__(self):
        self.image = pygame.Surface((20, 20))
        self.image.fill((139, 69, 19))  # Brown bow color
        self.projectile_speed = 10

    def shoot(self, player, projectiles_group):
        direction = player.facing  # Assuming 'facing' is "left" or "right"
        projectile = Projectile(player.rect.centerx, player.rect.centery, direction, self.projectile_speed)
        projectiles_group.add(projectile)


class BowDrop:
    def __init__(self, player):
        self.player = player
        # Check if there is an empty slot in the player's hotbar or inventory
        if self.add_bow_to_inventory():
            print("Bow added to inventory!")
        else:
            print("No empty slots in the inventory.")

    def add_bow_to_inventory(self):
        # Check for an empty slot and add the bow to the inventory
        for i in range(len(self.player.hotbar)):
            if self.player.hotbar[i] is None:  # Assuming None means empty slot
                self.player.hotbar[i] = "Bow"  # Add a bow to the hotbar
                return True
        return False


