from IAPlayer import IAPlayer
import random
class ReflexAgentPlayer(IAPlayer):
    """Simple Reflex AI. Inherit IAPlayer."""
    def __init__(self, name="Reflex AI"):
        super().__init__(name)
        self.last_hit = None

    def make_shot(self):
        # If we had a hit last time, try adjacent cells
        if self.last_hit:
            row, column = self.last_hit
            potential_targets = []
            for x, y in [(0,1), (0,-1), (1,0), (-1,0)]: #Iterate in the four possible directions
                nr, nc = row + x, column + y
                if 0 <= nr < self.opponent_grid.size and \
                   0 <= nc < self.opponent_grid.size and \
                   self.opponent_grid.grid[nr][nc] == '.':
                    potential_targets.append((nr, nc)) # Only add if it's a valid, unshot cell

            if potential_targets:
                return random.choice(potential_targets) # Shoot at a random valid adjacent cell
            else:
                # If we dont have valid neighbors, reset last_hit
                self.last_hit = None

        # Otherwise, shoot at a random valid location
        while True:
            row = random.randint(0, self.opponent_grid.size - 1)
            col = random.randint(0, self.opponent_grid.size - 1)
            if self.opponent_grid.grid[row][col] == '.':
                return row, col