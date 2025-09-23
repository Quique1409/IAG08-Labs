import metro
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


#Creación de clase grafo
class Grafo():
    
    def __init__(self):
        self.vertices = {} #creamos el diccionario donde todos los nodos se guardaran
        self.padres = {} #Creamos el diccionario para que los padres se guarden

    def AgregarVertice(self, nombreNodo):
        if nombreNodo in self.vertices: #Si el nombre ya esta ocupado dentro del diccionario
            print(f"Ya existe el vecino pedido: {nombreNodo}") #Advertimos de su existencia y seguimos (Creo que esto ya no es necesario)
        else:
            self.vertices[nombreNodo] = Nodo(nombreNodo) #De lo contrario creamos un nuevo nodo con el nombre dado

    def AgregarArista(self, nombreNodo1, nombreNodo2, distancia): 
        if nombreNodo1 not in self.vertices: #Si el nombre 1 no es un vertice existente se advierte y seguimos
            print(f"El vertice {nombreNodo1} no esta definido")
        elif nombreNodo2 not in self.vertices: #Si el nombre 2 no es un vertice existente se advierte y seguimos
            print(f"El vertice {nombreNodo2} no esta definido")
        else: 
            #De lo contrario
            #Añadimos una arista entre el nodo1 y el nodo2 entre sí, añade cada uno a la lista de vecino del otro
            self.vertices[nombreNodo1].AgregarVecinos(self.vertices[nombreNodo2], distancia) 
            self.vertices[nombreNodo2].AgregarVecinos(self.vertices[nombreNodo1], distancia)

    def Imprimir(self):
        """Se recorrer el nodo en el diccionario de vertices, de igual forma se añade cada vecino en la tupla contenida para mostrar al usuario el camino"""
        for nodo_nombre in self.vertices[nodo_nombre]:
            nodo = self.vertices[nodo_nombre]
            cadena = nodo.nombre + "-> ["
            for vecino, distancia in nodo.vecinos:
                cadena += f"{vecino.nombre}({distancia}m), "
            print(cadena.strip(", ")+"]")


    def A_star(self, NodoInicial, NodoFinal):
        """
        Heurística (h) es la estimación del costo desde un nodo hasta el final, en este caso se usa una h=0
        """
        self.padres.clear()
        def heuristica(n1, n2):
            return 0
        
        nodos_visitados = set()

        g_score = {nombre: float('inf') for nombre in self.vertices}
        g_score[NodoInicial] = 0


        f_score = {nombre: float('inf') for nombre in self.vertices}
        f_score[NodoInicial] = heuristica(self.vertices[NodoInicial], self.vertices[NodoFinal])

        prioridad = [(f_score[NodoInicial], NodoInicial)]

        while prioridad:
            _, nodo_actual = heapq.heappop(prioridad)
            if nodo_actual == NodoFinal:
                camino = []
                distancia_Total = g_score[NodoFinal]
                temp = NodoFinal
                while temp in self.padres:
                    camino.append(temp)
                    temp = self.padres[temp]
                camino.append(NodoInicial)
                camino.reverse()
                return camino, distancia_Total
            

        nodos_visitados.add(nodo_actual)
        nodo_actual = self.vertices[nodo_actual]

        for nodo_vecino, distancia in nodo_actual.vecinos:
            vecino_nombre = nodo_vecino.nombre
            if vecino_nombre in nodos_visitados:
                continue

            g_score_final = g_score[nodo_actual] + distancia

            if g_score_final < g_score[vecino_nombre]:
                self. padres[vecino_nombre] = nodo_actual
                g_score[vecino_nombre] = g_score_final
                f_score[vecino_nombre] = g_score_final + heuristica(nodo_vecino, self.vertices[NodoFinal])

                if (f_score[vecino_nombre], vecino_nombre) not in prioridad:
                    heapq.heappush(prioridad, (f_score[vecino_nombre], vecino_nombre))

        return None, float('inf')
    
    def EncontrarRutaAStar(self, NodoInicial, NodoFinal):
        print(f"\n\033[105m*\033[0mResultado del A* (Ruta más corta en distancia):")
        camino, distancia = self.A_star(NodoInicial, NodoFinal)
        if camino:
            print(f"Distancia total: {distancia / 1000:.2f} km")
            print(f"No. de estaciones: {len(camino)}")
            print(" -> ".join(camino))
        else:
            print(f"No se encontró una ruta de {NodoInicial} a {NodoFinal}")

    #Implementación del Breadth First Search
    def BFS(self, nombreNodo1):
        for u in self.vertices.values(): #A cada vertice se le pondrán valores desde cero
            u.color = "blanco"
            u.padre = None
            u.dist = 0
        #Comprobamos si el nodo pedido esta definido
        if nombreNodo1 not in self.vertices:
            print(f"El nodo {nombreNodo1} no está en el grafo.")
            return
        #Hacemos que el nodo sea accesible de esta forma
        nodoInicial = self.vertices[nombreNodo1]
        #Lo modificamos a gris pues lo estamos analizando
        nodoInicial.color = "gris"
        #Inicializamos su distancia en 0
        nodoInicial.dist = 0

        #Creamos una cola (o lista que la simula) y agregamos el nodo pedido
        Q = []
        Q.append(nodoInicial)

        #Mientras la cola tenga datos dentro
        while Q:
            #Sacamos un dato de la cola y analizamos
            u = Q.pop(0)
            for v in u.vecinos: #A cada vecino de u lo analizaremos
                if v.color == "blanco": #Si y solo si este es blanco
                    v.color = "gris" #Al entrar al if, lo analizamos y por ende le cambiamos el color a gris
                    v.dist = u.dist + 1 #Le añadimos un numero a la distancia, así cada vez nos iremos alejando más del nodo pedido
                    v.padre = u #El padre de v sea U, el valor sacado de la cola
                    self.padres[v.nombre] = u.nombre #Añadimos a V la información de que U es su padre en un diccionario
                    Q.append(v) #Añadimos V a la cola para ahora evaluarlo y sacar los datos de sus vecinos
            u.color = "negro" #Como ya evaluamos a U y obtuvimos todo lo necesario de él, lo marcamos como negro indicando que el proceso terminó

    def dfsVisitar(self, u, tiempo):
        u.dist = tiempo #La distancia se iguala al tiempo
        u.color = "gris" #En proceso de analisis 
        for v in u.vecinos: #Revisamos todos los vecinos de u 
            if v.color == "blanco": #mientras que los vecinos sean blancos se analizará
                v.padre = u #al vecino de u se le asigna que U es su padre
                tiempo = self.dfsVisitar(v, tiempo) #Se llama recursivamente a esta función para obtener el tiempo o distancia del vecino
                self.padres[v.nombre] = u.nombre #Se agrega al dicionario que U es padre de V
        u.color = "negro" #Una vez analizado se pone negro 
        tiempo = tiempo + 1  # Incrementa el tiempo después de visitar los vecinos.
        u.f = tiempo  
        return tiempo #regresamos tiempo

    def DFS(self, nombreNodoInicial):
        tiempo = 0 #Inicializamos el tiempo en 0
        for u in self.vertices.values(): #A cada vertice se le pondrán valores desde cero
            u.color = "blanco"
            u.padre = None
            u.dist = 0
        u = self.vertices[nombreNodoInicial] #A u se le dará el valor del vertice con el nombre recibido en DFS
        u.tiempo = self.dfsVisitar(u, tiempo) #Se llama a dfsVisitar para evaluar cada vertice y obtener distancias y padres entre si


    def EncontrarBFS(self, nombreNodoInicial, nombreNodoFinal):
        self.BFS(nombreNodoInicial)  # Llama al BFS para realizar el cálculo
        print("\n\033[105m*\033[0mResultado del BFS:")
        nodo = self.vertices[nombreNodoFinal] #Se le pasan los atributos a nodo con el vertice con el nombre de la estación final
        print(f"No. de estaciones: {nodo.dist+1}") #Se saca la distancia con el nodo final respecto al nodo inicial
        camino = [nombreNodoFinal] #Una lista a la que le agregaremos los vecinos y el mejor camino
        nodo_actual = nombreNodoFinal #Empezaremos del final al inicio 
        while nodo_actual != nombreNodoInicial: #Mientras que los nombres sean distintos, seguiremos iterando
        
            nodo_actual = self.padres[nodo_actual] #El nodo actual pasa a ser el padre de la estación final
            camino.append(nodo_actual) #Añadimos el padre a la lista del camino
        camino.reverse() #Una vez que todos los padres están en la lista, la revertimos para ir del inicio al final 
        print(camino) #imprimimos

    # Modifica el método EncontrarRuta para utilizar DFS
    def EncontrarRutaDFS(self, nombreNodoInicial, nombreNodoFinal):
        self.DFS(nombreNodoInicial)  # Realiza un DFS desde el nodo inicial
        print("\n\033[105m*\033[0mResultado del DFS: ")
        #nodo = self.vertices[nombreNodoFinal] #
        camino = [nombreNodoFinal] # Se crea una lista que muestre las estaciones del camino
        nodo_actual = nombreNodoFinal #La lista irá de la estación final hasta el inicio

        while nodo_actual != nombreNodoInicial: #Se repetira hasta que se llegue a la estación inicial
            padre = self.padres[nodo_actual] #Obtenemos el padre del nodo actual
            camino.append(padre) #Añadiremos cada padre a la lista formando poco a poco el camino
            nodo_actual = padre #Ahora el nodo actual es el padre puesto en la lista

        print(f"No. de estaciones: {len(camino)}") #En este caso enumeraremos con la longitud de la lista
        camino.reverse() #Se invierten los valores, ahora la tabla va del inicio al final
        print(camino)


