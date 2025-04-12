import pygame
from src.player import Player
from src.sword import Sword
from src.enemies import Ninja
from src.game_platform import Platform
from src.camera import Camera

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

        self.platforms = [
            Platform(0, self.HEIGHT - 20, self.WIDTH, 20),
            Platform(100, 400, 200, 20),
            Platform(400, 500, 300, 20),
            Platform(800, 600, 250, 20),
        ]

        self.player = Player(self.WIDTH // 2, self.HEIGHT - 100)
        self.sword = Sword(350, 350)
        self.ninja = Ninja(100, 100, 50, 50, 2)

    def load_level(self, level_layout):
        self.platforms.clear()
        tile_size = 40
        for row_index, row in enumerate(level_layout):
            for col_index, tile in enumerate(row):
                if tile == "#":
                    platform = Platform(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                    self.platforms.append(platform)

    def update(self):
        keys = pygame.key.get_pressed()
        if self.state == "menu":
            self.handle_menu(keys)
        else:
            self.player.update(keys, self.platforms, self.sword)
            self.ninja.update(self.platforms, self.player)

    def handle_menu(self, keys):
        if keys[pygame.K_UP]:
            self.selected_option = max(0, self.selected_option - 1)
        elif keys[pygame.K_DOWN]:
            self.selected_option = min(len(self.menu_options) - 1, self.selected_option + 1)

        if keys[pygame.K_RETURN]:
            if self.selected_option == 0:
                self.state = "playing"
            elif self.selected_option == 1:
                print("Options menu is not implemented yet.")
            elif self.selected_option == 2:
                pygame.quit()
                quit()

    def draw(self):
        self.screen.fill(self.WHITE)

        if self.state == "menu":
            self.draw_menu()
        else:
            self.camera.update(self.player)

            for platform in self.platforms:
                platform.draw(self.screen, self.camera)

            # Draw sword only if it hasn't been picked up
            if self.sword and not self.sword.picked_up:
                self.sword.draw(self.screen, self.camera)

            self.player.draw(self.screen, self.camera)
            self.ninja.draw(self.screen, self.camera)
            self.player.draw_hotbar(self.screen)

        pygame.display.flip()

    def draw_menu(self):
        font = pygame.font.SysFont(None, 50)
        title_text = font.render("Ninja Man Prototype", True, (0, 0, 0))
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 100))

        option_font = pygame.font.SysFont(None, 30)
        for i, option in enumerate(self.menu_options):
            color = (255, 0, 0) if i == self.selected_option else (0, 0, 0)
            option_text = option_font.render(option, True, color)
            self.screen.blit(option_text, (self.WIDTH // 2 - option_text.get_width() // 2, 200 + i * 50))

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    from src.levels import level_1
    game = Game()
    game.load_level(level_1)
    game.run()
