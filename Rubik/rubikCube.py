from abc import ABC, abstractmethod
import time
from functools import reduce
import random
from collections import deque
import heapq
from random import seed, choice
from termcolor import colored
from itertools import product
import csv
import sys
import os


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

class AStar: #Implementation of the A* algorithm
  
    @staticmethod
    def search(origin, stop,g,h):
        """
        origin: Initial state
        stop: Stop funtion, true for the goal state
        g: Cumulative cost function
        h: Heuristic function, estimated cost to the goal
        """
        #Priority queue
        agenda = []
        # Set of state expanded
        expanded = set()
        #Trivial condition
        if stop(origin):
            return Trajectory(origin)
        
        #Initial state of the priority queue
        f = lambda s: g(s) + h(s)
        
        #tie-breaker, in the case is a tie in the cost between two nodes
        tie_breaker_counter = 0
        #This was implemented because the desicion makingfor the algorithm turned probabilistic when the cost were the same, this way
        #we made sure the algorithm would always take the same path
        #Tuple with 3 elements: (f_cost, tie_breaker_counter, node)
        heapq.heappush(agenda,(f(origin), tie_breaker_counter, origin))
        tie_breaker_counter += 1

        #While agenda unlike empty
        while agenda:
            # We pop the full tuple and get the node at index [2]
            node = heapq.heappop(agenda)[2] 
            # Check if node was already expanded. This check is needed because we might add the same node multiple times with different f-costs before expanding it.
            if node in expanded:
                continue
                
            expanded.add(node)
            
            if stop(node):
                return Trajectory(node)
            for sucessor in node.Expand():
                if sucessor not in expanded:
                    heapq.heappush(agenda, (f(sucessor), tie_breaker_counter, sucessor))
                    tie_breaker_counter += 1
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
ColorMap = {
    0:"white",
    1:"green",
    2:"red",
    3:"blue",
    4:"cyan",
    5:"yellow"}

#Map inverse, from read the CSV
colorNameMap = {name: code for code, name in ColorMap.items()}

"""
letter diagram:
Face 1 (top): ABCDEFGHI | White
Face 2 (Left): JKLUVWghi    | Green
Face 3 (Front): MNÑXYZjkl   | Red
Face 4 (Right): OPQabcmnñ   | Blue
Face 5 (Back): RSTdefopq    | Cyan
Face 6 (Bottom): rstuvwxyz  | Yellow
"""
faceLetters = [
    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], # White
    ['J', 'K', 'L', 'U', 'V', 'W', 'g', 'h', 'i'], # Green
    ['M', 'N', 'Ñ', 'X', 'Y', 'Z', 'j', 'k', 'l'], #  Red
    ['O', 'P', 'Q', 'a', 'b', 'c', 'm', 'n', 'ñ'], #  Blue
    ['R', 'S', 'T', 'd', 'e', 'f', 'o', 'p', 'q'], #  Cyan
    ['r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']  #  Yellow
]

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

class RubikPuzzle:
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
        colored(chr(FILL),ColorMap[(((7<<n)&self.configuration)>>n)])*K
        
    def apply(self,action):
        """
        Apply the action to the configuration
        """
        # Action tuple (axis, row, direction)
        # Turn from left to right
        if(action[2]==0):
            moved,mask = reduce(lambda x,y:(x[0]|y[0],x[1]|y[1]),\
            [self.move(x) for x in actions[action[0]][action[1]]])
        else: # Turn from right to left
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
        # from position i to j
        i = code[locations[0]][0]
        j = code[locations[1]][0]
        # returns both the moved block and the mask
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
        other: The other cube
        return: true if the depth of one cube is less than the other
        Used as tiebreaker before implementing tie-breaker-counter, kept in case the tie breaker doesnt work (theorically impossible)
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
    
    def GetParent(self):
        return self.parent
    
    def GetDepth(self):
        return self.depth       
            
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
            # If we don't establish other objective we ask to order the cube 
            objective = RubikPuzzle()
        # To generate the data base our search is a BFS type
        agenda = deque()
        self.explored = set()
        self.depth = depth
        # We add the objective state as initial node
        agenda.append(objective)
        # Our data base is a dictionary 
        self.patterns = {}
        # If the pattern is not specified we use the corners
        if(pattern==None):
            pattern ='ACGIJLgiMÑjlOQmñRToqrtxz'
        self.pattern = pattern
        # Obtains the mask for this patterns
        self.pattern_mask = RubikPuzzle.GetpatternMask(pattern)
        # While the agenda is not empty
        while(agenda):
            # We pop the front of the agenda (the agenda is a queue)
            node = agenda.popleft()
            # We add to expanded
            self.explored.add(node)
            # Configuration for the node
            conf = self.pattern_mask&node.configuration
            # We add the subconfiguration to the data base
            # If it's the first time we discover it
            # we associate the depth
            if conf not in self.patterns:
                self.patterns[conf] = node.depth
            for child in node.Expand():
                if(child.depth>depth):
                    # All finished
                    return 
                elif child not in self.explored:
                    # We add the child node to the case in which it hasn´t been expanded
                    agenda.append(child)
                    
    def Heurisic(self,puzzle):
        """
        calculates heuristics using the database
        """
        key = self.pattern_mask&puzzle.configuration
        return (self.patterns[key] \
        if key in self.patterns else self.depth+1)
    
