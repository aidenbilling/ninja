import pygame
from src.player import Player
from src.sword import Sword
from src.enemies import Ninja
from src.game_platform import Platform
from src.camera import Camera
from src.levels import level_1

class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.WHITE = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ninja Man Prototype")

        self.clock = pygame.time.Clock()
        self.camera = Camera(self.WIDTH, self.HEIGHT, 1600, 1200)

        self.state = "menu"
        self.menu_options = ["Play", "Options", "Exit"]
        self.selected_option = 0

        self.platforms = []
        self.items = []
        self.ninjas = []
        self.player = Player(self.WIDTH // 2, self.HEIGHT - 100)

    def handle_menu(self, keys):
        if keys[pygame.K_UP]:
            self.selected_option = max(0, self.selected_option - 1)
        elif keys[pygame.K_DOWN]:
            self.selected_option = min(len(self.menu_options) - 1, self.selected_option + 1)

        if keys[pygame.K_RETURN]:
            if self.selected_option == 0:
                self.state = "playing"
                self.load_level(level_1)
            elif self.selected_option == 1:
                print("Options menu is not implemented yet.")
            elif self.selected_option == 2:
                pygame.quit()
                quit()

    def load_level(self, level_layout):
        self.platforms.clear()
        self.items.clear()
        self.ninjas.clear()

        tile_size = 40
        for row_index, row in enumerate(level_layout):
            for col_index, tile in enumerate(row):
                if tile == "#":
                    platform = Platform(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                    self.platforms.append(platform)
                elif tile == "@":
                    sword = Sword(col_index * tile_size, row_index * tile_size)
                    self.items.append(sword)
                elif tile == "N":
                    ninja = Ninja(col_index * tile_size, row_index * tile_size, 50, 50, 0.5)
                    self.ninjas.append(ninja)

        if self.platforms:
            self.player.rect.bottom = self.platforms[0].rect.top

    def update(self):
        keys = pygame.key.get_pressed()
        if self.state == "menu":
            self.handle_menu(keys)
        elif self.state == "playing":
            self.player.update(keys, self.platforms, self.items[0] if self.items else None)

            for ninja in self.ninjas:
                ninja.update(self.platforms, self.player)
                if ninja.rect.colliderect(self.player.rect):
                    self.player.health -= 1  # Enemy deals damage

            if self.player.health <= 0:
                self.state = "death"

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

            self.player.draw(self.screen, self.camera)
            self.draw_health_bar()
        elif self.state == "death":
            self.draw_death_menu()

        pygame.display.flip()

    def draw_health_bar(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, 200, 20))
        current_width = 200 * (self.player.health / 100)
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, current_width, 20))

    def draw_menu(self):
        font = pygame.font.SysFont(None, 50)
        title_text = font.render("Ninja Man Prototype", True, (0, 0, 0))
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

            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
