from Player import Player
class HumanPlayer(Player):
    """Representa a un jugador humano. Hereda de Player."""
    def place_boats(self):
        print(f"\n{self.name}, es hora de colocar tus barcos.")
        for boat in self.boat_fleet:
            placed = False
            while not placed:
                self.own_grid.display()
                print(f"Colocando {boat.name} (tamaño: {boat.size})")
                try:
                    prompt = f"Ingresa coordenada de inicio (ej. A5) y orientación (H/V), ej. A5 H: "
                    placement = input(prompt).strip().upper().split()
                    coord_str, orientation = placement[0], placement[1]

                    col = ord(coord_str[0]) - ord('A')
                    row = int(coord_str[1:]) - 1

                    if orientation not in ['H', 'V']:
                        raise ValueError("Orientación inválida.")
                    if not (0 <= row < self.own_grid.size and 0 <= col < self.own_grid.size):
                         raise ValueError("Coordenadas fuera del tablero.")

                    if self.own_grid.place_boat(boat, row, col, orientation):
                        placed = True
                    else:
                        print("No se puede colocar el barco ahí. Ya está ocupado o fuera del tablero.")
                except (ValueError, IndexError):
                    print("Formato de entrada inválido. Por favor, usa el formato 'A5 H'.")

    def make_shot(self):
        while True:
            try:
                coord_str = input(f"{self.name}, ingresa la coordenada para tu disparo (ej. B7): ").strip().upper()
                col = ord(coord_str[0]) - ord('A')
                row = int(coord_str[1:]) - 1
                if not (0 <= row < self.opponent_grid_view.size and 0 <= col < self.opponent_grid_view.size):
                    raise ValueError("Coordenadas fuera del tablero.")
                if self.opponent_grid_view.grid[row][col] != '.':
                    print("Ya has disparado a esa coordenada. Intenta de nuevo.")
                    continue
                return row, col
            except (ValueError, IndexError):
                print("Coordenada inválida. Por favor, usa el formato 'B7'.")