import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0  # Reset horizontal movement

        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power  # Jump if on the ground

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > 10:  # Terminal velocity
            self.vel_y = 10

    def check_collision(self, platforms):
        self.on_ground = False
        self.rect.y += self.vel_y  # Move vertically first

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        self.rect.x += self.vel_x  # Move horizontally
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:  # Moving left
                    self.rect.left = platform.rect.right

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()
        self.check_collision(platforms)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)  # Blue player
