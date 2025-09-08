from IAPlayer import IAPlayer
import random
class ReflexAgentPlayer(IAPlayer):
    """Simple Reflex AI. Inherit from IAPlayer."""
    def __init__(self, name="Reflex AI"):
        super().__init__(name) #Inherit the constructor of IAPlayer
        self.last_hit = None # Store the coordinates of the last hit (if any)

    def make_shot(self):
        # If we get a hit last time, try adjacent cells
        if self.last_hit:
            column, row = self.last_hit #row and column of the last hit
            close_targets = [] #list of the valid targets next to the last hit
            for x, y in [(0,1), (0,-1), (1,0), (-1,0)]:
                new_column, new_row = column + x, row + y
                if 0 <= new_row < self.opponent_grid.size and \
                0 <= new_column < self.opponent_grid.size and \
                self.opponent_grid.grid[new_column][new_row] == '.': #check that new coordinates are valid and not shot before        
                    close_targets.append((new_column, new_row))

            if close_targets:
                return random.choice(close_targets) #select a random target from the list
            else:
                # If we already shoot all the neighbros, reset last_hit list
                self.last_hit = None

        # If we don't have a last hit or no valid neighbors, shoot randomly
        while True:
            column = random.randint(0, self.opponent_grid.size - 1) #if still didnt shoot, shoot randomly
            row = random.randint(0, self.opponent_grid.size - 1)
            if self.opponent_grid.grid[column][row] == '.':
                return column, row