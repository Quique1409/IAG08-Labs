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
            shot = self.target_shot()
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

        if possible_shots:
            shot = random.choice(possible_shots)
        else:
            shot = self.random_shot()
        return shot
    
    def random_shot(self):
        """If we dont have tuples in possible_shots, shoot randomly where it can."""
        while True:
            row = random.randint(0, self.opponent_grid.size - 1)
            col = random.randint(0, self.opponent_grid.size - 1)
            if self.opponent_grid.grid[row][col] == '.':
                return row, col

    def target_shot(self):
        """Lógica para disparar cuando un barco ha sido golpeado pero no hundido."""
        potential_targets = set()
        for r, c in self.target_hits:
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.opponent_grid.size and \
                   0 <= nc < self.opponent_grid.size and \
                   self.opponent_grid.grid[nr][nc] == '.':
                    potential_targets.add((nr, nc))
        
        # Si tenemos múltiples aciertos, intentamos determinar la orientación
        if len(self.target_hits) > 1:
            first_hit = self.target_hits[0]
            second_hit = self.target_hits[1]
            is_horizontal = first_hit[0] == second_hit[0]
            
            line_targets = []
            if is_horizontal:
                row = first_hit[0]
                cols = [c for r,c in self.target_hits]
                min_c, max_c = min(cols), max(cols)
                if min_c - 1 >= 0: line_targets.append((row, min_c - 1))
                if max_c + 1 < self.opponent_grid.size: line_targets.append((row, max_c + 1))
            else: # Vertical
                col = first_hit[1]
                rows = [r for r,c in self.target_hits]
                min_r, max_r = min(rows), max(rows)
                if min_r - 1 >= 0: line_targets.append((min_r - 1, col))
                if max_r + 1 < self.opponent_grid.size: line_targets.append((max_r + 1, col))

            valid_line_targets = [t for t in line_targets if self.opponent_grid.grid[t[0]][t[1]] == '.']
            if valid_line_targets:
                return random.choice(valid_line_targets)

        if potential_targets:
            return random.choice(list(potential_targets))
        
        return None # No se encontraron objetivos válidos