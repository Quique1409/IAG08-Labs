import metro
#creación de la clase Nodo
class Nodo():
    def __init__(self, nombre):
        self.nombre = nombre #es la forma de nombrar al nodo
        self.vecinos = [] #Lista para que se almacenen los vecinos de cada nodo
        self.color = "blanco"
        self.dist = -1
        self.padre = None
        self.f = -1        

    def AgregarVecinos(self, vecino):
        #verifica si no hay un vecino ya con ese nombre en algún vertice 
        if vecino != self.nombre and vecino not in self.vecinos: 
            self.vecinos.append(vecino) #Añadimos los vecinos a la lista de vecinos


#Creación de clase grafo
class Grafo():
    
    def __init__(self):
        self.vertices = {} #creamos el diccionario donde todos los nodos se guardaran
        self.padres = {} #Creamos el diccionario para que los padres se guarden

    def AgregarVertice(self, nombreNodo):
        if nombreNodo in self.vertices: #Si el nombre ya esta ocupado dentro del diccionario
            print(f"Ya existe el vecino pedido: {nombreNodo}") #Advertimos de su existencia y seguimos
        else:
            self.vertices[nombreNodo] = Nodo(nombreNodo) #De lo contrario creamos un nuevo nodo con el nombre dado

    def AgregarArista(self, nombreNodo1, nombreNodo2):
        if nombreNodo1 not in self.vertices: #Si el nombre 1 no es un vertice existente se advierte y seguimos
            print(f"El vertice {nombreNodo1} no esta definido")
        elif nombreNodo2 not in self.vertices: #Si el nombre 2 no es un vertice existente se advierte y seguimos
            print(f"El vertice {nombreNodo2} no esta definido")
        else: 
            #De lo contrario
            #Añadimos una arista entre el nodo1 y el nodo2 entre sí, añade cada uno a la lista de vecino del otro
            self.vertices[nombreNodo1].AgregarVecinos(self.vertices[nombreNodo2]) 
            self.vertices[nombreNodo2].AgregarVecinos(self.vertices[nombreNodo1])

    def Imprimir(self):
        for nodo in self.vertices.keys(): #Se recorre cada nodo en el diccionario de vertices
            cadena = nodo + " -> [" #Se imprime el nodo y empezamos un modo de impresión como arreglo
            for vecino in self.vertices[nodo].vecinos: #recorreremos cada vecino que tenga la lista de vecinos
                cadena += vecino.nombre + ", " #añadira cada vecino contenido en la lista de sus vecinos correspondientes en la cadena seguido de una coma
            print(cadena + "]") #Imprime la lista entera y al final cerramos el "arreglo"

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