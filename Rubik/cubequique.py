from abc import ABC, abstractmethod
import time

class EstadoProblema:
    """
    La clase EstadoProblema es abstracta.
    Representa un estado o configuración del problema a resolver.
    
    Es una interfaz simplificada para utilizarse
    en los algoritmos de búsqueda del curso.
    
    Al definir un problema particular hay que implementar los métodos
    abstractos
    """
    
    @abstractmethod
    def expand():
        """
        :return: el conjunto de estados sucesores
        """
        pass
    
    @abstractmethod
    def get_depth():
        """
        :return: la profundidad del estado
        """
        pass
        
    @abstractmethod
    def get_parent():
        """
        :return: referencia al estado predecesor o padre
        """
        pass
    
from functools import reduce
import random    

# La secuencia del 0 al 15
# 0 representará el espacio en blanco
seq = list(range(0,16))

# Cuatro posibles acciones para nuestro agente
# Mover una ficha en dirección: 
# izquierda (E), derecha (W), arriba (N), o abajo (S)
actions = ['E','W','N','S']

# Representaremos las configuraciones con bits
# Definimos algunas funciones útiles
# Recorre un bloque de 4 bits de unos a la posición i
x_mask = lambda i: 15<<(4*i)

# Extrae los cuatro bits que están en la posción i
# en la configuración c
# El rompecabezas tiene 16 posiciones (16X4 = 64 bits)
extract = lambda i,c: (c&(x_mask(i)))>>(4*i)

# Verifica si la posición z es la última columna
e_most = lambda z: (z%4)==3

# Verifica si la posición z es la primera columna
w_most = lambda z: (z%4)==0

# Verifica si la posición z es el primer renglón
n_most = lambda z: z<=3

# Verifica si la posición z es el último renglón
s_most = lambda z:z>=12

# Establecemos un diccionario con las acciones posibles
# para cada posición del rompecabezas
valid_moves = {i:list(filter(lambda action:\
((not action=='E') or (not e_most(i))) and \
((not action=='W') or (not w_most(i))) and \
((not action=='S') or (not s_most(i))) and \
((not action=='N') or (not n_most(i))),actions)) for i in seq}

# Realiza el movimiento hacía la izquierda
def move_east(puzzle):
    """
    :param puzzle: el rompecabezas
    """
    if(not e_most(puzzle.zero)):
        puzzle.zero += 1;
        mask = x_mask(puzzle.zero)
        puzzle.configuration = \
        (puzzle.configuration&mask)>>4 | \
        (puzzle.configuration&~mask)

# Realiza el movimiento hacía la derecha
def move_west(puzzle):
    if(not w_most(puzzle.zero)):
        puzzle.zero -= 1;
        mask = x_mask(puzzle.zero)
        puzzle.configuration = \
        (puzzle.configuration&mask)<<4 | \
        (puzzle.configuration&~mask)

# Realiza el movimiento hacía arriba
def move_north(puzzle):
    if(not n_most(puzzle.zero)):
        puzzle.zero -= 4;
        mask = x_mask(puzzle.zero)
        puzzle.configuration = \
        (puzzle.configuration&mask)<<16 | \
        (puzzle.configuration&~mask)

# Realiza el movimiento hacía abajo
def move_south(puzzle):
    if(not s_most(puzzle.zero)):
        puzzle.zero += 4;
        mask = x_mask(puzzle.zero)
        puzzle.configuration = \
        (puzzle.configuration&mask)>>16 | \
        (puzzle.configuration&~mask)

