import numpy as np
import time  # Para medir el tiempo, es interesante ver cuánto tarda N

# Configurar numpy para imprimir de forma más legible
np.set_printoptions(precision=4, suppress=True)

# --- 1. Constantes y Definición del Tablero ---

N_ESTADOS = 101  # Estados del 0 (inicio) al 100 (victoria)
N_CARAS = 6
PROB_DADO = 1.0 / N_CARAS

def obtener_mapa_saltos():
    """
    Define y devuelve el mapeo de serpientes y escaleras.
    Si aterrizas en 'llave', te mueves instantáneamente a 'valor'.
    """
    mapa_saltos = {
        # Escaleras
        1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100,
        # Serpientes
        16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78,
    }
    return mapa_saltos

# --- 2. Lógica de la Cadena de Markov (en funciones) ---

def crear_matriz_transicion(n_estados, n_caras, mapa_saltos):
    """
    Construye la matriz de transición P (101x101) basada
    en las reglas del juego.
    """
    P = np.zeros((n_estados, n_estados))
    prob_dado = 1.0 / n_caras

    # Rellenar la matriz para los estados transitorios (0 a 99)
    for i in range(n_estados - 1):  # i = estado actual (0 a 99)
        for dado in range(1, n_caras + 1):  # j = tirada del dado (1 a 6)
            
            destino_temp = i + dado
            
            # --- Inicio de la Lógica de Reglas (Tu lógica) ---
            if destino_temp > 100:
                # Regla "Overshoot": te quedas en la casilla actual
                destino_final = i
            elif destino_temp in mapa_saltos:
                # Caíste en una serpiente o escalera
                destino_final = mapa_saltos[destino_temp]
            else:
                # Movimiento normal
                destino_final = destino_temp
            # --- Fin de la Lógica de Reglas ---
                
            # Añadir la probabilidad (1/6) a la celda correspondiente
            P[i, destino_final] += prob_dado

    # Definir el estado absorbente (Victoria)
    # Si llegas a 100, te quedas en 100 (P_100,100 = 1)
    P[100, 100] = 1.0
    
    return P

def calcular_prob_k_pasos(P, v0, k):
    """
    Calcula la distribución de probabilidad v_k = v0 * P^k
    """
    try:
        P_k = np.linalg.matrix_power(P, k)
        v_k = v0 @ P_k
        return v_k
    except np.linalg.LinAlgError as e:
        print(f"Error al calcular P^{k}: {e}")
        return None

def calcular_movimientos_esperados(P):
    """
    Calcula el número esperado de movimientos para ganar
    usando la Matriz Fundamental N = (I - Q)^-1
    """
    # Q = Transiciones entre estados transitorios (0-99)
    # (Tomamos N_ESTADOS-1 para ser genéricos, o sea, 100)
    transient_states = N_ESTADOS - 1
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
    movimientos_esperados = t[0, 0]
    return movimientos_esperados


# --- 3. Ejecución Principal (main) ---

def main():
    print("--- 1. Construyendo Matriz de Transición P ---")
    mapa = obtener_mapa_saltos()
    P = crear_matriz_transicion(N_ESTADOS, N_CARAS, mapa)
    print(f"Forma de P: {P.shape}")
    print(f"Suma de la fila 0 (debe ser 1.0): {P[0].sum():.1f}")
    print(f"Suma de la fila 97 (debe ser 1.0): {P[97].sum():.1f}")
    print(f"Suma de la fila 100 (debe ser 1.0): {P[100].sum():.1f}")
    print("-" * 30)
    
    # Vector de estado inicial v0 = [1, 0, 0, ...]
    v0 = np.zeros((1, N_ESTADOS))
    v0[0, 0] = 1.0
    
    print("--- 2. Probabilidad después de k=25 movimientos ---")
    v_25 = calcular_prob_k_pasos(P, v0, 25)
    if v_25 is not None:
        print(f"Prob. de estar en la casilla 14: {v_25[0, 14]:.4%}")
        print(f"Prob. de estar en la casilla 53: {v_25[0, 53]:.4%}")
        print(f"Prob. de estar en la casilla 99: {v_25[0, 99]:.4%}")
        print(f"PROBABILIDAD DE HABER GANADO: {v_25[0, 100]:.4%}")
    print("-" * 30)

    print("--- 3. Probabilidad después de k=50 movimientos ---")
    v_50 = calcular_prob_k_pasos(P, v0, 50)
    if v_50 is not None:
        print(f"Prob. de estar en la casilla 14: {v_50[0, 14]:.4%}")
        print(f"Prob. de estar en la casilla 53: {v_50[0, 53]:.4%}")
        print(f"Prob. de estar en la casilla 99: {v_50[0, 99]:.4%}")
        print(f"PROBABILIDAD DE HABER GANADO: {v_50[0, 100]:.4%}")
    print("-" * 30)

    print("--- 4. (Nota Completa) Número Esperado de Movimientos ---")
    movimientos_esperados = calcular_movimientos_esperados(P)
    if movimientos_esperados is not None:
        print(f"El número esperado de movimientos para ganar el juego es:")
        print(f"==> {movimientos_esperados:.4f} movimientos")
    print("-" * 30)


if __name__ == "__main__":
    main()