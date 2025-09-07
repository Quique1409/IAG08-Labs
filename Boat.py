import random
import time
import os

class Boat:
    """Represents a single boat with its size and position."""
    def __init__(self, size, name):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = 0

    def is_sunk(self):
        """Returns True if the boat has been sunk."""
        return self.hits >= self.size