class Puzzle(EstadoProblema):
    """
    Rompecabezas del 15
    """
    
    
    def __init__(self, parent=None, action =None, depth=0):
        """
        Puede crearse un rompecabezas ordenado al no especificar
        parámetros del constructor.
        También se puede crear una nueva configuración a 
        partir de una configuración dada en parent.
        :param parent: configuración de referencia.
        :param action: la acción que se aplica a parent para
        generar la configuración sucesora.
        :depth la profundidad del estado a crear
        """
        self.parent = parent
        self.depth = depth
        if(parent == None):
            self.configuration =  \
                reduce(lambda x,y: x | (y << 4*(y-1)), seq)
            # posición del cero
            self.zero = 15
        else:
            self.configuration = parent.configuration
            self.zero = parent.zero
            if(action != None):
                self.move(action)

    def __str__(self):
        """
        :return: un string que representa 
        la configuración del rompecabezas
        """
        return '\n'+''.join(list(map(lambda i:\
        format(extract(i,self.configuration)," x")+\
        ('\n' if (i+1)%4==0 else ''),seq)))+'\n'

    def __repr__(self):
        """
        :return: representación texto de la configuración
        """
        return self.__str__()

    def __eq__(self,other):
        """
        :param other: la otra configuración con la que se comparará
        el objeto
        :return: verdadero cuando el objeto y el parámetro
        tienen la misma configuración.
        """
        return (isinstance(other, self.__class__)) and \
        (self.configuration==other.configuration)

    def __ne__(self,other):
        """
        :param other: la otra configuración con la que se comparará
        el objeto
        :return: verdadero cuando el objeto y el parámetro
        no tienen la misma configuración
        """
        return not self.__eq__(other)
        
    def __lt__(self,other):
        """
        :param other: la otra configuración con la que se comparará
        el objeto
        :return: verdadero cuando la profundidad del objeto
        es menor que la del argumento
        """
        return self.depth < other.depth

    def __hash__(self):
        """
        :return: un número hash para poder usar la configuración en 
        un diccionario, delegamos al hash de un entero
        """
        return hash(self.configuration)

    def move(self,action):
        """
        Realiza un movimiento de ficha.
        Debemos imaginar que el espacio se mueve en la dirección
        especificada por acción
        :param action: la acción a realizar
        """
        if(action =='E'):
            move_east(self)
        if(action =='W'):
            move_west(self)
        if(action =='N'):
            move_north(self)
        if(action =='S'):
            move_south(self)
        return self


    @staticmethod
    def to_list(puzzle):
        """
        Convertimos la configuración a una lista de números
        :param puzzle: la configuración a convertir
        :return la lista con enteros
        """
        return [extract(i,puzzle.configuration) for i in seq]

    def shuffle(self,n):
        """
        Desordena de manera aleatoria el rompecabezas.
        :param n: el número de movimientos aleatorios a aplicar
        """
        for i in range(0,n):
            self.move(random.choice(valid_moves[self.zero]))
        return self

    def expand(self):
        """
        Los sucesores del estado, quitamos el estado padre
        """
        #filtering the path back to parent
        return list(filter(lambda x: \
        (x!=self.parent), \
        [Puzzle(self,action,self.depth+1) \
        for action in valid_moves[self.zero]]))
    
    def get_depth(self):
        """
        :return: la profundidad del estado
        """
        return self.depth
    
    def get_parent(self):
        """
        :return: el nodo predecesor (padre) del estado 
        """
        return self.parent
# Ejemplo del método to_list
# Creamos un rompecabezas ordenado
ordenado = Puzzle()
print("rompecabezas ordenado:",ordenado)
lista_ordenada = Puzzle.to_list(ordenado)
print("el rompecabezas ordenado como una lista:\n",lista_ordenada)

# Si desordenamos el rompecabezas su lista ya no estará ordenada
from random import seed
seed(2019)
desordenado = Puzzle()
desordenado.shuffle(5)
print("rompecabezas desordenado:",desordenado)
lista_desordenada = Puzzle.to_list(desordenado)
print("el rompecabezas desordenado como una lista:\n",lista_desordenada)

def h1(p_1,p_2):
    # cuenta el número de fichas que no están en orden
    return sum(1 \
    for a,b in zip(Puzzle.to_list(p_1),Puzzle.to_list(p_2)) if a!=b)
print("ordenado:",ordenado)
print("desordenado:",desordenado)
print("número de fichas fuera de lugar:",h1(ordenado,desordenado))

from collections import deque

# trajectory nos regresará la trayectoria a partir de un estado
def trajectory(end):
    # nos valemos de un deque para almacenar la ruta
    sequence = deque()
    # agregamos el estado final o meta
    sequence.append(end)
    # nos vamos regresando al estado predecesor mientras este exista
    while end.get_parent():
        # nos movemos al predecesor
        end = end.get_parent()
        # lo agregamos a la lista
        sequence.append(end)
    # invertimos el orden de la secuencia
    sequence.reverse()
    # lo regresamos como una lista
    return list(sequence)

import heapq

