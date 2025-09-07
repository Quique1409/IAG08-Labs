from IAPlayer import IAPlayer
class GoalBasedAgentPlayer(IAPlayer):
    """Un agente más avanzado basado en objetivos. Hereda de IAPlayer."""
    def __init__(self, name="Goal-Based AI"):
        super().__init__(name)
        self.mode = 'HUNT' # HUNT (cazar) o TARGET (apuntar)
        self.target_hits = []

    def make_shot(self):
        if self.mode == 'TARGET':
            shot = self._target_shot()
            if shot:
                return shot
            else:
                # El modo TARGET falló (¿quizás se hundió?), vuelve a HUNT
                self.mode = 'HUNT'
                self.target_hits = []

        # Modo HUNT
        # Usa un patrón de tablero de ajedrez para una caza más eficiente
        possible_shots = []
        for r in range(self.opponent_grid_view.size):
            for c in range(self.opponent_grid_view.size):
                if (r + c) % 2 == 0 and self.opponent_grid_view.grid[r][c] == '.':
                    possible_shots.append((r, c))
        
        if not possible_shots: # Si el patrón de ajedrez está completo, llena los huecos
            for r in range(self.opponent_grid_view.size):
                for c in range(self.opponent_grid_view.size):
                    if self.opponent_grid_view.grid[r][c] == '.':
                        possible_shots.append((r,c))

        return random.choice(possible_shots) if possible_shots else self._random_fallback_shot()
    
    def _random_fallback_shot(self):
        """Disparo aleatorio si no quedan más opciones."""
        while True:
            row = random.randint(0, self.opponent_grid_view.size - 1)
            col = random.randint(0, self.opponent_grid_view.size - 1)
            if self.opponent_grid_view.grid[row][col] == '.':
                return row, col

    def _target_shot(self):
        """Lógica para disparar cuando un barco ha sido golpeado pero no hundido."""
        potential_targets = set()
        for r, c in self.target_hits:
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.opponent_grid_view.size and \
                   0 <= nc < self.opponent_grid_view.size and \
                   self.opponent_grid_view.grid[nr][nc] == '.':
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
                if max_c + 1 < self.opponent_grid_view.size: line_targets.append((row, max_c + 1))
            else: # Vertical
                col = first_hit[1]
                rows = [r for r,c in self.target_hits]
                min_r, max_r = min(rows), max(rows)
                if min_r - 1 >= 0: line_targets.append((min_r - 1, col))
                if max_r + 1 < self.opponent_grid_view.size: line_targets.append((max_r + 1, col))

            valid_line_targets = [t for t in line_targets if self.opponent_grid_view.grid[t[0]][t[1]] == '.']
            if valid_line_targets:
                return random.choice(valid_line_targets)

        if potential_targets:
            return random.choice(list(potential_targets))
        
        return None # No se encontraron objetivos válidos