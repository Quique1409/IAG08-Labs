import lines 
import heapq #Priority queue


class Nodo(): #represent a single station
    def __init__(self, name):
        self.name = name #station name
        self.neighbors = [] #list of neighboring stations
        self.dist = -1 #distance from the initial station
        self.father = None #previous station in the shortest path
        self.f = -1 #estimated total cost (g + h)

    def Addneighbors(self, neighbor, distance): 
        if neighbor != self.name and neighbor not in self.neighbors: #avoid adding itself as neighbor and duplicates
            self.neighbors.append((neighbor, distance)) 

class Graph: #represent the subway network
    def __init__(self):
        self.vertices = {} #dictionary of stations
        self.fathers = {} #to reconstruct the path

    def AddVertice(self, name_station, datos_station):
        self.vertices[name_station] = datos_station #add station to the graph

    def Dijkstra(self, InitialNode, FinalNode): #Dijkstra's algorithm to find the shortest path

        self.fathers.clear() #clear previous path data
        
        g_score = {name: float('inf') for name in self.vertices} #cost from start to current node, default to infinity
        g_score[InitialNode] = 0   #cost from start to start is 0

        priority = [(g_score[InitialNode], InitialNode)] #priority queue for exploring nodes

        while priority: #main loop, continues until all nodes are explored or the destination is reached
            # Get the node with the lowest g_score
            #This loop continues until all nodes are explored or the destination is reached
            _, current_node_name = heapq.heappop(priority) #get node with lowest g_score, 
            #_ its because we are not going to use the distance value just for know wich extract

            if current_node_name == FinalNode: #if we reached the destination
                path = [] #to store the path
                distance_Total = g_score[FinalNode] #total distance of the path
                temp = FinalNode
                while temp in self.fathers: #reconstruct the path using the fathers dictionary
                    path.append(temp) #add current node to path
                    temp = self.fathers[temp] 
                path.append(InitialNode) #add the initial node
                path.reverse() #reverse the path to get it from start to end
                return path, distance_Total

            for neighbor_name, distance in self.vertices[current_node_name]["neighbors"]:
                g_score_final = g_score[current_node_name] + distance
                
                if g_score_final < g_score.get(neighbor_name, float('inf')): #if the new path to neighbor is shorter
                    self.fathers[neighbor_name] = current_node_name #update the father of the neighbor
                    g_score[neighbor_name] = g_score_final #update the g_score of the neighbor
                    heapq.heappush(priority, (g_score[neighbor_name], neighbor_name)) #add neighbor to the priority queue
        
        return None, float('inf')
    
    def FindPathDijkstra(self, InitialNode, FinalNode):
        print(f"\n\033[105m*\033[0mResults using Dijkstra (Shortest path in distance):")
        if InitialNode not in self.vertices or FinalNode not in self.vertices: #check if both stations exist in the graph
            print(f"One or more subway stations weren't found.")
            return

        path, distance = self.Dijkstra(InitialNode, FinalNode) #find the shortest path using Dijkstra's algorithm
        if path: #if a path was found
            print(f"total distance: {distance / 1000:.2f} km")
            print(f"Number of stations: {len(path)}")
            print(" -> ".join(path))
        else:
            print(f"No path found from {InitialNode} to {FinalNode}")

def main():
    STC_Metro = Graph() #create the subway graph
  
    for line_data in lines.lineas_with_data.values():
        for station_name, station_info in line_data.items(): #iterate through each station in each line
            if station_name not in STC_Metro.vertices: #check if station is already in the graph
                STC_Metro.AddVertice(station_name, station_info) #add station to the graph if not already present

    for line_data in lines.lineas_with_data.values():
        for station_name, station_info in line_data.items():
            neighbors_actuales = STC_Metro.vertices[station_name]["neighbors"] #get current neighbors of the station
            for neighbor, distance in station_info["neighbors"]: #iterate through the neighbors of the station
                if (neighbor, distance) not in neighbors_actuales: #check if neighbor is already in the list
                    neighbors_actuales.append((neighbor, distance)) #add neighbor if not already present

    #Route 1
    InitialState1 = "Pantitlán"
    FinalStation1 = "Barranca del Muerto"

    #Route 2
    InitialState2 = "Tacubaya"
    FinalStation2 = "Pantitlán"

    #Route 3
    InitialState3 = "Pantitlán"
    FinalStation3 = "Tacubaya"
    
    #Route 4
    InitialState4 = "Universidad"
    FinalStation4 = "Canal del Norte"

    #Route 5
    InitialState5 = "Ciudad Azteca"
    FinalStation5 = "Mixcoac"

    #Route 6
    InitialState6 = "Observatorio"
    FinalStation6 = "La Paz"

    #Route 7
    InitialState7 = "Politécnico"
    FinalStation7 = "Mexicaltzingo"

    #Route 8
    InitialState8 = "Santa Anita"
    FinalStation8 = "Tacuba"

    #Route 9
    InitialState9 = "Constitución de 1917"
    FinalStation9 = "El Rosario"

    #Route 10
    InitialState10 = "Zapata"
    FinalStation10 = "Pantitlán"

    #First path
    print(f"\n\033[0m\033[104m* Path:\033[0m {InitialState1.upper()} to {FinalStation1.upper()}")
    STC_Metro.FindPathDijkstra(InitialState1, FinalStation1)
    print("\nHappy travels\n-----------------------")

    #Second Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState2.upper()} to {FinalStation2.upper()}")
    STC_Metro.FindPathDijkstra(InitialState2, FinalStation2)
    print("\nHappy travels!\n-----------------------")

    #Third Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState3.upper()} to {FinalStation3.upper()}")
    STC_Metro.FindPathDijkstra(InitialState3, FinalStation3)
    print("\nHappy travels!\n-----------------------")

#Fourth Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState4.upper()} to {FinalStation4.upper()}")
    STC_Metro.FindPathDijkstra(InitialState4, FinalStation4)
    print("\nHappy travels!\n-----------------------")

    #Fifth Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState5.upper()} to {FinalStation5.upper()}")
    STC_Metro.FindPathDijkstra(InitialState5, FinalStation5)
    print("\nHappy travels!\n-----------------------")

    #Sixth Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState6.upper()} to {FinalStation6.upper()}")
    STC_Metro.FindPathDijkstra(InitialState6, FinalStation6)
    print("\nHappy travels!\n-----------------------")

    #Seventh Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState7.upper()} to {FinalStation7.upper()}")
    STC_Metro.FindPathDijkstra(InitialState7, FinalStation7)
    print("\nHappy travels!\n-----------------------")

    #Eighth Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState8.upper()} to {FinalStation8.upper()}")
    STC_Metro.FindPathDijkstra(InitialState8, FinalStation8)
    print("\nHappy travels!\n-----------------------")

    #Ninth Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState9.upper()} to {FinalStation9.upper()}")
    STC_Metro.FindPathDijkstra(InitialState9, FinalStation9)
    print("\nHappy travels!\n-----------------------")

    #Tenth Path
    print(f"\n\n\033[0m\033[104m* Path:\033[0m {InitialState10.upper()} to {FinalStation10.upper()}")
    STC_Metro.FindPathDijkstra(InitialState10, FinalStation10)
    print("\nHappy travels!\n-----------------------")
    
main()