class AStar:
    """
    Implementación del algoritmo A*
    """
    @staticmethod
    def search(origen,stop,g,h):
        """
        Búsqueda informada A*
        :param origen: estado inicial
        :param stop: función de paro, verdadera para el estado meta
        :param g: función de costo acumulado
        :param h: función heurística, costo estimado a la meta
        """
        # Nuestra cola de prioridad
        agenda = []
        # Conjunto de estados expandidos
        expandidos = set()
        # Condición trivial
        if stop(origen):
            return trajectory(origen)
        
        # Estado inicial a la cola de prioridad
        # La prioridad será f(s) = g(s) + h(s), 
        # para s una configuración
        f = lambda s: g(s) + h(s)
        
        # Agregamos el origen a la agenda
        heapq.heappush(agenda,(f(origen),origen))
        
        # Mientras la agenda no este vacía
        while agenda:
            # El frente de la cola de prioridad es la configuración
            # de menor costo f
            nodo = heapq.heappop(agenda)[1]
            # Agregamos el estado a la lista de expandidos
            expandidos.add(nodo)
            # En A* es necesario verificar la condición de 
            # paro tras sacar el elemento de la agenda
            if stop(nodo):
                return trajectory(nodo)
            # Realizamos la expansión del vértice
            for sucesor in nodo.expand():
                # Agregamos a la cola de prioridad siempre que no se haya
                # expandido previamente
                if sucesor not in expandidos:
                    heapq.heappush(agenda,(f(sucesor),sucesor))
        # No hay ruta al nodo meta
        # instrucción redundante
        return None
    
seed(2019)
p = Puzzle()
# 40 movimientos aleatorios
p.shuffle(40)
print("rompecabezas a resolver:",p)

# Invocamos al algoritmo A*
ruta = AStar.search(p, # rompecabezas desordenado
                    lambda s:s==Puzzle(), # detenerse si esta ordenado
                    lambda s:s.get_depth(), # el costo acumulado es la profunidad
                    lambda s:h1(s,Puzzle())) # la heurística h1
print("la ruta encontrada:",ruta)
print("longitud de la ruta:",len(ruta)-1)

# Para obtener el algortimo UCS no
# usamos información del dominio del problema
# hacemos h cero para toda configuración
h_ucs = lambda s: 0

# Invocamos al algoritmo A*, se comportará como UCS
ruta = AStar.search(p, # rompecabezas desordenado
                    lambda s:s==Puzzle(), # detenerse si esta ordenado
                    lambda s:s.get_depth(), # el costo acumulado es la profunidad
                    h_ucs) # la heurística es cero para toda configuración
print("la ruta encontrada:",ruta)
print("longitud de la ruta:",len(ruta)-1)

# Para obtener el algortimo GBFS no tomamos
# en cuenta el costo acumulado
# solo nos fijamos en la estimación a la meta
# para ello hacemos la función de costo igual a cero
g_gbfs = lambda s:0

# Invocamos al algoritmo A*, se comportará como GBFS
ruta = AStar.search(p, # rompecabezas desordenado
                    lambda s:s==Puzzle(), # detenerse si esta ordenado

                    g_gbfs, # el costo acumulado no se tomará en cuenta
                    lambda s:h1(s,Puzzle())) # la heurística h1
print("la ruta encontrada:",ruta)
print("longitud de la ruta:",len(ruta)-1)

import timeit
from functools import partial

# función de paro
stop = lambda s:s==Puzzle()
# función de costo acumulado
g = lambda s:s.get_depth()
#función heurística

h = lambda s:h1(s,Puzzle())

# definimos una función para A*
def a_star(p,stop,g,h):
    return AStar.search(p,stop,g,h)

# función para UCS
def ucs(p,stop,g):
    return AStar.search(p,stop,g,lambda s:0)
    
# función para GBFS
def gbfs(p,stop,h):
    return AStar.search(p,stop,lambda s:0,h)

# Invocamos el algoritmo A*, tomamos el tiempo que toma una ejecución
t = timeit.timeit(partial(a_star,p=p,stop = stop,g=g,h=h),number=1)
print("A* tomó %.4f segundos en encontrar la solución"%t)
# Invocamos el algoritmo UCS, tomamos el tiempo que toma una ejecución
t = timeit.timeit(partial(ucs,p=p,stop = stop,g=g),number=1)
print("UCS tomó %.4f segundos en encontrar la solución"%t)
# Invocamos el algoritmo GBFS, tomamos el tiempo que toma una ejecucióN
t = timeit.timeit(partial(gbfs,p=p,stop = stop,h=h),number=1)
print("GBFS tomó %.4f segundos en encontrar la solución"%t)

# La secuencia del 0 al 15
# 0 representará el espacio en blanco
seq = list(range(0,16))
# el renglón
row = lambda i: i//4
# la columna
col = lambda i: i%4

