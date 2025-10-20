from abc import ABC, abstractmethod
import time
from functools import reduce
import random
from collections import deque
import heapq
from random import seed
from termcolor import colored
from random import choice
from itertools import product

class ProblemState:
    """
    The class ProblemState is abstract.
    It represents a state or configuration of the problem to be solved.
    """

    @abstractmethod
    def Expand(self):
        """
        :return: set of successor states
        """
        pass
    
    @abstractmethod
    def GetDepth(self):
        """
        :return: depth of the state
        """
        pass

    @abstractmethod
    def GetParent(self):
        """
        :return: reference of the predecessor state
        """
        pass

def Trajectory(end):
    """
    Trajectory will return the trajectory from a state
    """
    sequence = deque()
    sequence.append(end)
    while end.GetParent():
        end = end.GetParent()
        sequence.append(end)
    sequence.reverse()
    return list(sequence)

class AStar:
    """
    Implementation of the A* algorithm
    """

    @staticmethod
    def search(origin, stop,g,h):
        """
        :param source: Initial state
        :param stop: Stop funtion, true for the goal state
        :param g: Cumulative cost function
        :param h: Heuristic function, estimated cost to the goal
        """
        #Priority queue
        agenda = []
        # Set of state expanded
        expanded = set()
        #Trivial condition
        if stop(origin):
            return Trajectory(origin)
        
        #Initial state of the priority queue | The priority will be f(s) = g(s) + h(s)
        f = lambda s: g(s) + h(s)
        heapq.heappush(agenda,(f(origin), origin))

        #While agenda unlike empty
        while agenda:
            node = heapq.heappop(agenda)[1]
            expanded.add(node)
            if stop(node):
                return Trajectory(node)
            for sucessor in node.Expand():
                if sucessor not in expanded:
                    heapq.heappush(agenda, (f(sucessor), sucessor))
        return None
    
#Definition in the function for A*
def A_Star(p, stop, g, h):
    return AStar.search(p, stop, g, h)

#Color codes
#White
W = 0;
# Green
G = 1;
# Red
R = 2;
# Blue
B = 3;
# Cyan
C = 4;
# Yellow
Y = 5;

#Dictionary with names for codes
color_map = {
    0:"white",
    1:"green",
    2:"red",
    3:"blue",
    4:"cyan",
    5:"yellow"}

"""
Each letter will be a position relative to the colors of the cubes in the 
centers of each face (the centers do not change position eitch rotation)
Letter code: (block location, location color)

    ABC
    DEF
    GHI
JKL MNÑ OPQ RST
UVW XYZ abc def
ghi jkl mnñ opq
    rst
    uvw
    xyz

The cube is encoded as a sequence of bits. Each subcube has 3 bits
This is the color code.

000 White
001 Green
010 Red
011 Blue
100 Cian
101 Yellow
"""

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

# Blank spaces, for printing the cube
BLANK = ' '*6
# chr(FILL) fill character
FILL = 9608
# how many times the fill character
K = 2
    
