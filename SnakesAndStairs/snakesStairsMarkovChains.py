import numpy as np
import time  # To measure how long it takes to calculate the fundamental matrix

# Printing in a more legible way numpy objects in terminal 
np.set_printoptions(precision=4, suppress=True)

# --- Board dimensions and number of faces in dice ---

N_States = 101  # Goes from state 0 (Start) to state 100 (Finish)
N_Faces = 6

def jumps_SnakesandLadders():
    """
    Defines and returns the map of the snakes and ladders.
    If you land at the key, you move to the value.
    """
    jump_map = {
        # Stairs
        3: 19, 7:33, 22: 58, 40:59, 48: 85, 56: 79, 69: 87, 80: 98,
        # Snakes
        96: 58, 89: 47, 80: 39, 66: 1, 44: 26, 52: 49, 37: 18, 47: 9
    }
    return jump_map

# --- Creation of the Markov Chain ---

def transitionMatrix_creation(N_States, n_Faces, jump_map):
    """
    Creates de transition matrix P (101x101) based on the game rules
    """
    P = np.zeros((N_States, N_States))
    Dice_Prob = 1.0 / n_Faces

    # Fill the matrix with the transient states (0 to 99)
    for i in range(N_States - 1):  # i = current state (0 to 99)
        for dice in range(1, n_Faces + 1):  # j = dice roll (1 to 6)
            
            destination_temp = i + dice
            
            # --- Game conditions ---
            if destination_temp > 100:
                #Overshoot: stays in current box
                final_destination = i
            elif destination_temp in jump_map:
                # Fell into a snake or ladder
                final_destination = jump_map[destination_temp]
            else:
                # Normal move
                final_destination = destination_temp
            # --- End game conditions ---
                
            # Add the (1/N_faces) probability to the corresponding box
            P[i, final_destination] += Dice_Prob

    # Defining the absorbing state (Victory)
    #If you reach 100, you must stay in 100
    P[100, 100] = 1.0
    
    return P

def prob_k_steps(P, v0, k):
    """
     v_k = v0 * P^k
    """
    try:
        P_k = np.linalg.matrix_power(P, k) #Elevates matrix P to the power of k
        v_k = v0 @ P_k #Matrix multiplication
        return v_k #Return the probability of being in all states after k moves
    except np.linalg.LinAlgError as e: #Failsafe
        print(f"Error obtaining P^{k}: {e}")
        return None

def expected_moves(P):
    """
    Calculates the average numbers of moves to win
    using the fundamental matrix N = (I - Q)^-1
    """
    # Q = Transtions between transient states (0-99 in our case)
    transient_states = N_States - 1
    Q = P[0:transient_states, 0:transient_states]
    
    # I = Identity matrix (same dimention as the number of transient states)
    I = np.identity(transient_states)
    
    try:
        start_time = time.time()
        N = np.linalg.inv(I - Q)
        end_time = time.time()
        print(f"(Getting N=(I-Q)^-1 took {end_time - start_time:.4f}s)")
        
    except np.linalg.LinAlgError as e:
        print(f"Error obtaining the invert matrix (I-Q): {e}")
        return None

    # t = N * 1 (column vector of ones)
    ones_vector = np.ones((transient_states, 1))
    t = N @ ones_vector
    
    # We only cared fot the expected number of moves starting in the initial state
    expected_moves_value = t[0, 0]
    return expected_moves_value


# --- MAIN ---

def main():
    print("--- Building the transition matrix ---")
    map = jumps_SnakesandLadders()
    P = transitionMatrix_creation(N_States, N_Faces, map)
    print(f"P Dimensions: {P.shape}")
    print("Saving the P matrix in 'transition_matrix.csv'...")
    # fmt='%.4f' max for decimals for each probability
    np.savetxt("transition_matrix.csv", P, delimiter=",", fmt='%.4f')
    print("-" * 30)
    
    # initial state vector v0 = [1, 0, 0, ...]
    #its a row vector, since our matrix is transposed comparing to the ones generated in class
    v0 = np.zeros((1, N_States))
    v0[0, 0] = 1.0
    
    print("--- Probability of being in each box after 25 moves ---")
    v_25 = prob_k_steps(P, v0, 25)
    if v_25 is not None:
        prob_25 = v_25.flatten() # Transforms the 2D array into a 1D array, facilitating the iteration
        for i in range(N_States):
            # {i:3d} alingment of the numbers
            print(f"  Box {i:3d}: {prob_25[i]:.6%}")
        print(f"PROBABILITY OF HAVING WON: {prob_25[100]:.6%}")
    print("-" * 30)

    print("--- Probability of being in each box after 50 moves ---")
    v_50 = prob_k_steps(P, v0, 50)
    if v_50 is not None:
        prob_50 = v_50.flatten() 
        for i in range(N_States):
            print(f"  Casilla {i:3d}: {prob_50[i]:.6%}")
        print(f"PROBABILITY OF HAVING WON: {prob_50[100]:.6%}")
    print("-" * 30)

    print("---Expected number of moves ---")
    expected_moves_value = expected_moves(P)
    if expected_moves_value is not None:
        print(f"The average number of moves to expect to win is: {expected_moves_value:.4f}")
    print("-" * 30)


if __name__ == "__main__":
    main()