class ManhattanDistance:
    """
    Implementación de la distancia de Manhattan para el rompecabezas del 15
    """
    def __init__(self,target = Puzzle()):
        """
        Crea el objeto para la meta establecida
        :param target: configuración meta
        """
        self.target =target
        self.locations =self._find_locations(target)
        self.distances = self._precompute_distances(self.locations)
        
    def _find_locations(self,puzzle):
        """
        Encuentra la posición de cada ficha
        :param puzzle: el rompecabezas
        :return: las posiciones
        """
        locations = [None]*16
        for i in enumerate(Puzzle.to_list(puzzle)):
            locations[i[1]] = i[0]
        return locations
        
    def _precompute_distances(self,locations):
        """
        Precalcula distancias por posición
        :param locations: ubicación de las fichas
        :return: las distancias
        """
        distances = [[0]*16 for i in seq]
        for i in seq:
            for j in seq:
                distances[i][j] = abs(row(j)-row(locations[i]))+ \
                abs(col(j)-col(locations[i]))
        return distances
       
    def distance_to_target(self,puzzle):
        """
        Calcula la distancia de Manhattan al objetivo
        :param puzzle: la configuración 
        :return: la distancia
        """
        # no consideramos la posición del cero
        return sum(map(lambda i:self.distances[i[0]+1][i[1]],\
        enumerate(self._find_locations(puzzle)[1:])))
    
m = ManhattanDistance(target=Puzzle())

h2 = m.distance_to_target

print("La heurística h1 (número de piezas desordenadas) es:",h1(p,Puzzle()))
print("La heurística h2 (distancia de Manhattan) es:",h2(p))


# Invocamos el algoritmo A*, tomamos el tiempo que toma una ejecución
t = timeit.timeit(partial(a_star,p=p,stop = stop,g=g,h=h2),number=1)
print("A* tomó %.4f segundos en encontrar la solución"%t)
# Invocamos el algoritmo UCS, tomamos el tiempo que toma una ejecución
t = timeit.timeit(partial(ucs,p=p,stop = stop,g=g),number=1)
print("UCS tomó %.4f segundos en encontrar la solución"%t)
# Invocamos el algoritmo GBFS, tomamos el tiempo que toma una ejecucióN
t = timeit.timeit(partial(gbfs,p=p,stop = stop,h=h2),number=1)
print("GBFS tomó %.4f segundos en encontrar la solución"%t)

from functools import reduce
from termcolor import colored
from random import choice
from itertools import product

# Códigos de los colores
# Blanco
W = 0;
# Verde
G = 1;
# Rojo
R = 2;
# Azul
B = 3;
# Azul cielo
C = 4;
# Amarillo
Y = 5;

# Diccionario con los nombres para los códigos
color_map = {
    0:"white",
    1:"green",
    2:"red",
    3:"blue",
    4:"cyan",
    5:"yellow"}

# Cada Letra será una posición relativa a los colores de 
# los cubos de los centros de cada cara
# (los centros no cambian de posción con los giros)
# Código de letra : (localización del bloque, color de la ubicación)
#
# Hay que imaginar el cubo desdoblado
# Así se interpretan las letras
#
#     ABC
#     DEF
#     GHI
# JKL MNÑ OPQ RST
# UVW XYZ abc def
# ghi jkl mnñ opq
#     rst
#     uvw
#     xyz
#
# El cubo esta codificado como una secuencia de bits
# Cada subcubo tiene 3 bits
# Este es el código de colores
#
# 000 White
# 001 Green
# 010 Red
# 011 Blue
# 100 Cian (El naranja no esta disponible como color de terminal)
# 101 Yellow
#
code = {
    'A' : (0,W),
    'B' : (3,W),
    'C' : (6,W),
    'D' : (9,W),
    'E' : (12,W),
    'F' : (15,W),
    'G' : (18,W),
    'H' : (21,W),
    'I' : (24,W),
    'J' : (27,G),
    'K' : (30,G),
    'L' : (33,G),
    'M' : (36,R),
    'N' : (39,R),
    'Ñ' : (42,R),
    'O' : (45,B),
    'P' : (48,B),
    'Q' : (51,B),
    'R' : (54,C),
    'S' : (57,C),
    'T' : (60,C),
    'U' : (63,G),
    'V' : (66,G),
    'W' : (69,G),
    'X' : (72,R),
    'Y' : (75,R),
    'Z' : (78,R),
    'a' : (81,B),
    'b' : (84,B),
    'c' : (87,B),
    'd' : (90,C),
    'e' : (93,C),
    'f' : (96,C),
    'g' : (99,G),
    'h' : (102,G),
    'i' : (105,G),
    'j' : (108,R),
    'k' : (111,R),
    'l' : (114,R),
    'm' : (117,B),
    'n' : (120,B),
    'ñ' : (123,B),
    'o' : (126,C),
    'p' : (129,C),
    'q' : (132,C),
    'r' : (135,Y),
    's' : (138,Y),
    't' : (141,Y),
    'u' : (144,Y),
    'v' : (147,Y),
    'w' : (150,Y),
    'x' : (153,Y),
    'y' : (156,Y),
    'z' : (159,Y)    
}

