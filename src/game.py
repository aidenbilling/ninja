import pygame
from src.player import Player
from src.sword import Sword
from src.enemies import Ninja
from src.game_platform import Platform
from src.camera import Camera
from src.levels import level_1  # Import level layout from levels.py

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
        self.items = []  # List to hold items like sword
        self.ninjas = []  # List to hold ninja enemies
        self.player = Player(self.WIDTH // 2, self.HEIGHT - 100)  # Initialize player

    def handle_menu(self, keys):
        """Handle the menu navigation."""
        if keys[pygame.K_UP]:
            self.selected_option = max(0, self.selected_option - 1)
        elif keys[pygame.K_DOWN]:
            self.selected_option = min(len(self.menu_options) - 1, self.selected_option + 1)

        if keys[pygame.K_RETURN]:
            if self.selected_option == 0:
                self.state = "playing"  # Start the game when "Play" is selected
                self.load_level(level_1)  # Load the first level when playing
            elif self.selected_option == 1:
                print("Options menu is not implemented yet.")
            elif self.selected_option == 2:
                pygame.quit()
                quit()

    def load_level(self, level_layout):
        """Load the level layout into the game."""
        self.platforms.clear()  # Clear previous platforms
        self.items.clear()  # Clear previous items
        self.ninjas.clear()  # Clear previous ninjas

        tile_size = 40  # Size of each tile (platform)
        for row_index, row in enumerate(level_layout):
            for col_index, tile in enumerate(row):
                if tile == "#":  # Platform tile
                    platform = Platform(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                    self.platforms.append(platform)
                elif tile == "@":  # Special tile for sword or other items
                    sword = Sword(col_index * tile_size, row_index * tile_size)
                    self.items.append(sword)
                elif tile == "N":  # Special tile for ninja enemies
                    ninja = Ninja(col_index * tile_size, row_index * tile_size, 50, 50, 2)
                    self.ninjas.append(ninja)

        # Place the player on the first platform after loading the level
        if self.platforms:
            self.player.rect.bottom = self.platforms[0].rect.top  # Place player on top of the first platform

    def update(self):
        """Update game objects."""
        keys = pygame.key.get_pressed()
        if self.state == "menu":
            self.handle_menu(keys)  # Call the menu handling
        else:
            self.player.update(keys, self.platforms, self.items)
            for ninja in self.ninjas:
                ninja.update(self.platforms, self.player)

    def draw(self):
        """Draw game objects."""
        self.screen.fill(self.WHITE)

        if self.state == "menu":
            self.draw_menu()
        else:
            self.camera.update(self.player)

            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen, self.camera)

            # Draw items (e.g., sword)
            for item in self.items:
                item.draw(self.screen, self.camera)

            # Draw player and ninjas
            self.player.draw(self.screen, self.camera)
            for ninja in self.ninjas:
                ninja.draw(self.screen, self.camera)
            self.player.draw_hotbar(self.screen)

        pygame.display.flip()

    def draw_menu(self):
        """Draw the menu screen."""
        font = pygame.font.SysFont(None, 50)
        title_text = font.render("Ninja Man Prototype", True, (0, 0, 0))
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 100))

        option_font = pygame.font.SysFont(None, 30)
        for i, option in enumerate(self.menu_options):
            color = (255, 0, 0) if i == self.selected_option else (0, 0, 0)
            option_text = option_font.render(option, True, color)
            self.screen.blit(option_text, (self.WIDTH // 2 - option_text.get_width() // 2, 200 + i * 50))

    def run(self):
        """Run the game loop."""
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
    game = Game()
    game.run()


