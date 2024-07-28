import heapq
import csv
import math
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

def generate_random_path(n):

    path = list(range(2, n + 1))

    random.shuffle(path)

    return [1] + path + [1]

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

def temperature_function(temperature, cooling_ratio):
    return temperature * cooling_ratio

##################################################################

def simuAnnealing(graph, n, restarts, initial_temperature, cooling_ratio):

    visited = 0
    best_path_cost = sys.maxsize

    for restart in range(0, restarts):

        # generate a random final state, its cost, and reset the temperature for SA on this restart
        current_path = generate_random_path(n)
        current_cost = calculate_path_cost(graph, current_path)
        temperature = initial_temperature

        while temperature > 0: 
            temperature = temperature_function(temperature, cooling_ratio)
            restart += 1

            if (temperature <= 1):
                # if this final path is better than our best path, save it
                if (current_cost < best_path_cost):
                    best_path = current_path
                    best_path_cost = current_cost
                done = True
                break

            # generate a random new state
            visited += 1
            i, j = random.sample(range(1, n), 2)
            neighbor_path = current_path[:]
            neighbor_path[i], neighbor_path[j] = neighbor_path[j], neighbor_path[i]
            neighbor_cost = calculate_path_cost(graph, neighbor_path)
            deltaE = current_cost - neighbor_cost

            # accept, or conditionally accept state
            if (deltaE > 0):
                current_path = neighbor_path
                current_cost = neighbor_cost
                #print(current_path)
            else:
                #print(math.exp(deltaE/temperature))
                if (math.exp(deltaE/temperature) > random.random()):
                    current_path = neighbor_path
                    current_cost = neighbor_cost

            # repeat

    return best_path, best_path_cost, visited

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

def append_costs_to_csv(data, filename='simuAnnealing.csv'):

    with open(filename, mode='a', newline='') as file:

        writer = csv.writer(file)

        writer.writerow(data)

##################################################################

restarts = 5
initial_temperature = 500
cooling_ratio = .95
path, path_length, nodes_expanded = simuAnnealing(g, n, restarts, initial_temperature, cooling_ratio)

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