# Espacios en blanco, para la impresión del cubo
BLANK = ' '*6
# chr(FILL) caracter de llenado
FILL = 9608
# cuantas veces el caracter de llenado
K = 2
    
# las acciones son listas de listas de listas de tuplas
# Representan giros de 90 grados en todas las caras del cubo
actions = [
# La primer lista interna es el eje X
[
    # La primera lista de la primera lista interna
    # Es la lista de tuplas con parejas que indican
    # que pasa con cada letra al aplicar la acción.
    # Giro 90 grados en la dirección de las manecillas
    # del reloj en la cara inferior de acuerdo a la
    # figura de referencia y visto desde arriba
    # por ejemplo ('A','g') indica que 'g' tomará la
    # posición de 'A' al rotar este eje
    [('A','g'),('B','U'),('C','J'),('Q','A'),('c','B'),
    ('ñ','C'),('z','Q'),('y','c'),('x','ñ'),('g','z'),
    ('U','y'),('J','x'),('R','T'),('S','f'),('T','q'),
    ('d','S'),('f','p'),('o','R'),('p','d'),('q','o')],
    # Giro 90 grados en la dirección de las manecillas
    # del reloj en la cara superior visto desde arriba
    [('G','i'),('H','W'),('I','L'),('O','G'),('a','H'),
    ('m','I'),('t','O'),('s','a'),('r','m'),('i','t'),
    ('W','s'),('L','r'),('M','j'),('N','X'),('Ñ','M'),
    ('Z','N'),('l','Ñ'),('k','Z'),('j','l'),('X','k')]
],\
# La segunda lista interna es el eje Y
[
    # Giro de 90 grados hacia el frente de la cara
    # que queda del lado izquierdo
    [('A','q'),('D','f'),('G','T'),('M','A'),('X','D'),
    ('j','G'),('r','M'),('u','X'),('x','j'),('T','x'),
    ('f','u'),('q','r'),('J','g'),('K','U'),('L','J'),
    ('U','h'),('W','K'),('g','i'),('h','W'),('i','L')],
    # Giro de 90 grados hacia el frente de la cara
    # que queda del lado derecho
    [('C','o'),('F','d'),('I','R'),('Ñ','C'),('Z','F'),
    ('l','I'),('t','Ñ'),('w','Z'),('z','l'),('o','t'),
    ('d','w'),('R','z'),('O','Q'),('P','c'),('Q','ñ'),
    ('a','P'),('c','n'),('m','O'),('n','a'),('ñ','m')]
],\
# La tercera lista interna es el eje Z
[
    # Giro de 90 grados hacia la derecha de la cara
    # que se encuentra arriba en la figura 2D
    [('J','R'),('K','S'),('L','T'),('M','J'),('N','K'),
    ('Ñ','L'),('O','M'),('P','N'),('Q','Ñ'),('R','O'),
    ('S','P'),('T','Q'),('G','A'),('H','D'),('I','G'),
    ('F','H'),('C','I'),('B','F'),('A','C'),('D','B')], 
    # Giro de 90 grados hacia la derecha de la cara
    # que se encuentra abajo en la figura 2D
    [('g','o'),('h','p'),('i','q'),('j','g'),('k','h'),
    ('l','i'),('m','j'),('n','k'),('ñ','l'),('o','m'),
    ('p','n'),('q','ñ'),('r','x'),('s','u'),('t','r'),
    ('u','y'),('w','s'),('x','z'),('y','w'),('z','t')]
]]

# calcula la configuración ordenada del cubo
# por única vez
initial_conf = reduce(lambda x,y:(0,x[1]|(y[1]<<y[0])), \
[(0,0)]+[v for k,v in code.items()])[1]

