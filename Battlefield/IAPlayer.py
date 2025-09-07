from Player import Player
import random
class IAPlayer(Player):
    """Class for the AI Agents. Inherit from Player."""
    def place_boats_randomly(self):
        """Random position of boats."""
        for boat in self.boat_fleet: #iterate over the boats, it means 5 times
            spot = False
            while not spot:
                #select a random place in the board
                col = random.randint(0, self.own_grid.size - 1)
                row = random.randint(0, self.own_grid.size - 1) 
                orientation = random.choice(['H', 'V']) #select a rando orientation
                spot = self.own_grid.place_boat(boat, col, row, orientation)