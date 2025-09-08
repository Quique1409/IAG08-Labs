from Player import Player
class HumanPlayer(Player):
    """Son class for a real player."""
    def place_boats(self):
        print(f"\n{self.name}, put your boats on the board.")
        for boat in self.boat_fleet:
            placed = False
            while not placed:
                self.own_grid.display()
                print(f"Put your {boat.name} (Size: {boat.size})")
                try:
                    prompt = f"Start coordinate (ej. A5) y orientation (H/V), example: A5 H: "
                    placement = input(prompt).strip().upper().split() # Split input into coordinate and orientation
                    coord_str, orientation = placement[0], placement[1]

                    col = ord(coord_str[0]) - ord('A') # Convert letter to number (A=0, B=1, ...)
                    row = int(coord_str[1:]) - 1 # Convert number to 0-indexed

                    if orientation not in ['H', 'V']: #make sure orientation is valid
                        raise ValueError("Invalid orientation. Use 'H' for horizontal or 'V' for vertical.")
                    if not (0 <= row < self.own_grid.size and 0 <= col < self.own_grid.size): #check for the number is in the range 0-9
                         raise ValueError("Coordinates out of bounds.")

                    if self.own_grid.intro_boat(boat, row, col, orientation): #If sintaxis introduced is correct, try to place the boat
                        placed = True
                    else: # If placement failed, intro_boat() returns False
                        print("This coordinates are already occupied or out of bounds. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input format. Please use the format 'A8 H'.") #The boat in the loop didnt get placed, so we try again

    def make_shot(self):
        while True:
            try:
                coord_str = input(f"{self.name}, input the coordinate for you shot (ej. B7): ").strip().upper() #We get the coordinate from the user
                col = ord(coord_str[0]) - ord('A')
                row = int(coord_str[1:]) - 1
                if not (0 <= row < self.opponent_grid.size and 0 <= col < self.opponent_grid.size):
                    raise ValueError("Coordinates out of bounds.")
                if self.opponent_grid.grid[row][col] != '.':
                    print("You have already shot at this coordinate. Try again.")
                    continue
                return row, col
            except (ValueError, IndexError):
                print("Invalid coordinate. Please use the format 'B7'.")