# La clase abtrae el grafo de estados acciones
class RubikPuzzle(EstadoProblema):
    """
    Cubo de Rubik de 3 X 3
    Implementación con todos los subcubos 
    Cada subcubo una terna de bit que codifica su color
    """
    def __init__(self,parent = None,action=None,depth=0,pattern=None):
        """
        Crea el rompecabezas de Rubik.
        :param parent: el predecesor de la configuración a crear
        :param action: la acción que se toma para crear al hijo
        a partir de su predecesor
        :param depth: la profundidad del nodo
        :param pattern: un diccionario con la configuración a 
        establecer en el nodo
        """
        self.parent = parent
        self.depth = depth
        if parent != None and action!=None:
            # se crea el cubo a partir de la configuración del padre
            self.configuration = parent.configuration
            # se aplica la acción
            self.apply(action)
        elif pattern!=None:
            # se establece la configuración con el mapa
            self.configuration = self.initialize(pattern)
        else:
            # un cubo ordenado
            self.configuration = initial_conf
            
    def initialize(self,pattern):
        """
        Establece la configuración del cubo
        :param pattern: la configuración a establecer en diccionario
        :return: la configuración codificada en bits
        """
        # la configuración a establecer esta en un
        # diccionario {letra:código de color}
        return reduce(lambda x,y:x|y,\
        [val<<(code[key][0]) for key,val in pattern.items()])
            
    def cube(self,symbol):
        """
        Un subcubo a mostrar
        :param symbol: letra de la posición a mostrar
        :return: la cadena a mostrar como subcubo
        """
        n = code[symbol][0]
        return \
        colored(chr(FILL),color_map[(((7<<n)&self.configuration)>>n)])*K
        
    def apply(self,action):
        """
        Aplica la acción a la configuración
        """
        # tupla de acción (eje,renglón,dirección)
        # giro de izquierda a derecha
        if(action[2]==0):
            moved,mask = reduce(lambda x,y:(x[0]|y[0],x[1]|y[1]),\
            [self.move(x) for x in actions[action[0]][action[1]]])
        else: #giro de derecha a izquierda
            moved,mask = reduce(lambda x,y:(x[0]|y[0],x[1]|y[1]),\
            [self.move((b,a)) for a,b in actions[action[0]][action[1]]])
        self.configuration = moved | \
        ((((2<<162)-1)^mask)&self.configuration)
                
    def move(self,locations):
        """
        Mueve el valor de una localidad a otra
        :param locations: las posiciones a mover
        :return: tupla con el bloque movido y la máscara de bits
        """
        # de la posición i a la j
        i = code[locations[0]][0]
        j = code[locations[1]][0]
        #regresa tanto el bloque movido como la máscara
        return (((((7<<i)&self.configuration)>>i)<<j),(7<<i)|(7<<j))
        
            
    def __str__(self):
        """
        El cubo a mostar en texto.
        :return: representación del cubo en texto
        """
        return ('\n'+
        BLANK+self.cube('A')+self.cube('B')+self.cube('C')+'\n'+
        BLANK+self.cube('D')+self.cube('E')+self.cube('F')+'\n'+
        BLANK+self.cube('G')+self.cube('H')+self.cube('I')+'\n'+
        self.cube('J')+self.cube('K')+self.cube('L')+
        self.cube('M')+self.cube('N')+self.cube('Ñ')+
        self.cube('O')+self.cube('P')+self.cube('Q')+  
        self.cube('R')+self.cube('S')+self.cube('T')+'\n'+
        self.cube('U')+self.cube('V')+self.cube('W') +
        self.cube('X')+self.cube('Y')+self.cube('Z') +
        self.cube('a')+self.cube('b')+self.cube('c')+ 
        self.cube('d')+self.cube('e')+self.cube('f') +'\n'+        
        self.cube('g')+self.cube('h')+self.cube('i')+
        self.cube('j')+self.cube('k')+self.cube('l') +
        self.cube('m')+self.cube('n')+self.cube('ñ')+ 
        self.cube('o')+self.cube('p')+self.cube('q') +'\n'+                
        BLANK+self.cube('r')+self.cube('s')+self.cube('t')+'\n'+
        BLANK+self.cube('u')+self.cube('v')+self.cube('w')+'\n'+
        BLANK+self.cube('x')+self.cube('y')+self.cube('z')+'\n' )
        
    def __repr__(self):
        """
        :return: representación visual del cubo
        """
        return self.__str__()

    def __eq__(self,other):
        """
        Dos cubos son iguales si sus configuraciones son iguales
        :param other: el otro cubo
        :return: verdadero si son iguales, falso de otra forma
        """
        return (isinstance(other, self.__class__)) and \
        (self.configuration==other.configuration)

    def __ne__(self,other):
        """
        Determina si los cubos son diferentes
        :param other: el otro cubo
        :return: verdadero si los cubos son diferentes, falso de 
        otra forma
        """
        return not self.__eq__(other)
        
    def __lt__(self,other):
        """
        Determina si la profundidad de un cubo es menor que la de otro
        :param other: el otro cubo
        :return: verdadero si la profundidad del cubo es menor a la del otro
        """
        return self.depth < other.depth

    def __hash__(self):
        """
        Función de hash para un cubo
        :return: un entero hash 
        """
        return hash(self.configuration)
        
    def pattern_equals(self,pattern,target=initial_conf):
        """
        Determina si el cubo es parte de un patrón
        :param pattern: el patrón a verificar
        :target: la meta
        :return: verdadero si el patrón incluye la 
        configuración del cubo
        """
        mask = RubikPuzzle.get_pattern_mask(pattern)
        return ((mask&self.configuration)^(mask&target))==0
        
    @staticmethod
    def get_pattern_mask(pattern):
        """
        Calcula la mácara de bits para extraer los patrones
        :param patter: el patrón que define la máscara
        :return la máscara de bits
        """
        return reduce(lambda x,y:x|y,[(7<<code[letter][0])\
        for letter in pattern])
    
    def get_parent(self):
        return self.parent
    
    def get_depth(self):
        return self.depth
        
    def shuffle(self,n):
        """
        Desordena el cubo
        :param n: número de movimientos
        """
        for i in range(0,n):
            self.apply((choice([0,1,2]),choice([0,1]),choice([0,1])))
            
    def expand(self):
        # quitamos el predecesor
        return list(filter(lambda x: \
        (x!=self.parent), \
        [RubikPuzzle(self,action,self.depth+1) \
        for action in product([0,1,2],[0,1],[0,1])]))
    
