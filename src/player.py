import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x_vel = 0
        self.y_vel = 0

        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False
        self.hotbar = [None] * 3
        self.selected_slot = 0
        self.holding_item = None

        # Fixed offset for the sword (relative to the player)
        self.weapon_offset = (20, -10)  # Adjust this offset to fit your sword's position

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0

        if keys[pygame.K_LEFT]:
            self.x_vel = -self.speed
        if keys[pygame.K_RIGHT]:
            self.x_vel = self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.y_vel = self.jump_power

        # Equip weapon if hotbar slot contains an item
        if keys[pygame.K_1] and self.hotbar[0]:
            self.equip_weapon(self.hotbar[0], 0)
        elif keys[pygame.K_2] and self.hotbar[1]:
            self.equip_weapon(self.hotbar[1], 1)
        elif keys[pygame.K_3] and self.hotbar[2]:
            self.equip_weapon(self.hotbar[2], 2)

        # Switching between slots if empty
        elif keys[pygame.K_1] and not self.hotbar[0]:
            self.equip_weapon(None, 0)
        elif keys[pygame.K_2] and not self.hotbar[1]:
            self.equip_weapon(None, 1)
        elif keys[pygame.K_3] and not self.hotbar[2]:
            self.equip_weapon(None, 2)

    def apply_gravity(self):
        self.y_vel += self.gravity
        if self.y_vel > 10:
            self.y_vel = 10

    def check_collision(self, platforms):
        self.on_ground = False
        self.rect.y += self.y_vel

        for platform in platforms:
            if hasattr(platform, "rect") and self.rect.colliderect(platform.rect):
                if self.y_vel > 0:
                    self.rect.bottom = platform.rect.top
                    self.y_vel = 0
                    self.on_ground = True
                elif self.y_vel < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0

        self.rect.x += self.x_vel
        for platform in platforms:
            if hasattr(platform, "rect") and self.rect.colliderect(platform.rect):
                if self.x_vel > 0:
                    self.rect.right = platform.rect.left
                elif self.x_vel < 0:
                    self.rect.left = platform.rect.right

    def update(self, keys, platforms, sword):
        self.handle_input()
        self.apply_gravity()
        self.check_collision(platforms)

        # Handle sword pickup
        if sword and not sword.picked_up and self.rect.colliderect(sword.rect):
            for i in range(3):
                if self.hotbar[i] is None:
                    self.hotbar[i] = sword
                    sword.picked_up = True
                    self.equip_weapon(sword, i)  # Equip immediately on pickup
                    break

    def equip_weapon(self, weapon, slot):
        self.holding_item = weapon
        self.selected_slot = slot

    def draw(self, screen, camera):
        # Draw the player
        screen.blit(self.image, camera.apply(self))

        # Draw held weapon if any (use the fixed offset for positioning)
        if self.holding_item:
            # Sword will be drawn at a fixed offset relative to the player
            sword_pos = self.rect.x, self.rect.y
            # Apply camera transformation to the sword position
            screen.blit(self.holding_item.image, camera.apply_pos(sword_pos))

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
