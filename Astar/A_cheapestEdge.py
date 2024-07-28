import heapq
import csv
import random
import time
import sys

# Start measuring time
start_cpu_time = time.process_time()
start_realworld_time = time.time()

##################################################################

class Graph:

    def __init__(self, edge_list, heuristic_list):

        self.adj_list = {}
        self.heuristic_list = {}

        for (src, dest, weight) in edge_list:

            if src not in self.adj_list:
                self.adj_list[src] = []

            if dest not in self.adj_list:
                self.adj_list[dest] = []
            
            self.adj_list[src].append((dest, weight))

        for node, h_value in heuristic_list:

            self.heuristic_list[node] = h_value  

##################################################################

def MST_cost_generator(graph, path, n):

    all_numbers = set(range(1, n + 1))
    used_numbers = set(path)
    numbers_left = list(all_numbers - used_numbers)

    # generate the mst and get cost
    total_cost = 0
    in_mst = set()
    edges = []

    # add all edges (relevant)
    for vertex in numbers_left:
        for dst, weight in graph.adj_list[vertex]:
            if vertex < dst:  # To avoid duplicate edges
                edges.append((weight, vertex, dst))
    
    # grab cheapest edges for MST (Prim's)
    edges.sort()


    for weight, src, dst in edges:
            
        if (src not in numbers_left or dst not in numbers_left):
            continue

        if (src in in_mst and dst in in_mst):
            continue

        total_cost += weight

        in_mst.add(src)
        in_mst.add(dst)

        if len(in_mst) == len(numbers_left):
            break

    return total_cost

##################################################################

def calculate_path_cost(graph, path):

    total_cost = 0

    for i in range(len(path) - 1):
        
        src = path[i]
        
        dst = path[i + 1]

        for dest, cost in graph.adj_list[src]:

            if dest == dst:

                total_cost += cost

                break

    return total_cost

##################################################################


def A_cheapestEdge(graph, start_node, dest_node, n):

    visited = 0

    # Priority queue contains tuples of (cumulative cost, node, path)
    queue = [(0, start_node, [start_node])]  
    heapq.heapify(queue)
    
    while queue:

        # Get first (cost, node, path)
        current_cost, current, path = heapq.heappop(queue)

        # Check upper bound time
        '''
        current_realworld_time = time.time()
        if current_realworld_time - start_realworld_time > time_limit:
            print(f"Time limit for {n} exceeded.")
            current_cost = calculate_path_cost(graph, path)
            return path + [-1], current_cost, visited
        '''

        visited += 1

        if current == dest_node and len(path) == n + 1:
            #print(f"Destination node {dest_node} found!")
            #print(f"Total edge length: {current_cost}")
            #print(f"Path: {' -> '.join(map(str, path))}")
            return path, calculate_path_cost(graph, path), visited

        # For all neighbors generate MST, heuristic, enque
        for neighbor, weight in graph.adj_list[current]:

            if neighbor not in path or (neighbor == start_node and len(path) == n):

                if (neighbor != dest_node):
                    heuristic_weight = MST_cost_generator(graph, path + [neighbor], n)
                else:
                    heuristic_weight = 0

                heapq.heappush(queue, (current_cost + weight + heuristic_weight, neighbor, path + [neighbor]))

        #print(f"Visited nodes: {visited}")
            
        #else:
            
            #print(f"Node {current} already visited")
        
        #input("Press Enter to continue...")
        #print(f"Current queue: {queue}")
        #print("---------------------")

    return None, -1, visited  # If there is no path from start_node to dest_node
    
##################################################################

input_stream = sys.stdin

edge_list = []
heuristic_list = []

#with open("Graphs/graph2.txt", "r") as file:

    #n = int(file.readline().strip())
n = int(input_stream.readline().strip()) 

for row in range(n):

    #line = file.readline().strip()
    line = input_stream.readline().strip()
    
    numbers = line.split()

    heuristic_list.append((row + 1, 0))

    for col in range(n):

        if (col >= row):

            if (row == col):
                continue

            value = int(numbers[col])

            edge_list.append((row + 1, col + 1, value))
            edge_list.append((col + 1, row + 1, value))

#print(edge_list)

g = Graph(edge_list, heuristic_list)

##################################################################

def append_costs_to_csv(data, filename='A_cheapestEdge.csv'):

    with open(filename, mode='a', newline='') as file:

        writer = csv.writer(file)

        writer.writerow(data)

##################################################################

start_node = 1
goal_node = 1

'''
if (n <= 150):
    time_limit = 10800 # 3 hours

if (n <= 100):
    time_limit = 7200 # 2 hours

if (n <= 30):
    time_limit = 3600 # 1 hours
'''

path, path_length, nodes_expanded = A_cheapestEdge(g, start_node, goal_node, n)

# Stop measuring time
end_cpu_time = time.process_time()
end_realworld_time = time.time()

# Calculate times
cpu_time = end_cpu_time - start_cpu_time
realworld_time = end_realworld_time - start_realworld_time

# cost, nodes, cpu, real-run-time
data = [path, path_length, nodes_expanded, cpu_time, realworld_time]

#print(path)
#print(data)

append_costs_to_csv(data)