cubo = RubikPuzzle()
print(cubo)

sucesores = cubo.expand()
print(sucesores)
print("El factor de arborescencia es:",len(sucesores))

#inicializamos el generador de números aleatorios
seed(201901)
cubo = RubikPuzzle()
cubo.shuffle(5)
print("cubo a resolver:",cubo)

# Usamos A* como un UCS haciendo h=0
ruta = ucs(cubo,lambda s:s==RubikPuzzle(),lambda s:s.get_depth())
print("la ruta encontrada es:",ruta)
print("la longitud de la ruta es",len(ruta)-1)

from collections import deque

class PatternBasedHeuristic:
    """
    Implementación de Hurística para el cubo de Rubik
    Basada en una base de datos de patrones
    """
    def __init__(self,objective=None,depth=6,pattern=None):
        """
        Crea la base de datos de patrones
        :param objective: el estado meta
        :param depth: la profundidad máxima de los estados en la base
        :param pattern: el patrón con el que se forma la base
        """
        print('computing pattern data base...')
        if(objective==None):
            # De no establecerse otro objetivo se pide ordenar el cubo
            objective = RubikPuzzle()
        # para generar la base de datos nuestra búsqueda es tipo BFS
        agenda = deque()
        self.explored = set()
        self.depth = depth
        # agregamos el estado objetivo como nodo inicial
        agenda.append(objective)
        # nuestra base de datos es un diccionario
        self.patterns = {}
        # si el patrón no se especifica usaremos las esquinas
        if(pattern==None):
            pattern ='ACGIJLgiMÑjlOQmñRToqrtxz'
        self.pattern = pattern
        # obtiene la mascara para este patrón
        self.pattern_mask = RubikPuzzle.get_pattern_mask(pattern)
        # mientras la agenda no este vacía
        while(agenda):
            # sacamos el frente de la agenda (agenda es una cola)
            node = agenda.popleft()
            # agregamos a expandidos
            self.explored.add(node)
            # la configuración del nodo
            conf = self.pattern_mask&node.configuration
            # agregamos la subconfiguración a la base de datos
            # si es la primera vez que la descubrimos
            # le asociamos la profundidad
            if conf not in self.patterns:
                self.patterns[conf] = node.depth
            for child in node.expand():
                if(child.depth>depth):
                    #hemos terminado
                    return 
                elif child not in self.explored:
                    # agregamos al hijo en caso de que no se haya
                    # expandido
                    agenda.append(child)
                    
                    
    def heuristic(self,puzzle):
        """
        calcula la heurística usando la base de datos
        """
        key = self.pattern_mask&puzzle.configuration
        return (self.patterns[key] \
        if key in self.patterns else self.depth+1)
    
    from collections import deque

