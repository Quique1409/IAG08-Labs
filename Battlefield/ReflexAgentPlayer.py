from IAPlayer import IAPlayer
import random
class ReflexAgentPlayer(IAPlayer):
    """Un agente reflejo simple. Hereda de IAPlayer."""
    def __init__(self, name="Reflex AI"):
        super().__init__(name)
        self.last_hit = None

    def make_shot(self):
        # Si tuvimos un HIT en el último turno, dispara cerca
        if self.last_hit:
            r, c = self.last_hit
            potential_targets = []
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.opponent_grid_view.size and \
                   0 <= nc < self.opponent_grid_view.size and \
                   self.opponent_grid_view.grid[nr][nc] == '.':
                    potential_targets.append((nr, nc))

            if potential_targets:
                return random.choice(potential_targets)
            else:
                # Si todos los vecinos ya fueron atacados, limpia last_hit y dispara aleatoriamente
                self.last_hit = None

        # De lo contrario, dispara a un lugar válido al azar
        while True:
            row = random.randint(0, self.opponent_grid_view.size - 1)
            col = random.randint(0, self.opponent_grid_view.size - 1)
            if self.opponent_grid_view.grid[row][col] == '.':
                return row, col