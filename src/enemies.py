import pygame
from pygame.rect import Rect
from src.bow import Projectile, BowDrop

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = Rect(x, y, width, height)
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.5
        self.max_speed = 3
        self.health = 50
        self.drops = []

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def check_collisions(self, platforms):
        self.on_ground = False
        self.rect.y += self.vel_y
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        self.rect.x += self.vel_x
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right

    def update(self, platforms, player):
        self.apply_gravity()
        self.move()
        self.check_collisions(platforms)

class Ninja(Enemy):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, platforms, player):
        self.apply_gravity()
        self.follow_player(player, platforms)
        self.move()
        self.check_collisions(platforms)
        self.damage_player(player)

    def follow_player(self, player, platforms):
        line_clear = True
        test_rect = self.rect.copy()

        step = 1 if self.rect.centerx < player.rect.centerx else -1

        for x in range(self.rect.centerx, player.rect.centerx, step * 5):
            test_rect.centerx = x
            for platform in platforms:
                if platform.rect.clipline(self.rect.center, player.rect.center):
                    line_clear = False
                    break
            if not line_clear:
                break

        if line_clear:
            self.vel_x = self.speed * step
        else:
            self.vel_x = 0

    def damage_player(self, player):
        if self.rect.colliderect(player.rect) and player.alive:
            player.health -= 1

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

class Archer(Enemy):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shooting_range = 200
        self.shoot_delay = 2000
        self.last_shot_time = 0
        self.projectiles = []

    def update(self, platforms, player):
        self.apply_gravity()
        self.follow_player(player)
        self.move()
        self.check_collisions(platforms)

        if pygame.time.get_ticks() - self.last_shot_time >= self.shoot_delay:
            if self.can_see_player(player, platforms):
                self.shoot(player)

        for projectile in self.projectiles[:]:
            projectile.update(platforms)  # <-- Corrected this line!
            if projectile.check_collision(player):
                self.projectiles.remove(projectile)

        if self.health <= 0 and not self.drops:
            self.drops.append(BowDrop(self.rect.centerx, self.rect.bottom))

    def follow_player(self, player):
        if abs(self.rect.centerx - player.rect.centerx) > self.shooting_range:
            self.vel_x = self.speed if self.rect.centerx < player.rect.centerx else -self.speed
        else:
            self.vel_x = 0

    def shoot(self, player):
        projectile = Projectile(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery, 5)
        self.projectiles.append(projectile)
        self.last_shot_time = pygame.time.get_ticks()

    def can_see_player(self, player, platforms):
        line_clear = True
        test_rect = self.rect.copy()

        step = 5 if self.rect.centerx < player.rect.centerx else -5
        for x in range(self.rect.centerx, player.rect.centerx, step):
            test_rect.centerx = x
            for platform in platforms:
                if platform.rect.clipline(self.rect.center, player.rect.center):
                    line_clear = False
                    break
            if not line_clear:
                break
        return line_clear

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
        for drop in self.drops:
            drop.draw(screen, camera)
