import lines 
import heapq #Cola de prioridad
#creación de la clase Nodo
class Nodo():
    def __init__(self, nombre):
        self.nombre = nombre #es la forma de nombrar al nodo
        self.vecinos = [] #Lista para que se almacenen los vecinos de cada nodo
        self.color = "blanco"
        self.dist = -1
        self.padre = None
        self.f = -1        

    def AgregarVecinos(self, vecino, distancia):
        #verifica si no hay un vecino ya con ese nombre en algún vertice 
        if vecino != self.nombre and vecino not in self.vecinos: 
            self.vecinos.append((vecino, distancia)) #Añadimos la tupla con los vecinos y la distancia



class Grafo:
    def __init__(self):
        self.vertices = {}
        self.padres = {}

    def AgregarVertice(self, nombre_estacion, datos_estacion):
        self.vertices[nombre_estacion] = datos_estacion

    def A_star(self, NodoInicial, NodoFinal):
        def heuristica(n1, n2):
            return 0  # Heurística simple, ya que no se tienen coordenadas

        self.padres.clear()
        
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
                while temp in self.padres:
                    camino.append(temp)
                    temp = self.padres[temp]
                camino.append(NodoInicial)
                camino.reverse()
                return camino, distancia_Total

            for vecino_nombre, distancia in self.vertices[nodo_actual_nombre]["neighbors"]:
                g_score_final = g_score[nodo_actual_nombre] + distancia
                
                if g_score_final < g_score.get(vecino_nombre, float('inf')):
                    self.padres[vecino_nombre] = nodo_actual_nombre
                    g_score[vecino_nombre] = g_score_final
                    f_score[vecino_nombre] = g_score_final + heuristica(vecino_nombre, NodoFinal)
                    heapq.heappush(prioridad, (f_score[vecino_nombre], vecino_nombre))
        
        return None, float('inf')
    
    def EncontrarRutaAStar(self, NodoInicial, NodoFinal):
        print(f"\n\033[105m*\033[0mResultado del A* (Ruta más corta en distancia):")
        if NodoInicial not in self.vertices or NodoFinal not in self.vertices:
            print(f"Una o ambas estaciones no se encontraron en la red del metro.")
            return

        camino, distancia = self.A_star(NodoInicial, NodoFinal)
        if camino:
            print(f"Distancia total: {distancia / 1000:.2f} km")
            print(f"No. de estaciones: {len(camino)}")
            print(" -> ".join(camino))
        else:
            print(f"No se encontró una ruta de {NodoInicial} a {NodoFinal}")


# -------------------------------------------------------------
# Nueva y correcta construcción del grafo
# -------------------------------------------------------------
grafo = Grafo()
  
# Añadir todos los vértices al grafo
for line_data in lines.lineas_with_data.values():
    for station_name, station_info in line_data.items():
        if station_name not in grafo.vertices:
            grafo.AgregarVertice(station_name, station_info)


# 2. Después, poblamos la lista de vecinos para cada estación
for line_data in lines.lineas_with_data.values():
    for station_name, station_info in line_data.items():
        # Obtenemos la lista de vecinos actuales del grafo
        vecinos_actuales = grafo.vertices[station_name]["neighbors"]
        # Agregamos los nuevos vecinos solo si no están ya en la lista
        for vecino, distancia in station_info["neighbors"]:
            if (vecino, distancia) not in vecinos_actuales:
                vecinos_actuales.append((vecino, distancia))

# Las aristas se añaden automáticamente a través de la estructura 'neighbors'
# en el diccionario 'lineas_with_data', por lo que no es necesario un bucle de aristas separado.



#Ruta 1
estacionInicial1 = "San Antonio"
estacionFinal1 = "Aragón"

#Ruta 2
estacionInicial2 = "San Joaquín"
estacionFinal2 = "Universidad"

#Ruta 3
estacionInicial3 = "Universidad"
estacionFinal3 = "San Joaquín"

#Encontramos los caminos en la ruta 1 con A*
print(f"\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial1.upper()} a {estacionFinal1.upper()}")
grafo.EncontrarRutaAStar(estacionInicial1, estacionFinal1)
print("\nFeliz viaje!\n-----------------------")

#Encontramos los caminos en la ruta 2 con A*
print(f"\n\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial2.upper()} a {estacionFinal2.upper()}")
grafo.EncontrarRutaAStar(estacionInicial2, estacionFinal2)
print("\nFeliz viaje!\n-----------------------")

#Encontramos los caminos en la ruta 3 con A*
print(f"\n\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial3.upper()} a {estacionFinal3.upper()}")
grafo.EncontrarRutaAStar(estacionInicial3, estacionFinal3)
print("\nFeliz viaje!\n-----------------------")