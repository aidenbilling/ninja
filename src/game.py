import pygame
from src.player import Player
from src.sword import Sword
from src.enemies import Ninja, Archer
from src.game_platform import Platform
from src.camera import Camera
from src.levels import level_1, level_2, level_3
from src.key import Key
from src.door import Door
from src.bow import Bow

class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.WHITE = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ninja Man 1")

        self.clock = pygame.time.Clock()
        self.camera = Camera(self.WIDTH, self.HEIGHT, 1600, 1200)

        self.state = "menu"
        self.menu_options = ["Play", "Controls", "Exit"]
        self.selected_option = 0
        self.menu_timer = 0

        self.platforms = []
        self.items = []
        self.ninjas = []
        self.archers = []
        self.player = Player(self.WIDTH // 2, self.HEIGHT - 100)

        self.levels = [level_1, level_2, level_3]
        self.current_level_index = 0

        # Initialize projectile list
        self.projectiles = []

    def handle_menu(self, keys):
        # Gradual movement for option selection
        if self.menu_timer <= 0:
            if keys[pygame.K_1]:
                self.selected_option = 0
            elif keys[pygame.K_2]:
                self.selected_option = 1
            elif keys[pygame.K_3]:
                self.selected_option = 2

        if keys[pygame.K_RETURN]:
            if self.selected_option == 0:
                self.state = "playing"
                self.current_level_index = 0
                self.load_level(self.levels[self.current_level_index])
            elif self.selected_option == 1:
                self.state = "controls"  # Go to controls menu
            elif self.selected_option == 2:
                pygame.quit()
                quit()

    def load_controls_menu(self):
        # Simple controls display in the controls menu
        font = pygame.font.SysFont(None, 40)
        controls_text = [
            "Arrow keys - Movement",
            "Space - Use item",
        ]

        y_offset = 100
        for text in controls_text:
            control_text = font.render(text, True, (0, 0, 0))
            self.screen.blit(control_text, (self.WIDTH // 2 - control_text.get_width() // 2, y_offset))
            y_offset += 50

        back_text = font.render("Press [Esc] to return", True, (0, 0, 0))
        self.screen.blit(back_text, (self.WIDTH // 2 - back_text.get_width() // 2, y_offset))

    def load_level(self, level_layout):
        self.platforms.clear()
        self.items.clear()
        self.ninjas.clear()
        self.archers.clear()

        tile_size = 40
        for row_index, row in enumerate(level_layout):
            for col_index, tile in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size
                if tile == "#":
                    self.platforms.append(Platform(x, y, tile_size, tile_size))
                elif tile == "@":
                    self.items.append(Sword(x, y))
                elif tile == "K":
                    self.items.append(Key(x, y))
                elif tile == "D":
                    self.items.append(Door(x, y))
                elif tile == "N":
                    self.ninjas.append(Ninja(x, y, 50, 50, 1))
                elif tile == "A":
                    self.archers.append(Archer(x, y, 50, 50, 1))

        if self.platforms:
            self.player.rect.bottom = self.platforms[0].rect.top
            self.player.pos = pygame.math.Vector2(self.player.rect.topleft)

        self.player.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if self.state == "menu":
            self.handle_menu(keys)
        elif self.state == "playing":
            self.player.update(keys, self.platforms, self.items, self.ninjas + self.archers)

            if keys[pygame.K_SPACE] and self.player.holding_item and isinstance(self.player.holding_item, Sword):
                self.player.attack(self.ninjas + self.archers)

            # Handle projectile shooting
            if keys[pygame.K_f] and self.player.holding_item and isinstance(self.player.holding_item, Bow):
                self.player.shoot_projectile(self.projectiles)

            for item in self.items:
                if isinstance(item, Door):
                    item.update(self.player)
                    if not item.locked:
                        self.advance_level()

            for ninja in self.ninjas[:]:
                ninja.update(self.platforms, self.player)
                if ninja.health <= 0:
                    self.ninjas.remove(ninja)

            for archer in self.archers[:]:
                archer.update(self.platforms, self.player)
                if archer.health <= 0:
                    self.archers.remove(archer)

            # Update projectiles
            for projectile in self.projectiles[:]:
                projectile.update()
                if projectile.rect.x < 0 or projectile.rect.x > self.WIDTH:
                    self.projectiles.remove(projectile)

            if self.player.health <= 0:
                self.state = "death"

        elif self.state == "controls":
            if keys[pygame.K_ESCAPE]:  # Exit the controls menu
                self.state = "menu"

    def advance_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.load_level(self.levels[self.current_level_index])
            self.player.holding_key = False
            self.player.hotbar = [None] * 3
            print(f"Loaded Level {self.current_level_index + 1}")
        else:
            print("You've completed all levels!")
            self.state = "menu"
            self.player.health = 100

    def draw(self):
        self.screen.fill(self.WHITE)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.camera.update(self.player)

            for platform in self.platforms:
                platform.draw(self.screen, self.camera)

            for item in self.items:
                item.draw(self.screen, self.camera)

            for ninja in self.ninjas:
                ninja.draw(self.screen, self.camera)

            for archer in self.archers:
                archer.draw(self.screen, self.camera)

            self.player.draw(self.screen, self.camera)

            # Draw projectiles
            for projectile in self.projectiles:
                pygame.draw.rect(self.screen, (255, 0, 0), projectile.rect)

            self.draw_health_bar()

        elif self.state == "death":
            self.draw_death_menu()
        elif self.state == "controls":
            self.load_controls_menu()

        pygame.display.flip()

    def draw_health_bar(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, 200, 20))
        current_width = 200 * (self.player.health / 100)
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, current_width, 20))

    def draw_menu(self):
        font = pygame.font.SysFont(None, 50)
        title_text = font.render("Ninja Man 1", True, (0, 0, 0))
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 100))

        option_font = pygame.font.SysFont(None, 30)
        for i, option in enumerate(self.menu_options):
            color = (255, 0, 0) if i == self.selected_option else (0, 0, 0)
            option_text = option_font.render(option, True, color)
            self.screen.blit(option_text, (self.WIDTH // 2 - option_text.get_width() // 2, 200 + i * 50))

    def draw_death_menu(self):
        font = pygame.font.SysFont(None, 60)
        death_text = font.render("You Died", True, (200, 0, 0))
        self.screen.blit(death_text, (self.WIDTH // 2 - death_text.get_width() // 2, 200))

        font_small = pygame.font.SysFont(None, 40)
        return_text = font_small.render("Press [R] to return to menu", True, (0, 0, 0))
        self.screen.blit(return_text, (self.WIDTH // 2 - return_text.get_width() // 2, 300))

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()

            if self.state == "death":
                if keys[pygame.K_r]:
                    self.state = "menu"
                    self.player.health = 100
                    self.player.holding_key = False
                    self.player.hotbar = [None] * 3

            self.update()
            self.draw()

        pygame.quit()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += self.direction * 10
        if self.rect.x < 0 or self.rect.x > 800:  # Remove if it goes out of bounds
            self.kill()


if __name__ == "__main__":
    game = Game()
    game.run()