def LoadCubeCSV(filename):
    """
    Loads a cube configuration from a CSV file.
    :param filename: The path to the .csv file
    :return: A 'pattern' dictionary for RubikPuzzle, or None if there is an error
    """
    print(f"Loading the cube state from '{filename}'...")
    pattern = {}
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            AllRows = list(reader)
            
            if len(AllRows) != 6:
                print(f"Error: The CSV must have exactly 6 rows (one per face). Found {len(AllRows)}.")
                return None

            for RowIndex, row in enumerate(AllRows):
                
                if len(row) != 9:
                    print(f"Error: The row {RowIndex+1} must have 9 color values. Found {len(row)}.")
                    print(f"Row data: {row}")
                    return None
                
                LettersForFaces = faceLetters[RowIndex]
                
                for ColIndex, ColorName in enumerate(row):
                    ColorNameClean = ColorName.strip().lower()
                    
                    if ColorNameClean not in colorNameMap:
                        if ColorNameClean == "":
                            print(f"Error: Empty cell found in row {RowIndex+1}, column {ColIndex+1}.")
                        else:
                            print(f"Error: Unknown color '{ColorName}' in row {RowIndex+1}, column {ColIndex+1}.")
                        return None
                    
                    letter = LettersForFaces[ColIndex]
                    color_code = colorNameMap[ColorNameClean]
                    pattern[letter] = color_code
                    
    except FileNotFoundError:
        print(f"Error: File not found in '{filename}'")
        return None
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")
        return None
    
    print("CSV file uploaded successfully.")
    return pattern
    
#---------------------Main----------------------

if __name__ == "__main__":

    # Create the cube Rubik's
    SolvedCube = RubikPuzzle()
    print("Cube solved initial: ")
    print(SolvedCube)

    ScriptDir = os.path.dirname(os.path.abspath(__file__))
    
    # Une la ruta del script con el nombre del archivo CSV
    CSVFile = os.path.join(ScriptDir, 'Moves.csv')  # CSVFile = 'Moves.csv'
   
    
    # Charge File
    ScramblePattern = LoadCubeCSV(CSVFile)
    
    if ScramblePattern is None:
        print("Error loading cube from CSV. Exiting.")
        sys.exit(1)

    InitialCube = RubikPuzzle(pattern=ScramblePattern)
    
    print(f"\nCube loaded from '{CSVFile}':")
    print(InitialCube)

    # Create pattern-based heuristics
    heuristic = PatternBasedHeuristic(depth=4) #Changes

    # Define the functions required by A*
    stop = lambda state: state.configuration == InitialConf
    g = lambda state: state.GetDepth()
    h = lambda state: heuristic.Heurisic(state)

    print("\nExecute search A*...\n")
    StartTime = time.time()

    solution = A_Star(InitialCube, stop, g, h)

    EndTime = time.time()
    TotalTime = EndTime - StartTime

    # Results
    if solution is not None:
        print(f"Solution found in {len(solution)-1} movements.")
        print(f"Total Time: {TotalTime:.2f} seconds\n")
        print("Solution path:\n")

        for i, state in enumerate(solution):
            print(f"Step {i}:")
            print(state)
            print("-" * 40)
    else:
        print("Not found solution")