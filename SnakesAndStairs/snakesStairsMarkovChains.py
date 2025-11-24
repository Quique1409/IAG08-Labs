import numpy as np
import time

# Printing in a more legible way numpy objects in terminal 
np.set_printoptions(precision=4, suppress=True)

# --- Board dimensions and number of faces in dice ---

<<<<<<< HEAD
NUM_STATES = 101  # Estados del 0 al 80
NUM_FACES = 6
PROB_DADO = 1.0 / NUM_FACES

def get_jump_map():
    #map for snakes and stairs
    jump_map = {
        # Stairs
        3: 19, 7:33, 22: 58, 40:59, 48: 85, 56: 79, 69: 87, 80: 9,
=======
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
>>>>>>> origin/main
        # Snakes
        96: 58, 89: 47, 80: 39, 66: 1, 44: 26, 52: 49, 37: 18, 47: 9
    }
    return jump_map

<<<<<<< HEAD
def create_tran_matrix(NUM_STATES, jump_map):
    #constructing the transition matrix based on the possibles moves
    M = np.zeros((NUM_STATES, NUM_STATES))
    prob_dado = 1.0 / 6

    # fill the transition matrix P
    for i in range(NUM_STATES - 1):  # i = actual state (0 a 99)
        for dado in range(1, 7):  # iteramos sobre cada resultado del lado (1 a 6)
            d_temp = i + dado
            if d_temp > 100:
                #if we pass from the goal state, we stay in the same state and it means that we already win
                d_final = i
            elif d_temp in jump_map:
                # we are in a snake or stair
                d_final = jump_map[d_temp] #the state given is the key for the and it return the new position on the board
            else:
                # we finish normaly
                d_final = d_temp                
            # Update the transition probability for go from state i to d_final
            M[i, d_final] += prob_dado

    # If we reach the goal state (100), we stay there 100%
    M[100, 100] = 1.0
=======
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
>>>>>>> origin/main
    
    return M #we return the transition matrix

<<<<<<< HEAD
def calculate_prob_k_moves(M, v0, k):
=======
def prob_k_steps(M, v0, k):
    """
     v_k = v0 * P^k
>>>>>>> origin/main
    """
    #calculate the probability distribution after k steps
    # M: transition matrix 
    # v0: initial state vector
    # k: number of steps"""
    try:
<<<<<<< HEAD
        P_k = np.linalg.matrix_power(M, k)
        v_k = v0 @ P_k
        return v_k
    except np.linalg.LinAlgError as e:
        print(f"Error al calcular P^{k}: {e}")
        return None

def expected_moves(P):
    """
    Calculate the expected number of moves
    usando la Matriz Fundamental N = (I - Q)^-1
    """
    # Q = Transiciones entre estados transitorios (0-99)
    # (Tomamos NUM_STATES-1 para ser genéricos, o sea, 100)
    transient_states = NUM_STATES - 1
=======
        start_time = time.time()
        P_k = np.linalg.matrix_power(M, k) #Elevaxtes matrix M to the power of k
        v_k = v0 @ P_k #Matrix multiplication
        end_time = time.time()
        print(f"(Calculating P^{k} and then multiplying v_k: {end_time - start_time:.4f}s)")
        return v_k #Return the vector of probabilities of being in all states after k moves
    except np.linalg.LinAlgError as e: 
        print(f"Error obtaining P^{k}: {e}")
        return None

def iterative_prob_k_steps(M, v0, k):
    v_k = v0.copy()
    try:
        start_time = time.time()
        for step in range(k):
            v_k = v_k @ M  # Matrix multiplication
        end_time = time.time()
        print(f"(Calculating v_k iteratively: {end_time - start_time:.4f}s)")
        return v_k  # Return the vector of probabilities of being in all states after k moves
    except np.linalg.LinAlgError as e:
        print(f"Error obtaining v_{k} iteratively: {e}")
        return None

def expected_moves(P):
    """
    Calculates the average numbers of moves to win
    using the fundamental matrix N = (I - Q)^-1
    """
    # Q = Transtions between transient states (0-99 in our case)
    transient_states = N_States - 1
>>>>>>> origin/main
    Q = P[0:transient_states, 0:transient_states]
    
    # I = Identity matrix (same dimention as the number of transient states)
    I = np.identity(transient_states)
    
    try:
        start_time = time.time()
        N = np.linalg.inv(I - Q)
        end_time = time.time()
        print(f"(Getting N=(I-Q)^-1 took {end_time - start_time:.4f}s)")
        print("Saving the fundamental matrix N in 'fundamental_matrix_N.csv'...")
        np.savetxt("fundamental_matrix_N.csv", N, delimiter=",", fmt='%.4f')
        
    except np.linalg.LinAlgError as e:
        print(f"Error obtaining the invert matrix (I-Q): {e}")
        return None

    # t = N * 1 (column vector of ones)
    ones_vector = np.ones((transient_states, 1))
    t = N @ ones_vector
    
<<<<<<< HEAD
    # Queremos el tiempo esperado empezando desde el estado 0
    moves = t[0, 0]
    return moves

def main():
    SS = get_jump_map()
    M = create_tran_matrix(NUM_STATES, SS)
    print(f"Forma de P: {M.shape}")
    print(f"Suma de la fila 0 (debe ser 1.0): {M[0].sum():.1f}")
    print(f"Suma de la fila 97 (debe ser 1.0): {M[97].sum():.1f}")
    print(f"Suma de la fila 100 (debe ser 1.0): {M[100].sum():.1f}")
    print("-" * 30)
    
    # Vector de estado inicial v0 = [1, 0, 0, ...]
    v0 = np.zeros((1, NUM_STATES))
    v0[0, 0] = 1.0
    
    print("--- 2. Probabilidad después de k=25 movimientos ---")
    v_25 = calculate_prob_k_moves(M, v0, 25)
=======
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
    v2_25 = iterative_prob_k_steps(P, v0, 25)  # Just to compare times
>>>>>>> origin/main
    if v_25 is not None:
        prob_25 = v_25.flatten() # Transforms the 2D array into a 1D array, facilitating the iteration
        for i in range(N_States):
            # {i:3d} alingment of the numbers
            print(f"  Box {i:3d}: {prob_25[i]:.6%}")
        print(f"PROBABILITY OF HAVING WON: {prob_25[100]:.6%}")

<<<<<<< HEAD
    print("--- 3. Probabilidad después de k=50 movimientos ---")
    v_50 = calculate_prob_k_moves(M, v0, 50)
=======
    print("--- Probability of being in each box after 50 moves ---")
    v_50 = prob_k_steps(P, v0, 50)
    v2_50 = iterative_prob_k_steps(P, v0, 50)  # Just to compare times
>>>>>>> origin/main
    if v_50 is not None:
        prob_50 = v_50.flatten() 
        for i in range(N_States):
            print(f"  Box {i:3d}: {prob_50[i]:.6%}")
        print(f"PROBABILITY OF HAVING WON: {prob_50[100]:.6%}")
    print("-" * 30)
    print("-" * 30)

<<<<<<< HEAD
    print("--- 4. (Nota Completa) Número Esperado de Movimientos ---")
    movimientos_esperados = expected_moves(M)
    if movimientos_esperados is not None:
        print(f"El número esperado de movimientos para ganar el juego es:")
        print(f"==> {movimientos_esperados:.4f} movimientos")
=======
    print("---Expected number of moves ---")
    expected_moves_value = expected_moves(P)
    if expected_moves_value is not None:
        print(f"The average number of moves to expect to win is: {expected_moves_value:.4f}")
>>>>>>> origin/main
    print("-" * 30)


if __name__ == "__main__":
    main()