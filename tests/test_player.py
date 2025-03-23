import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pygame
from src.player import Player
from pygame.rect import Rect

# Initialize pygame and set up display
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

# Mock platform object to simulate collision
@pytest.fixture
def mock_platform():
    class MockPlatform:
        def __init__(self):
            self.rect = Rect(0, 200, 640, 50)  # Example platform at the bottom of the screen
    return MockPlatform()

# Mock sword object (if needed)
@pytest.fixture
def mock_sword():
    class MockSword:
        def __init__(self):
            self.rect = Rect(100, 100, 20, 20)
            self.picked_up = False
    return MockSword()

# Player fixture with starting position
@pytest.fixture
def player():
    return Player(x=100, y=100)

def test_player_movement_left(player, mock_platform):
    initial_x = player.rect.x
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT}))
    player.update([mock_platform], None)  # Pass the mock platform
    assert player.rect.x < initial_x

    pygame.event.post(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_LEFT}))  # Stop the movement
    player.update([mock_platform], None)  # Ensure the player stops moving
    assert player.rect.x == initial_x  # The player should stop at the same position

def test_player_movement_right(player, mock_platform):
    initial_x = player.rect.x
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT}))
    player.update([mock_platform], None)  # Pass the mock platform
    assert player.rect.x > initial_x

    pygame.event.post(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_RIGHT}))  # Stop the movement
    player.update([mock_platform], None)  # Ensure the player stops moving
    assert player.rect.x == initial_x  # The player should stop at the same position

def test_jump(player, mock_platform):
    player.on_ground = True  # Set the player on the ground to allow jumping
    initial_y = player.rect.y

    # Simulate the jump key press
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}))
    player.update([mock_platform], None)  # Pass the mock platform
    
    assert player.rect.y < initial_y  # The player should move upwards (y-coordinate decreases)

    # Simulate the key release to stop the jump
    pygame.event.post(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_SPACE}))
    player.update([mock_platform], None)  # Ensure the jump stops at the peak
    assert player.rect.y == initial_y - 1  # The player should be slightly lower than the initial height

    # Ensure the player is on the ground after falling back down
    player.on_ground = True  # Simulate the player landing
    player.update([mock_platform], None)
    assert player.rect.y == mock_platform.rect.top - player.rect.height  # Player should land on the platform