# The actions are lists of lists of lists of tuples
# they represent 90 degree rotations on all faces of the cube
actions = [
# The first internal list is the X axis
[
    
    # The first list of the first inner list. It's the list of
    # tuples with pairs that indicate what happens to each letter
    # when the action is applied. Rotating the lower face 90 degrees
    # clockwise according to the reference figure, and viewed from
    # above, for example ('A','g'), indicates that 'g' will take the
    # position of 'A' when rotating this axis.


    [('A','g'),('B','U'),('C','J'),('Q','A'),('c','B'),
    ('ñ','C'),('z','Q'),('y','c'),('x','ñ'),('g','z'),
    ('U','y'),('J','x'),('R','T'),('S','f'),('T','q'),
    ('d','S'),('f','p'),('o','R'),('p','d'),('q','o')],
    # Turn 90° clockwise
    # clockwise on the top face as seen from above
    [('G','i'),('H','W'),('I','L'),('O','G'),('a','H'),
    ('m','I'),('t','O'),('s','a'),('r','m'),('i','t'),
    ('W','s'),('L','r'),('M','j'),('N','X'),('Ñ','M'),
    ('Z','N'),('l','Ñ'),('k','Z'),('j','l'),('X','k')]
],\
# The second internal list is the Y axis
[
    # 90° turn toward the front of the face
    # on the left side
    [('A','q'),('D','f'),('G','T'),('M','A'),('X','D'),
    ('j','G'),('r','M'),('u','X'),('x','j'),('T','x'),
    ('f','u'),('q','r'),('J','g'),('K','U'),('L','J'),
    ('U','h'),('W','K'),('g','i'),('h','W'),('i','L')],
    # 90° turn toward the front of the face
    # on the right side
    [('C','o'),('F','d'),('I','R'),('Ñ','C'),('Z','F'),
    ('l','I'),('t','Ñ'),('w','Z'),('z','l'),('o','t'),
    ('d','w'),('R','z'),('O','Q'),('P','c'),('Q','ñ'),
    ('a','P'),('c','n'),('m','O'),('n','a'),('ñ','m')]
],\
# The last internal list is the Z axis
[
    # 90° turn to the right of the face
    [('J','R'),('K','S'),('L','T'),('M','J'),('N','K'),
    ('Ñ','L'),('O','M'),('P','N'),('Q','Ñ'),('R','O'),
    ('S','P'),('T','Q'),('G','A'),('H','D'),('I','G'),
    ('F','H'),('C','I'),('B','F'),('A','C'),('D','B')], 
    # 90° turn to the right of the face
    [('g','o'),('h','p'),('i','q'),('j','g'),('k','h'),
    ('l','i'),('m','j'),('n','k'),('ñ','l'),('o','m'),
    ('p','n'),('q','ñ'),('r','x'),('s','u'),('t','r'),
    ('u','y'),('w','s'),('x','z'),('y','w'),('z','t')]
]]

# calculates the ordered configuration of the cube
InitialConf = reduce(lambda x,y:(0,x[1]|(y[1]<<y[0])), \
[(0,0)]+[v for k,v in code.items()])[1]

class RubikPuzzle(ProblemState):
    """
    3 x 3 Rubik's Cube. Implementation with all subcubes
    Each subcube has a triplet of bits that encode its color
    """
    def __init__(self,parent=None, action=None, depth=0, pattern=None):
        """
        Creates the rubik's puzzle
        :param parent: The parent of the configuration to create
        :parama action: The action taken to create the chlid from is parent
        :param depth: The depth of the node
        :param pattern: A dictionary with the configuration to set on the node
        """
        self.parent = parent
        self.depth = depth
        if parent != None and action!=None:
            # the cube is created from the parent's configuration
            self.configuration = parent.configuration
            self.apply(action)
        elif pattern!=None:
            # the configuration is established with the map
            self.configuration = self.initialize(pattern)
        else:
            self.configuration = InitialConf
            
    def initialize(self,pattern):
        """
        Sets the cube configuration
        :param pattern: The configuration to set in the dictionary
        :return: The bit-encoded configuration
        """
        # The configuration to be set is in a
        # dictionary {letter:color code}
        return reduce(lambda x,y:x|y,\
        [val<<(code[key][0]) for key,val in pattern.items()])
            
    def cube(self,symbol):
        """
        A subcube to display
        :param symbol: letter of the position to display
        :return: the string to display as a subcube
        """
        n = code[symbol][0]
        return \
        colored(chr(FILL),color_map[(((7<<n)&self.configuration)>>n)])*K
        
    def apply(self,action):
        """
        Apply the action to the configuration
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
        Move the value from one location to another
        :param locations: the positions to move
        :return: tuple with the moved block and the bit mask
        """
        # de la posición i a la j
        i = code[locations[0]][0]
        j = code[locations[1]][0]
        #regresa tanto el bloque movido como la máscara
        return (((((7<<i)&self.configuration)>>i)<<j),(7<<i)|(7<<j))
        
            
    def __str__(self):
        """
        The cube to be displayed in text.
        :return: representation of the cube in text
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
        :return: visual representation of the cube
        """
        return self.__str__()

    def __eq__(self,other):
        """
        Two cubes are equal if their configurations are the same.
        :param other: The other cube
        :return: true if they are equal, false otherwise
        """
        return (isinstance(other, self.__class__)) and \
        (self.configuration==other.configuration)

    def __ne__(self,other):
        """
        Determine if the cubes are different
        :param other: The other cube
        :return: true if they are equal, false otherwise
        """
        return not self.__eq__(other)
        
    def __lt__(self,other):
        """
        Determines if the depth of one cube is less than the depth of another
        :param other: The other cube
        :return: true if the depth of one cube is less than the other
        """
        return self.depth < other.depth

    def __hash__(self):
        """
        Hash function for a cube
        :return: A integer
        """
        return hash(self.configuration)
        
    def PatternEqual(self,pattern,target=InitialConf):
        """
        Determine if the cube is part of a pattern
        :param pattern: the pattern to be verified
        :target: The goal
        :return: true if the pattern includes the
        cube configuration
        """
        mask = RubikPuzzle.GetpatternMask(pattern)
        return ((mask&self.configuration)^(mask&target))==0
        
    @staticmethod
    def GetpatternMask(pattern):
        """
        Calculate the bit mask to extract the patterns
        :param patter: the pattern that defines the mask
        :return: the bit mask
        """
        return reduce(lambda x,y:x|y,[(7<<code[letter][0])\
        for letter in pattern])
    
    def Getparent(self):
        return self.parent
    
    def GetDepth(self):
        return self.depth
        
    def Shuffle(self,n):
        """
        Disorder the cube
        :param n: Number of movements
        """
        for i in range(0,n):
            self.apply((choice([0,1,2]),choice([0,1]),choice([0,1])))
            
    def Expand(self):
        # we remove the predecessor
        return list(filter(lambda x: \
        (x!=self.parent), \
        [RubikPuzzle(self,action,self.depth+1) \
        for action in product([0,1,2],[0,1],[0,1])]))


