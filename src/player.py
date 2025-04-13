import pygame
from src.sword import Sword
from src.bow import BowDrop, Projectile
import time  # Import the time module to check the time difference

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        self.pos = pygame.math.Vector2(x, y)
        self.rect.topleft = self.pos

        self.x_vel = 0
        self.y_vel = 0

        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False

        self.hotbar = [None] * 3  # Hotbar with 3 slots
        self.selected_slot = 0  # Currently selected slot
        self.holding_item = None  # The item currently being held by the player
        self.holding_key = False  # Tracks if the player is holding a key

        self.health = 100
        self.weapon_offset = (20, -10)  # Offset for weapon rendering

        self.facing_direction = 1  # Default facing right
        self.has_bow = False  # Track if the player has a bow

        # Cooldown management for sword attacks
        self.last_attack_time = 0  # Initialize last attack time to 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0

        if keys[pygame.K_LEFT]:
            self.x_vel = -self.speed
            self.facing_direction = -1  # Facing left
        if keys[pygame.K_RIGHT]:
            self.x_vel = self.speed
            self.facing_direction = 1  # Facing right
        if keys[pygame.K_UP] and self.on_ground:
            self.y_vel = self.jump_power

        if keys[pygame.K_1] and self.hotbar[0]:
            self.equip_weapon(self.hotbar[0], 0)
        elif keys[pygame.K_2] and self.hotbar[1]:
            self.equip_weapon(self.hotbar[1], 1)
        elif keys[pygame.K_3] and self.hotbar[2]:
            self.equip_weapon(self.hotbar[2], 2)

    def attack(self, enemies):
        keys = pygame.key.get_pressed()
        if not self.holding_item:
            return
        
        # Check if enough time has passed for sword attack (0.3 second cooldown)
        current_time = time.time()  # Get the current time in seconds
        if isinstance(self.holding_item, Sword) and keys[pygame.K_SPACE]:
            if current_time - self.last_attack_time >= 0.3:  # 0.3 second cooldown
                self.sword_attack(enemies)
                self.last_attack_time = current_time  # Update the last attack time
        elif self.has_bow and keys[pygame.K_SPACE]:  # Check if the player has a bow
            self.bow_attack()

    def sword_attack(self, enemies):
        attack_range = 50  # How far the sword can hit
        attack_rect = self.rect.copy()
        attack_rect.x += self.facing_direction * attack_range

        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect):
                enemy.take_damage(10)  # Deal damage to the enemy
                print(f"Enemy hit! Remaining health: {enemy.health}")

    def bow_attack(self):
        if self.has_bow:  # If the player has a bow
            # Create a projectile and shoot it
            target_x = self.pos.x + self.facing_direction * 100  # Adjust target for projectile
            target_y = self.pos.y
            speed = 10  # Adjust the speed of the projectile
            projectile = Projectile(self.pos.x, self.pos.y, target_x, target_y, speed)
            # You would want to add this projectile to a group or list to update it
            print("Bow attack fired!")

    def apply_gravity(self):
        self.y_vel += self.gravity
        if self.y_vel > 10:
            self.y_vel = 10

    def check_collision(self, platforms):
        self.on_ground = False
        self.pos.y += self.y_vel
        self.rect.topleft = self.pos

        for platform in platforms:
            if hasattr(platform, "rect") and self.rect.colliderect(platform.rect):
                if self.y_vel > 0:
                    self.rect.bottom = platform.rect.top
                    self.y_vel = 0
                    self.on_ground = True
                elif self.y_vel < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0
                self.pos.y = self.rect.y

        self.pos.x += self.x_vel
        self.rect.topleft = self.pos

        for platform in platforms:
            if hasattr(platform, "rect") and self.rect.colliderect(platform.rect):
                if self.x_vel > 0:
                    self.rect.right = platform.rect.left
                elif self.x_vel < 0:
                    self.rect.left = platform.rect.right
                self.pos.x = self.rect.x

    def update(self, keys, platforms, items, enemies):
        self.handle_input()
        self.apply_gravity()
        self.check_collision(platforms)

        for item in items:
            if hasattr(item, "rect") and self.rect.colliderect(item.rect):
                if item.__class__.__name__ in ["Sword", "Key", "BowDrop"] and not getattr(item, 'picked_up', False):
                    for i in range(3):
                        if self.hotbar[i] is None:
                            self.hotbar[i] = item
                            item.picked_up = True
                            self.equip_weapon(item, i)
                            if item.__class__.__name__ == "BowDrop":  # Handle Bow pickup
                                self.has_bow = True
                            if item.__class__.__name__ == "Key":
                                self.holding_key = True
                            break

        self.attack(enemies)

    def equip_weapon(self, weapon, slot):
        self.holding_item = weapon
        self.selected_slot = slot

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

        # No sword drawing, removed the code that was drawing the sword
        self.draw_hotbar(screen)

    def draw_hotbar(self, screen):
        font = pygame.font.SysFont(None, 30)
        for i, weapon in enumerate(self.hotbar):
            rect = pygame.Rect(10 + i * 60, 550, 50, 40)
            if weapon:
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                screen.blit(weapon.image, rect.topleft)
            else:
                pygame.draw.rect(screen, (200, 200, 200), rect, 2)
                text = font.render("Empty", True, (0, 0, 0))
                screen.blit(text, (rect.x + 5, rect.y + 5))
