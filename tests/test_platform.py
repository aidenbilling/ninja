import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pygame
from src.game_platform import Platform 
from pygame.rect import Rect

# Initialize pygame and set up display
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

# Mock player object for testing platform collision
@pytest.fixture
def mock_player():
    class MockPlayer:
        def __init__(self):
            self.rect = Rect(100, 150, 50, 50)  # Player size and initial position
    return MockPlayer()

def test_platform_collision(mock_player):
    platform = Platform(x=0, y=200, width=640, height=50)  # Platform at the bottom
    player = mock_player
    player.rect.y -= 10  # Position player above the platform for collision test

    # Simulate gravity by moving the player down
    player.rect.y += 5
    assert player.rect.colliderect(platform.rect)  # Check for collision

    # Simulate the player standing on the platform
    player.rect.y = platform.rect.top - player.rect.height
    assert player.rect.bottom == platform.rect.top  # The player should land on the platform
