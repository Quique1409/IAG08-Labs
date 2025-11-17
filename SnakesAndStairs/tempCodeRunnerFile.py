def get_jump_map():
    #map for snakes and stairs
    jump_map = {
        # Stairs
        3: 19, 7:33, 22: 58, 40:59, 48: 85, 56: 79, 69: 87, 80: 9,
        # Snakes
        96: 58, 89: 47, 80: 39, 66: 1, 44: 26, 52: 49, 37: 18, 47: 9
    }
    return jump_map