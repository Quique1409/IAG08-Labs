import lines 
import coordinates
import heapq
import math

# La clase Nodo no requiere cambios.
class Nodo():
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = []
        self.color = "blanco"
        self.dist = -1
        self.padre = None
        self.f = -1       

    def AgregarVecinos(self, vecino, distancia):
        if vecino != self.nombre and vecino not in self.vecinos: 
            self.vecinos.append((vecino, distancia))

class Grafo:
    def __init__(self):
        self.vertices = {}

    # ESTE ES EL MÉTODO DE CONSTRUCCIÓN CORRECTO Y DEFINITIVO.
    # Fusiona las conexiones de los transbordos en lugar de sobrescribirlas.
    def construir_grafo_desde_datos(self, datos_lineas):
        for estaciones in datos_lineas.values():
            for nombre_estacion, datos_estacion in estaciones.items():
                # Si la estación es nueva, la creamos en el grafo.
                if nombre_estacion not in self.vertices:
                    self.vertices[nombre_estacion] = {"neighbors": []}
                
                # Obtenemos los nombres de los vecinos que ya tiene para no duplicarlos.
                vecinos_existentes = {vecino[0] for vecino in self.vertices[nombre_estacion]["neighbors"]}

                # Agregamos los nuevos vecinos de la línea actual SOLO SI NO EXISTEN previamente.
                for vecino, distancia in datos_estacion.get("neighbors", []):
                    if vecino not in vecinos_existentes:
                        self.vertices[nombre_estacion]["neighbors"].append((vecino, distancia))

    def A_star(self, NodoInicial, NodoFinal):
        """
        Algoritmo A* que utiliza la heurística de Haversine con las coordenadas importadas.
        """
        def haversine(coord1, coord2):
            R = 6371000  # Radio de la Tierra en metros
            lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
            lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c

        def heuristica(n1, n2):
            """Busca las coordenadas en el archivo coordinates.py e invoca a haversine."""
            coord1 = coordinates.station_coordinates.get(n1)
            coord2 = coordinates.station_coordinates.get(n2)
            if coord1 and coord2:
                return haversine(coord1, coord2)
            return 0 # Fallback si alguna coordenada no se encuentra

        padres = {} # Diccionario local para esta búsqueda
        g_score = {nombre: float('inf') for nombre in self.vertices}
        g_score[NodoInicial] = 0
        f_score = {nombre: float('inf') for nombre in self.vertices}
        f_score[NodoInicial] = heuristica(NodoInicial, NodoFinal)
        prioridad = [(f_score[NodoInicial], NodoInicial)]

        while prioridad:
            f_actual, nodo_actual_nombre = heapq.heappop(prioridad)

            if nodo_actual_nombre == NodoFinal:
                camino = []
                distancia_Total = g_score[NodoFinal]
                temp = NodoFinal
                while temp in padres:
                    camino.append(temp)
                    temp = padres[temp]
                camino.append(NodoInicial)
                camino.reverse()
                return camino, distancia_Total
            
            if f_actual > f_score[nodo_actual_nombre]:
                continue

            for vecino_nombre, distancia in self.vertices[nodo_actual_nombre].get("neighbors", []):
                g_score_final = g_score[nodo_actual_nombre] + distancia
                
                if g_score_final < g_score.get(vecino_nombre, float('inf')):
                    padres[vecino_nombre] = nodo_actual_nombre
                    g_score[vecino_nombre] = g_score_final
                    f_score[vecino_nombre] = g_score_final + heuristica(vecino_nombre, NodoFinal)
                    heapq.heappush(prioridad, (f_score[vecino_nombre], vecino_nombre))
        
        return None, float('inf')
    
    def EncontrarRutaAStar(self, NodoInicial, NodoFinal):
        print(f"\n\033[105m*\033[0m Resultado del A* (Ruta más corta en distancia):")
        if NodoInicial not in self.vertices or NodoFinal not in self.vertices:
            print(f"Una o ambas estaciones ('{NodoInicial}' o '{NodoFinal}') no se encontraron en la red del metro.")
            return

        camino, distancia = self.A_star(NodoInicial, NodoFinal)
        if camino:
            print(f"Distancia total: {distancia / 1000:.2f} km")
            print(f"No. de estaciones: {len(camino)}")
            print(" -> ".join(camino))
        else:
            print(f"No se encontró una ruta de {NodoInicial} a {NodoFinal}")

# ==============================================================================
# EJECUCIÓN DEL PROGRAMA
# ==============================================================================

# 1. Crear la instancia del grafo
metro_cdmx = Grafo()
 
# 2. Construir el grafo unificado usando el método corregido
metro_cdmx.construir_grafo_desde_datos(lines.lineas_with_data)

# --- Rutas de prueba ---

# Ruta 1
estacionInicial1 = "San Antonio"
estacionFinal1 = "Aragón"
print(f"\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial1.upper()} a {estacionFinal1.upper()}")
metro_cdmx.EncontrarRutaAStar(estacionInicial1, estacionFinal1)
print("\n¡Feliz viaje!\n-----------------------")

# Ruta 2
estacionInicial2 = "Aragón"
estacionFinal2 = "San Antonio"
print(f"\n\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial2.upper()} a {estacionFinal2.upper()}")
metro_cdmx.EncontrarRutaAStar(estacionInicial2, estacionFinal2)
print("\n¡Feliz viaje!\n-----------------------")

# Ruta 3
estacionInicial3 = "San Antonio"
estacionFinal3 = "Aragón"
print(f"\n\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial3.upper()} a {estacionFinal3.upper()}")
metro_cdmx.EncontrarRutaAStar(estacionInicial3, estacionFinal3)
print("\n¡Feliz viaje!\n-----------------------")

# Ruta 4 (Prueba de simetría)
estacionInicial4 = "Aragón"
estacionFinal4 = "San Antonio"
print(f"\n\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial4.upper()} a {estacionFinal4.upper()}")
metro_cdmx.EncontrarRutaAStar(estacionInicial4, estacionFinal4)
print("\n¡Feliz viaje!\n-----------------------")