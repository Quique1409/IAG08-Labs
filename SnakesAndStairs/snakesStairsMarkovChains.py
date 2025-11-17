import numpy as np

# Configurar numpy para imprimir de forma más legible
np.set_printoptions(precision=4, suppress=True)

# --- 1. Definición del Tablero y Estados ---

N_ESTADOS = 101  # Estados del 0 (inicio) al 100 (victoria)
N_CARAS = 6
PROB_DADO = 1.0 / N_CARAS

# Mapeo de serpientes y escaleras (tablero estándar)
# Si aterrizas en 'llave', te mueves instantáneamente a 'valor'
mapa_saltos = {
    # Escaleras
    1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100,
    # Serpientes
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78,
}

# --- 2. Construir la Matriz de Transición (P) ---

# Inicializar la matriz P (101x101) con ceros
P = np.zeros((N_ESTADOS, N_ESTADOS))

# Rellenar la matriz para los estados transitorios (0 a 99)
for i in range(N_ESTADOS - 1):  # i = estado actual (0 a 99)
    for dado in range(1, N_CARAS + 1):  # j = tirada del dado (1 a 6)
        
        destino_temp = i + dado
        
        # Aplicar reglas del juego
        if destino_temp > 100:
            # Regla "Overshoot": te quedas en la casilla actual
            destino_final = i
        elif destino_temp in mapa_saltos:
            # Caíste en una serpiente o escalera
            destino_final = mapa_saltos[destino_temp]
        else:
            # Movimiento normal
            destino_final = destino_temp
            
        # Añadir la probabilidad (1/6) a la celda correspondiente
        P[i, destino_final] += PROB_DADO

# Definir el estado absorbente (Victoria)
# Si llegas a 100, te quedas en 100 (P_100,100 = 1)
P[100, 100] = 1.0

print("--- Matriz de Transición P (dimensiones) ---")
print(f"Forma de P: {P.shape}")
print(f"Fila 0 (inicio): {P[0, :40]}...") # Muestra el inicio
print(f"Fila 97 (cerca del final): {P[97, 70:]}...") # Muestra el final
print("-" * 30)


# --- 3. Probabilidad después de k movimientos (v_k = v_0 * P^k) ---

# Vector de estado inicial v0 = [1, 0, 0, ...]
# (Empiezas en el estado 0 con probabilidad 1)
v0 = np.zeros((1, N_ESTADOS))
v0[0, 0] = 1.0

# Calcular P^25 y P^50 usando el poder de matriz de numpy
# (Esto es mucho más eficiente que multiplicar en bucle)
try:
    P_25 = np.linalg.matrix_power(P, 25)
    P_50 = np.linalg.matrix_power(P, 50)
except np.linalg.LinAlgError as e:
    print(f"Error al calcular la potencia de la matriz: {e}")
    # En caso de error, salimos o manejamos
    P_25 = np.zeros_like(P)
    P_50 = np.zeros_like(P)

# Calcular la distribución de probabilidad v_k = v0 @ P^k
v_25 = v0 @ P_25
v_50 = v0 @ P_50

print("--- Probabilidad después de 25 movimientos (v_25) ---")
print(f"Prob. de estar en la casilla 14 (escalera): {v_25[0, 14]:.4%}")
print(f"Prob. de estar en la casilla 53 (serpiente): {v_25[0, 53]:.4%}")
print(f"Prob. de estar en la casilla 99: {v_25[0, 99]:.4%}")
print(f"PROBABILIDAD DE HABER GANADO (Estado 100): {v_25[0, 100]:.4%}")
print("-" * 30)

print("--- Probabilidad después de 50 movimientos (v_50) ---")
print(f"Prob. de estar en la casilla 14 (escalera): {v_50[0, 14]:.4%}")
print(f"Prob. de estar en la casilla 53 (serpiente): {v_50[0, 53]:.4%}")
print(f"Prob. de estar en la casilla 99: {v_50[0, 99]:.4%}")
print(f"PROBABILIDAD DE HABER GANADO (Estado 100): {v_50[0, 100]:.4%}")
print("-" * 30)


# --- 4. (Nota Completa) Número Esperado de Movimientos para Ganar ---

# Reordenamos la matriz P en la forma canónica:
# P = | Q  R |
#     | 0  I |

# Q = Transiciones entre estados transitorios (0-99)
# Es una submatriz de 100x100
Q = P[0:100, 0:100]

# I = Matriz identidad (100x100)
I = np.identity(100)

# N = Matriz Fundamental (I - Q)^-1
# Esta es la parte computacionalmente más pesada
try:
    # N = (I - Q)^-1
    N = np.linalg.inv(I - Q)
except np.linalg.LinAlgError as e:
    print(f"Error al invertir la matriz (I-Q): {e}")
    N = np.zeros((100, 100)) # Placeholder si falla

# t = Vector de tiempos esperados de absorción
# t = N * 1 (donde 1 es un vector columna de unos)
ones_vector = np.ones((100, 1))
t = N @ ones_vector

# El resultado que buscamos es el tiempo esperado empezando desde
# el estado 0 (la primera fila de t)
movimientos_esperados = t[0, 0]

print("--- Número Esperado de Movimientos (Nota Completa) ---")
print(f"El número esperado de movimientos para ganar el juego (E[T] desde el estado 0) es:")
print(f"==> {movimientos_esperados:.4f} movimientos")
print("-" * 30)