class PatternBasedHeuristic:
    """
    Huristics Implementation for the Rubik's Cube
    Based on a Pattern Database
    """
    def __init__(self, objective=None, depth=6, pattern=None):
        """
        Create the pattern database
        :param objective: The goal state
        :param depth: the maximum depth of the states in the base
        :param pattern: the pattern with which the base is formed
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
        self.pattern_mask = RubikPuzzle.GetpatternMask(pattern)
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
            for child in node.Expand():
                if(child.depth>depth):
                    #hemos terminado
                    return 
                elif child not in self.explored:
                    # agregamos al hijo en caso de que no se haya expandido
                    agenda.append(child)
                    
    def Heurisic(self,puzzle):
        """
        calculates heuristics using the database
        """
        key = self.pattern_mask&puzzle.configuration
        return (self.patterns[key] \
        if key in self.patterns else self.depth+1)
    
#---------------------Main----------------------

#we created the corner pattern database, use depth 6
db1 = PatternBasedHeuristic(depth=6,pattern = "ACGIJLgiMÑjlOQmñRToqrtxz")

#create the second database for the cross pattern, use depth 6
db2 = PatternBasedHeuristic(depth=6, pattern = "BDHFKUhWNxKZPancSdpfsuyw")

#we define the heuristics of each base
h1 = db1.Heurisic
h2 = db2.Heurisic

#sum of the heuristics
print(sum(db1.patterns.values())+sum(db2.patterns.values()))

db3 = PatternBasedHeuristic(depth=6,pattern = "ACGIJLgiMÑjlOQmñRToqrtxzBDEFHKNPSUXadVYbeWZcfhknpsuvwy") 
h = db3.Heurisic

seed(20190118)

# Creamos y desordenamos el cubo
cube = RubikPuzzle()
cube.Shuffle(6)
print("Cubo a resolver:", cube)

# Medimos el tiempo solo de la búsqueda A*
time_initial = time.perf_counter()
route = A_Star(cube, lambda s:s == RubikPuzzle(), lambda s: s.GetDepth(), h)
final_time = time.perf_counter()

search_time = final_time - time_initial

# --- NUEVA SECCIÓN DE RESULTADOS ---

if route:
    print("\n--- Pasos de la Solución ---")
    
    # Imprime la ruta solo si tiene más de 1 estado (es decir, si no es solo el inicio)
    if len(route) > 1:
        for i, estado in enumerate(route[1:], start=1):
            print(f"Paso {i}:")
            print(estado) # Esto llama al método __str__ de RubikPuzzle
    else:
        print("(El cubo ya estaba resuelto)")

    print("\n--- Resumen ---")
    print(f"Tiempo total: {search_time:.4f} [s]")
    print(f"Pasos en la ruta: {len(route)-1}")
else:
    # Esto se ejecutará si A_Star retorna None (búsqueda fallida)
    print("\n--- BÚSQUEDA FALLIDA ---")
    print("No se encontró una solución.")
    print(f"Tiempo de búsqueda (sin solución): {search_time:.4f} [s]")



