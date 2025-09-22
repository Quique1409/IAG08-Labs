from Boat import Boat
from Mesh import Mesh
class Player:
    """Clase padre para todos los tipos de jugadores."""
    def __init__(self, name):
        self.name = name
        self.own_grid = Mesh()
        self.opponent_grid = Mesh() # View of opponent's grid
        self.boat_fleet = [
            Boat(5, "Carrier (Length: 5)"), Boat(4, "Battleship (Length: 4)"),
            Boat(3, "Cruiser (Length: 3)"), Boat(3, "Submarine (Length: 3)"), Boat(2, "Destroyer (Length: 2)")
        ]

    def place_boats(self):
        """Método abstracto para colocar barcos."""
        raise NotImplementedError

    def make_shot(self):
        """Método abstracto para realizar un disparo."""
        raise NotImplementedError

    def has_lost(self):
        """Verifica si este jugador ha perdido."""
        return self.own_grid.all_boats_sunk()