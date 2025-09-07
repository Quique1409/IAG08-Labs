class Game:
    """Manages the main game loop and player turns."""
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2
        self.winner = None

    def setup_game(self):
        """Initializes the game by having players place their boats."""
        self.player1.place_boats()
        self.player2.place_boats()

    def play_turn(self, silent_mode=False):
        """Executes a single turn for the current player."""
        if not silent_mode:
            clear_screen()
            print(f"--- Turno de {self.current_player.name} ---")
            print("Tu tablero:")
            self.current_player.own_grid.display()
            print("Tu vista del tablero del oponente:")
            self.current_player.opponent_grid_view.display(hide_boats=True)

        row, col = self.current_player.make_shot()
        result = self.other_player.own_grid.receive_shot(row, col)

        if result:
            if result == 'HIT':
                self.current_player.opponent_grid_view.grid[row][col] = 'X'
            elif result == 'SUNK':
                self.current_player.opponent_grid_view.grid[row][col] = 'X'
                if not silent_mode:
                    sunk_boat = next(b for b in self.other_player.own_grid.boats if all(self.other_player.own_grid.grid[r][c]=='X' for r,c in b.positions))
                    print(f"¡Hundiste su {sunk_boat.name}!")
            else: # MISS
                self.current_player.opponent_grid_view.grid[row][col] = 'M'

            # Lógica para que los agentes de IA actualicen su estado
            if isinstance(self.current_player, ReflexAgent):
                if result in ['HIT', 'SUNK']:
                    self.current_player.last_hit = (row, col)
                    if result == 'SUNK':
                        self.current_player.last_hit = None
                else:
                    self.current_player.last_hit = None
            if isinstance(self.current_player, GoalBasedAgent):
                if result in ['HIT', 'SUNK']:
                    self.current_player.mode = 'TARGET'
                    self.current_player.target_hits.append((row, col))
                    if result == 'SUNK':
                        # Verifica si el barco que contiene TODOS los target_hits está hundido
                        is_target_boat_sunk = False
                        for boat in self.other_player.own_grid.boats:
                            if all(hit in boat.positions for hit in self.current_player.target_hits):
                                if boat.is_sunk():
                                    is_target_boat_sunk = True
                                    break
                        if is_target_boat_sunk:
                            self.current_player.mode = 'HUNT'
                            self.current_player.target_hits = []
        
        if not silent_mode:
            coord_str = f"{chr(ord('A') + col)}{row + 1}"
            print(f"{self.current_player.name} dispara a {coord_str}... Resultado: {result if result else 'YA HABÍAS DISPARADO AHÍ'}")
            input("Presiona Enter para continuar al siguiente turno...")

        if self.other_player.has_lost():
            self.winner = self.current_player
        else:
            self.current_player, self.other_player = self.other_player, self.current_player

    def run_game(self, silent_mode=False):
        """Starts and runs the main game loop."""
        self.setup_game()
        while not self.winner:
            self.play_turn(silent_mode=silent_mode)
        
        if not silent_mode:
            clear_screen()
            print(f"--- ¡Fin del Juego! ---")
            print(f"¡El ganador es {self.winner.name}!")
            print(f"\nTablero final de {self.player1.name}:")
            self.player1.own_grid.display()
            print(f"\nTablero final de {self.player2.name}:")
            self.player2.own_grid.display()
        
        return self.winner

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')