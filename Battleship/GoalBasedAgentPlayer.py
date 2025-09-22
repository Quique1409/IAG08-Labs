from IAPlayer import IAPlayer
import random
class GoalBasedAgentPlayer(IAPlayer):
    """Agent with behaviors based on a goal. Inherit from IAPlayer."""
    def __init__(self, name="Goal-Based AI"):
        super().__init__(name)
        self.mode = 'HUNT' # Initialize in HUNT state
        """The hunt state let the agent shoot in big spaces between shots for finding a boat."""
        self.target_hits = [] #list of reached hits on a target boat

    def make_shot(self):
        if self.mode == 'TARGET':
            """When a shot hits a boat, the agent passesd to TARGET mode.
            The agent will try to sink the boat by shooting around the hit positions, remembering all the hit positions in target_hits list."""
            shot = self.boat_blood()
            if shot:
                return shot
            else:
                # If TARGET mode failed (maybe the boat sank?), revert to HUNT
                self.mode = 'HUNT'
                self.target_hits = []

        # In case of HUNT state 
        # Use a pattern to cover more space efficiently
        possible_shots = []
        for rows in range(self.opponent_grid.size):
            for columns in range(self.opponent_grid.size): #for cover more space, the agent shoots with a minium distance of 2 cells
                if (rows + columns) % 2 == 0 and self.opponent_grid.grid[rows][columns] == '.': #if the plus of the current row and column is pair and void
                    possible_shots.append((rows, columns)) #add the cell to the possible shots

        if not possible_shots: # If we dont have any possible shots left in the pattern, shoot anywhere valid
            for rows in range(self.opponent_grid.size):
                for column in range(self.opponent_grid.size):
                    if self.opponent_grid.grid[rows][column] == '.':
                        possible_shots.append((rows,column))

        return random.choice(possible_shots)

    def boat_blood(self):
        """If we are in TARGET mode, try to sink the boat by shooting around the hit positions."""
        neighbors_cells = set() # Use a set to avoid duplicates
        for rows, columns in self.target_hits:
            for x, y in [(0,1), (0,-1), (1,0), (-1,0)]:
                nr, nc = rows + x, columns + y
                if 0 <= nr < self.opponent_grid.size and \
                   0 <= nc < self.opponent_grid.size and \
                   self.opponent_grid.grid[nr][nc] == '.':
                    neighbors_cells.add((nr, nc))
        
        # We try to be more intelligent if we have more than one hit
        if len(self.target_hits) > 1: # If we already have two hits, we can determine the orientation if they are next to the other
            first_hit = self.target_hits[0]
            second_hit = self.target_hits[1]
            is_horizontal = first_hit[0] == second_hit[0] # Check if they are in the same row with the first value of the tuple
            
            line_targets = []
            if is_horizontal: #if two hits are in the same row, we use columns for move left and right
                row = first_hit[0]
                cols = [columns for rows,columns in self.target_hits] # Get all columns of the hits
                min_c, max_c = min(cols), max(cols)     # Find the min and max column indices
                if min_c - 1 >= 0: line_targets.append((row, min_c - 1)) # If the hit is not in a border cell, append it
                if max_c + 1 < self.opponent_grid.size: line_targets.append((row, max_c + 1)) #add target to the right if is not in a border cell
            else: # Vertical
                col = first_hit[1]
                rows = [rws for rws,columns in self.target_hits] # Get all rows of the hits
                min_r, max_r = min(rows), max(rows)
                if min_r - 1 >= 0: line_targets.append((min_r - 1, col)) #we analize border cells of the rows from 0 - 9 for hit up and down
                if max_r + 1 < self.opponent_grid.size: line_targets.append((max_r + 1, col))

            valid_line_targets = []

            for t in line_targets: #from the possible targets in line, we check if they are valid
                if self.opponent_grid.grid[t[0]][t[1]] == '.':
                    valid_line_targets.append(t)
                    
            if valid_line_targets:
                return random.choice(valid_line_targets) # Return a random valid target in line if available

        if neighbors_cells:
            return random.choice(list(neighbors_cells)) # If we dont have more than 1 hit, return a random neighbor cell (still in TARGET mode)

        return None # No valid targets found
    