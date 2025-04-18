import pygame
from pygame.rect import Rect
from src.bow import Projectile
import random
from src.player import Player

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = Rect(x, y, width, height)
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.5
        self.max_speed = 3
        self.health = 30  # Sword does 10 damage -> 3 hits to kill

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

    def has_ground_ahead(self, platforms, direction, distance=5):
        """ Check if there is ground ahead in the given direction """
        check_rect = self.rect.copy()
        check_rect.x += direction * distance
        check_rect.y += 1  # Move it 1 pixel down to detect the platform below

        for platform in platforms:
            if check_rect.colliderect(platform.rect):
                return True
        return False


    def take_damage(self, amount, player=None):
        self.health -= amount
        if self.health <= 0:
            self.kill(player)

    def kill(self, player=None):
        # Default enemy drops nothing
        pass

class Ninja(Enemy):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_hit_time = -3000  # Makes sure it can hit right away
        self.hit_cooldown = 3000    # 3 seconds cooldown
        self.attack_damage = 15     # Deals 15 damage to player

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
            # Check ground before moving
            if self.has_ground_ahead(platforms, step):
                self.vel_x = self.speed * step
            else:
                self.vel_x = 0
        else:
            self.vel_x = 0


    def damage_player(self, player):
        current_time = pygame.time.get_ticks()
        if self.rect.colliderect(player.rect) and player.alive:
            if current_time - self.last_hit_time >= self.hit_cooldown:
                player.health -= self.attack_damage
                self.last_hit_time = current_time  # Reset cooldown

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
        self.follow_player(player, platforms)
        self.move()
        self.check_collisions(platforms)

        if pygame.time.get_ticks() - self.last_shot_time >= self.shoot_delay:
            if self.can_see_player(player, platforms):
                self.shoot(player)

        # Handle projectiles and collisions
        for projectile in self.projectiles[:]:
            projectile.update(platforms)
            if projectile.check_collision(player):
                self.projectiles.remove(projectile)

    def follow_player(self, player, platforms):
        distance = player.rect.centerx - self.rect.centerx
        step = 1 if distance > 0 else -1

        if abs(distance) > self.shooting_range:
            if self.has_ground_ahead(platforms, step):
                self.vel_x = self.speed * step
            else:
                self.vel_x = 0
        else:
            self.vel_x = 0


    def can_see_player(self, player, platforms):
        line_clear = True
        for platform in platforms:
            if platform.rect.clipline(self.rect.center, player.rect.center):
                line_clear = False
                break
        return line_clear

    def shoot(self, player):
        projectile = Projectile(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery, speed=7)
        self.projectiles.append(projectile)
        self.last_shot_time = pygame.time.get_ticks()

    def kill(self, player):

        if random.random() <= 0.25:  # 25% drop chance
            if player.try_add_bow():
                print("Bow drop successful!")
            else:
                print("Player inventory full. Bow not added.")








    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        for projectile in self.projectiles:
            projectile.draw(screen, camera)