grafo = Grafo()
#Función para que se añada cada elemento de las listas del metro
for index in range (0,12): #Se iterara tantas veces como lineas del metro hay
    nlinea = len(metro.lineas[index]) #Se obtiene la longitud de cada linea 
    for i in range(0, nlinea): #Se repetira a lo largo de la longitud de cada linea
        elemento = metro.lineas[index][i] #Agarraremos cada valor de cada linea individualmente 
        grafo.AgregarVertice(f"{elemento}") #Se añaden elemento por elemento cada vertice al grafo

#Creamos las aristas (conexiones entre cada vertice)
for index in range(0, 12): #Iteramos sobre cada una de las 12 lineas del metro
    nlinea = len(metro.lineas[index]) #Obtendremos la longitud de cada linea 
    for i in range(0, nlinea-1): #Iteraremos sobre la longitud del cada línea
        ant = metro.lineas[index][i] #Se obtiene el nombre de una estación
        sig = metro.lineas[index][i+1] #Se obtiene el nombre de la siguiente estación
        grafo.AgregarArista(f"{ant}", f"{sig}")  #Se crea la arista entre esas dos estaciones

#Ruta 1
estacionInicial1 = "San Antonio"
estacionFinal1 = "Aragón"

#Ruta 2
estacionInicial2 = "Aquiles Serdán"
estacionFinal2 = "Iztapalapa"

#Ruta 3
estacionInicial3 = "Vallejo"
estacionFinal3 = "Insurgentes"

#Encontramos los caminos en la ruta 1 con BFS y DFS
print(f"\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial1.upper()} a {estacionFinal1.upper()}")
grafo.EncontrarBFS(estacionInicial1, estacionFinal1)
grafo.EncontrarRutaDFS(estacionInicial1, estacionFinal1)
print("\nFeliz viaje!\n-----------------------")

#Encontramos los caminos en la ruta 2 con BFS y DFS
print(f"\n\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial2.upper()} a {estacionFinal2.upper()}")
grafo.EncontrarBFS(estacionInicial2, estacionFinal2)
grafo.EncontrarRutaDFS(estacionInicial2, estacionFinal2)
print("\nFeliz viaje!\n-----------------------")

#Encontramos los caminos en la ruta 3 con BFS y DFS
print(f"\n\n\033[0m\033[104m* Ruta de:\033[0m {estacionInicial3.upper()} a {estacionFinal3.upper()}")
grafo.EncontrarBFS(estacionInicial3, estacionFinal3)
grafo.EncontrarRutaDFS(estacionInicial3, estacionFinal3)
print("\nFeliz viaje!\n-----------------------")