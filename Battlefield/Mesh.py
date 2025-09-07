class Mesh:
    """Represents the game grid for a player."""
    def __init__(self, size=10):
        self.size = size
        # Grid representations:
        # '.' for empty, 'O' for boat, 'X' for hit, 'M' for miss
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.boats = []

    def display(self, hide_boats=False):
        """Prints the grid to the console."""
        print("   " + " ".join([chr(ord('A') + i) for i in range(self.size)]))
        for r in range(self.size):
            row_num = str(r + 1).rjust(2)
            display_row = []
            for c in range(self.size):
                if hide_boats and self.grid[r][c] == 'O':
                    display_row.append('.')
                else:
                    display_row.append(self.grid[r][c])
            print(f"{row_num} " + " ".join(display_row))
        print()

    def _can_place_boat(self, boat, row, col, orientation):
        """Checks if a boat can be placed at a specific location."""
        if orientation == 'H':
            if col + boat.size > self.size:
                return False
            for i in range(boat.size):
                if self.grid[row][col + i] != '.':
                    return False
        else: # Vertical
            if row + boat.size > self.size:
                return False
            for i in range(boat.size):
                if self.grid[row + i][col] != '.':
                    return False
        return True

    def place_boat(self, boat, row, col, orientation):
        """Places a boat on the grid."""
        if not self._can_place_boat(boat, row, col, orientation):
            return False

        boat.positions = []
        if orientation == 'H':
            for i in range(boat.size):
                self.grid[row][col + i] = 'O'
                boat.positions.append((row, col + i))
        else: # Vertical
            for i in range(boat.size):
                self.grid[row + i][col] = 'O'
                boat.positions.append((row + i, col))
        self.boats.append(boat)
        return True

    def receive_shot(self, row, col):
        """
        Processes a shot at a given coordinate.
        Returns: 'HIT', 'MISS', 'SUNK', or None if already shot.
        """
        if self.grid[row][col] == 'X' or self.grid[row][col] == 'M':
            return None # Already shot here

        if self.grid[row][col] == 'O':
            self.grid[row][col] = 'X'
            for boat in self.boats:
                if (row, col) in boat.positions:
                    boat.hits += 1
                    if boat.is_sunk():
                        print(f"You sunk their {boat.name}!")
                        return 'SUNK'
                    return 'HIT'
        else:
            self.grid[row][col] = 'M'
            return 'MISS'

    def all_boats_sunk(self):
        """Checks if all boats on this grid are sunk."""
        return all(boat.is_sunk() for boat in self.boats)