class PatternBasedHeuristic:
    """
    Implementación de Hurística para el cubo de Rubik
    Basada en una base de datos de patrones
    """
    def __init__(self,objective=None,depth=6,pattern=None):
        """
        Crea la base de datos de patrones
        :param objective: el estado meta
        :param depth: la profundidad máxima de los estados en la base
        :param pattern: el patrón con el que se forma la base
        """
        print('computing pattern data base...')
        if(objective==None):
            # De no establecerse otro objetivo se pide ordenar el cubo
            objective = RubikPuzzle()
        # para generar la base de datos nuestra búsqueda es tipo BFS
        agenda = deque()
        self.explored = set()
        self.depth = depth
        # agregamos el estado objetivo como nodo inicial
        agenda.append(objective)
        # nuestra base de datos es un diccionario
        self.patterns = {}
        # si el patrón no se especifica usaremos las esquinas
        if(pattern==None):
            pattern ='ACGIJLgiMÑjlOQmñRToqrtxz'
        self.pattern = pattern
        # obtiene la mascara para este patrón
        self.pattern_mask = RubikPuzzle.get_pattern_mask(pattern)
        # mientras la agenda no este vacía
        while(agenda):
            # sacamos el frente de la agenda (agenda es una cola)
            node = agenda.popleft()
            # agregamos a expandidos
            self.explored.add(node)
            # la configuración del nodo
            conf = self.pattern_mask&node.configuration
            # agregamos la subconfiguración a la base de datos
            # si es la primera vez que la descubrimos
            # le asociamos la profundidad
            if conf not in self.patterns:
                self.patterns[conf] = node.depth
            for child in node.expand():
                if(child.depth>depth):
                    #hemos terminado
                    return 
                elif child not in self.explored:
                    # agregamos al hijo en caso de que no se haya
                    # expandido
                    agenda.append(child)
                    
                    
    def heuristic(self,puzzle):
        """
        calcula la heurística usando la base de datos
        """
        key = self.pattern_mask&puzzle.configuration
        return (self.patterns[key] \
        if key in self.patterns else self.depth+1)
    
# creamos la base de datos de patrones
db = PatternBasedHeuristic(depth=5)

# definimos la heurística h usando la base de datos
h = db.heuristic
# usamos A* para resolver el cubo
ruta = a_star(cubo,lambda s:s==RubikPuzzle(),lambda s:s.get_depth(),h)
print("la ruta encontrada es:",ruta)
print("la longitud de la ruta es",len(ruta)-1)

# Se paciente al correr esta celda puede tomar algo de tiempo
# creamos la base de datos de patrón de esquinas
# usamos profundidad 6
# descomenta la línea siguiente
db1 = PatternBasedHeuristic(depth=6,pattern = "ACGIJLgiMÑjlOQmñRToqrtxz")

# Crea la segunda base de datos para el patrón de cruces
# usa profundidad 6
# llamale db2 a la base de datos
db2 = PatternBasedHeuristic(depth=6, pattern = "BDHFKUhWNxKZPancSdpfsuyw")

# definimos las heuristicas de cada base
# descomenta las líneas siguiente
h1 = db1.heuristic
h2 = db2.heuristic

# para la parte 1 de tu tarea de programación descomenta el código
# siguiente, copia la salida a un archivo e ingresalo como solución
print(sum(db1.patterns.values())+sum(db2.patterns.values()))

# Crea una heurística combinando las dos heurísticas anteriores
# toma en consideración que ambas heurísticas son admisibles
# la nueva heurística debe ser admisible
# dale a la heurística el nombre de h

db3 = PatternBasedHeuristic(depth=6,pattern = "ACGIJLgiMÑjlOQmñRToqrtxzBDEFHKNPSUXadVYbeWZcfhknpsuvwy") 
#h = AQUÍ TU CÓDIGO
h = db3.heuristic

# Descomenta el código siguiente y somete la salida como la parte 2
# de tu tarea de programación
seed(20190118)
time_inicial = time.perf_counter()
cubo = RubikPuzzle()
cubo.shuffle(13)
ruta = a_star(cubo,lambda s:s==RubikPuzzle(),lambda s:s.get_depth(),h)
res = "".join(str(n.configuration)+str(h(n))+str(h1(n))+str(h2(n)) for n in ruta)
print(res)
time_final = time.perf_counter()
tiempo = time_final - time_inicial
print(f"{tiempo} [s]")
