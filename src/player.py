import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 20
        
        character_path = os.path.join("assets", "player.png")
        self.image = pygame.image.load(character_path)

        self.x = 50
        self.y = 50

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.speed = 3

    def movement(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a]:
            self.x -= self.speed
        if keys_pressed[pygame.K_d]:
            self.x += self.speed

        self.rect.topleft = (self.x, self.y)

    def draw(self, canvas):
        canvas.blit(self.image, self.rect.topleft)
    
    def update(self):
        self.movement()
        self.draw(canvas)