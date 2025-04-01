import pygame
from src.sword import Sword

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False
        self.hotbar = []  # Holds items like the sword

        self.hotbar = [None] * 3  # Hotbar with 3 slots (expandable)
        self.selected_slot = 0  # Index of selected hotbar slot
        self.holding_item = None  # Currently held item
 
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0  # Reset horizontal movement

        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = self.jump_power  # Jump if on the ground

        for i in range(3):  # Check keys K_1 to K_3
            if keys[pygame.K_1 + i]:  
                self.selected_slot = i
                self.holding_item = self.hotbar[i]  # Update held item
        
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

    def pick_up_sword(self, sword):
        if self.rect.colliderect(sword.rect) and not sword.picked_up:  # Ensure the player is touching the sword
            for i in range(len(self.hotbar)):  # Find an empty slot
                if self.hotbar[i] is None:
                    self.hotbar[i] = sword
                    sword.picked_up = True  # Mark the sword as picked up
                    break  


    def update(self, platforms, sword):
        self.handle_input()
        self.apply_gravity()
        self.check_collision(platforms)
        self.pick_up_sword(sword)  # Check if player picks up the sword

        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))  # Clamping horizontally (800px width)
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))  # Clamping vertically (600px height)

    def draw_hotbar(self, screen):
        for i in range(len(self.hotbar)):
            x = 10 + i * 60  # Position hotbar slots
            color = (255, 255, 255) if i == self.selected_slot else (50, 50, 50)  # Highlight selected slot
            pygame.draw.rect(screen, color, (x, 10, 50, 50), border_radius=5)

            if isinstance(self.hotbar[i], Sword):  # Draw sword in hotbar
                pygame.draw.rect(screen, (255, 0, 0), (x + 10, 25, 30, 10))  

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)  # Blue player

        if isinstance(self.holding_item, Sword):
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x + 20, self.rect.y + 10, 30, 10))

        self.draw_hotbar(screen)  # Draw hotbar