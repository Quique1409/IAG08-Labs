from Player import Player
import random
class IAPlayer(Player):
    """Clase base para los agentes de IA. Hereda de Player."""
    def place_boats(self):
        """Coloca los barcos de forma aleatoria en el tablero."""
        for boat in self.boat_fleet:
            placed = False
            while not placed:
                row = random.randint(0, self.own_grid.size - 1)
                col = random.randint(0, self.own_grid.size - 1)
                orientation = random.choice(['H', 'V'])
                placed = self.own_grid.place_boat(boat, row, col, orientation)