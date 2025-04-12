import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Placeholder for player sprite
        self.image.fill((0, 255, 0))  # Make it green for visibility
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x_vel = 0
        self.y_vel = 0

        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False
        self.hotbar = [None] * 3  # Hotbar with 3 slots (expandable)
        self.selected_slot = 0  # Index of selected hotbar slot
        self.holding_item = None  # Currently held item

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0  # Reset horizontal movement

        if keys[pygame.K_LEFT]:
            self.x_vel = -self.speed
        if keys[pygame.K_RIGHT]:
            self.x_vel = self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.y_vel = self.jump_power  # Jump if on the ground

        # Equip item from hotbar
        if keys[pygame.K_1] and self.hotbar[0]:
            self.equip_weapon(self.hotbar[0], 0)
        elif keys[pygame.K_2] and self.hotbar[1]:
            self.equip_weapon(self.hotbar[1], 1)
        elif keys[pygame.K_3] and self.hotbar[2]:
            self.equip_weapon(self.hotbar[2], 2)

    def apply_gravity(self):
        self.y_vel += self.gravity
        if self.y_vel > 10:  # Terminal velocity
            self.y_vel = 10

    def check_collision(self, platforms):
        self.on_ground = False
        self.rect.y += self.y_vel  # Move vertically first

        for platform in platforms:
            if hasattr(platform, "rect") and self.rect.colliderect(platform.rect):
                if self.y_vel > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.y_vel = 0
                    self.on_ground = True
                elif self.y_vel < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0

        self.rect.x += self.x_vel  # Move horizontally
        for platform in platforms:
            if hasattr(platform, "rect") and self.rect.colliderect(platform.rect):
                if self.x_vel > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.x_vel < 0:  # Moving left
                    self.rect.left = platform.rect.right

    def update(self, keys, platforms, sword):
        self.handle_input()
        self.apply_gravity()
        self.check_collision(platforms)

        # Handle sword pickup and storing in hotbar
        if self.rect.colliderect(sword.rect) and sword:
            for i in range(3):
                if self.hotbar[i] is None:
                    self.hotbar[i] = sword
                    sword.rect.x, sword.rect.y = -100, -100  # Hide the sword after pickup
                    break

    def equip_weapon(self, weapon, slot):
        self.holding_item = weapon  # Equip the selected item from hotbar
        self.hotbar[slot] = None  # Remove from hotbar after equipping
        self.selected_slot = slot  # Update selected slot

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))  # Apply camera to player

    def draw_hotbar(self, screen):
        font = pygame.font.SysFont(None, 30)
        for i, weapon in enumerate(self.hotbar):
            rect = pygame.Rect(10 + i * 60, 550, 50, 40)
            if weapon:
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                screen.blit(weapon.image, rect.topleft)  # Display weapon in the hotbar
            else:
                pygame.draw.rect(screen, (200, 200, 200), rect, 2)
                text = font.render("Empty", True, (0, 0, 0))
                screen.blit(text, (rect.x + 5, rect.y + 5))
