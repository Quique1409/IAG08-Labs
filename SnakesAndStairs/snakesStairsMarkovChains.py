import numpy as np
import time  # Para medir el tiempo, es interesante ver cuánto tarda N

# Configurar numpy para imprimir de forma más legible
np.set_printoptions(precision=4, suppress=True)

# --- 1. Constantes y Definición del Tablero ---

NUM_STATES = 101  # Estados del 0 al 80
NUM_FACES = 6
PROB_DADO = 1.0 / NUM_FACES

def get_jump_map():
    #map for snakes and stairs
    jump_map = {
        # Stairs
        3: 19, 7:33, 22: 58, 40:59, 48: 85, 56: 79, 69: 87, 80: 9,
        # Snakes
        96: 58, 89: 47, 80: 39, 66: 1, 44: 26, 52: 49, 37: 18, 47: 9
    }
    return jump_map

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
    
    return M #we return the transition matrix

def calculate_prob_k_moves(M, v0, k):
    """
    #calculate the probability distribution after k steps
    # M: transition matrix 
    # v0: initial state vector
    # k: number of steps"""
    try:
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
    Q = P[0:transient_states, 0:transient_states]
    
    # I = Matriz identidad (100x100)
    I = np.identity(transient_states)
    
    try:
        # N = (I - Q)^-1
        start_time = time.time()
        N = np.linalg.inv(I - Q)
        end_time = time.time()
        print(f"(Cálculo de N=(I-Q)^-1 tomó {end_time - start_time:.4f}s)")
        
    except np.linalg.LinAlgError as e:
        print(f"Error al invertir la matriz (I-Q): {e}")
        return None

    # t = N * 1 (vector columna de unos)
    ones_vector = np.ones((transient_states, 1))
    t = N @ ones_vector
    
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
    if v_25 is not None:
        print(f"Prob. de estar en la casilla 14: {v_25[0, 14]:.4%}")
        print(f"Prob. de estar en la casilla 53: {v_25[0, 53]:.4%}")
        print(f"Prob. de estar en la casilla 99: {v_25[0, 99]:.4%}")
        print(f"PROBABILIDAD DE HABER GANADO: {v_25[0, 100]:.4%}")
    print("-" * 30)

    print("--- 3. Probabilidad después de k=50 movimientos ---")
    v_50 = calculate_prob_k_moves(M, v0, 50)
    if v_50 is not None:
        print(f"Prob. de estar en la casilla 14: {v_50[0, 14]:.4%}")
        print(f"Prob. de estar en la casilla 53: {v_50[0, 53]:.4%}")
        print(f"Prob. de estar en la casilla 99: {v_50[0, 99]:.4%}")
        print(f"PROBABILIDAD DE HABER GANADO: {v_50[0, 100]:.4%}")
    print("-" * 30)

    print("--- 4. (Nota Completa) Número Esperado de Movimientos ---")
    movimientos_esperados = expected_moves(M)
    if movimientos_esperados is not None:
        print(f"El número esperado de movimientos para ganar el juego es:")
        print(f"==> {movimientos_esperados:.4f} movimientos")
    print("-" * 30)


if __name__ == "__main__":
    main()