import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pygame
from src.sword import Sword
from pygame.rect import Rect

# Initialize pygame and set up display
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

# Sword fixture
@pytest.fixture
def sword():
    return Sword(300, 300)

def test_sword_initialization(sword):
    assert sword.rect.x == 300
    assert sword.rect.y == 300
    assert not sword.picked_up  # Should be False initially

def test_sword_pickup(sword):
    # Simulate picking up the sword
    sword.picked_up = True
    assert sword.picked_up is True

def test_sword_position_after_movement(sword):
    initial_x, initial_y = sword.rect.x, sword.rect.y
    sword.rect.x += 10
    sword.rect.y += 10
    assert sword.rect.x == initial_x + 10
    assert sword.rect.y == initial_y + 10
