import lines 
import heapq #Priority queue


class Nodo():
    def __init__(self, name):
        self.name = name 
        self.neighbors = [] 
        self.dist = -1
        self.father = None
        self.f = -1        

    def Addneighbors(self, neighbor, distance):
        if neighbor != self.name and neighbor not in self.neighbors: 
            self.neighbors.append((neighbor, distance)) 



class Graph:
    def __init__(self):
        self.vertices = {}
        self.fathers = {}

    def AddVertice(self, name_station, datos_station):
        self.vertices[name_station] = datos_station

    def Dijkstra(self, InitialNode, FinalNode):

        self.fathers.clear()
        
        g_score = {name: float('inf') for name in self.vertices}
        g_score[InitialNode] = 0


        priority = [(g_score[InitialNode], InitialNode)]

        while priority:
            _, current_node_name = heapq.heappop(priority)

            if current_node_name == FinalNode:
                path = []
                distance_Total = g_score[FinalNode]
                temp = FinalNode
                while temp in self.fathers:
                    path.append(temp)
                    temp = self.fathers[temp]
                path.append(InitialNode)
                path.reverse()
                return path, distance_Total

            for neighbor_name, distance in self.vertices[current_node_name]["neighbors"]:
                g_score_final = g_score[current_node_name] + distance
                
                if g_score_final < g_score.get(neighbor_name, float('inf')):
                    self.fathers[neighbor_name] = current_node_name
                    g_score[neighbor_name] = g_score_final
                    heapq.heappush(priority, (g_score[neighbor_name], neighbor_name))
        
        return None, float('inf')
    
    def FindPathDijkstra(self, InitialNode, FinalNode):
        print(f"\n\033[105m*\033[0mResults using Dijkstra (Shortest path in distance):")
        if InitialNode not in self.vertices or FinalNode not in self.vertices:
            print(f"One or more subway stations weren't found.")
            return

        path, distance = self.Dijkstra(InitialNode, FinalNode)
        if path:
            print(f"total distance: {distance / 1000:.2f} km")
            print(f"Number of stations: {len(path)}")
            print(" -> ".join(path))
        else:
            print(f"No path found from {InitialNode} to {FinalNode}")

def main():
    STC_Metro = Graph()
  
    for line_data in lines.lineas_with_data.values():
        for station_name, station_info in line_data.items():
            if station_name not in STC_Metro.vertices:
                STC_Metro.AddVertice(station_name, station_info)

    for line_data in lines.lineas_with_data.values():
        for station_name, station_info in line_data.items():
            neighbors_actuales = STC_Metro.vertices[station_name]["neighbors"]
            for neighbor, distance in station_info["neighbors"]:
                if (neighbor, distance) not in neighbors_actuales:
                    neighbors_actuales.append((neighbor, distance))

    #Route 1
    InitialState1 = "Pantitlán"
    FinalStation1 = "Barranca del Muerto"

    #Route 2
    InitialState2 = "Tacubaya"
    FinalStation2 = "Pantitlán"

    #Route 3
    InitialState3 = "Pantitlán"
    FinalStation3 = "Tacubaya"

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

main()