class Boat:
    """Represents a single boat with its size and position."""
    def __init__(self, size, name):
        self.name = name
        self.size = size # Length of the boat
        self.positions = [] # Tuples where the boat is placed (coordinates)
        self.hits = 0 # Number of hits taken

    def is_sunk(self):
        """Returns True if the boat has been sunk."""
        return self.hits >= self.size # If the hits acumulated are equal to the size