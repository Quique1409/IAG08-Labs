from Boat import Boat
from Mesh import Mesh
class Player:
    """Father class for all the players."""
    def __init__(self, name):
        self.name = name
        self.own_grid = Mesh()
        self.opponent_grid = Mesh() # View of opponent's grid
        self.boat_fleet = [ #fleet of every player
            Boat(5, "Carrier (Length: 5)"), Boat(4, "Battleship (Length: 4)"),
            Boat(3, "Cruiser (Length: 3)"), Boat(3, "Submarine (Length: 3)"), Boat(2, "Destroyer (Length: 2)")
        ]

    def place_boats(self):
        """Abstract method for place boats"""
        raise NotImplementedError

    def make_shot(self):
        """Abstract method for shoot"""
        raise NotImplementedError

    def has_lost(self):
        """Call a method of the class Mesh to check if all boats are sunk."""
        return self.own_grid.fleet_sunk()