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

    # Check for bad paths
    seen = set()
    for i in range(len(path) - 1):
        src = path[i]
        if src in seen:
            return sys.maxsize
        seen.add(src)

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

def random_weighted_parent(probabilty_ranges):

    probability = random.random()

    for parent_id, parent_probability in probabilty_ranges:

        if probability <= parent_probability:
            return parent_id
        
    return parent_id

##################################################################

def reproduce(parent1, parent2):

    path1 = parent1['path']
    path2 = parent2['path']
    n = len(path1)

    start, end = sorted(random.sample(range(1, n - 1), 2))

    child_path = [None] * n
    child_path[0] = path1[0]
    child_path[-1] = path1[-1]

    child_path[start:end + 1] = path1[start:end + 1]

    p2_index = 1
    for i in range(1, n - 1):
        if child_path[i] is None:
            while path2[p2_index] in child_path:
                p2_index += 1
            child_path[i] = path2[p2_index]
            p2_index += 1

    return {
        'path': child_path,
        'cost': 0,
        'probability': 0
    }

##################################################################

def mutate(child_path):
    i, j = random.sample(range(1, len(child_path) - 1), 2)
    child_path[i], child_path[j] = child_path[j], child_path[i]
    return child_path

##################################################################

def getCheapestChild(parents):

    min_cost = sys.maxsize
    cheapest_child_path = None

    for parent_id in parents:
        if parents[parent_id]['cost'] <= min_cost:
            min_cost = parents[parent_id]['cost']
            cheapest_child_path = parents[parent_id]['path']

    return cheapest_child_path

##################################################################

def genetic(graph, n, generations, mutation_rate):

    visited = 0
    best_path_cost = sys.maxsize

    # initial population
    parents = {}
    total_inverse_cost = 0
    for parent_id in range(0, 100):
        visited += 1
        parent_path = generate_random_path(n)
        cost = calculate_path_cost(graph, parent_path)
        inverse_cost = 1 / cost
        total_inverse_cost += inverse_cost
        parents[parent_id] = {
            'path': parent_path,
            'cost': cost,
            'probability': 0
        }
    # calculate fitness values and probability ranges
    cumulative_probability = 0
    probabilty_ranges = []
    for parent_id in parents:
        cost = parents[parent_id]['cost']
        inverse_cost = 1 / cost
        parents[parent_id]['probability'] = inverse_cost / total_inverse_cost
        cumulative_probability += parents[parent_id]['probability']
        probabilty_ranges.append((parent_id, cumulative_probability))

    # perform generations of genetic algorithm
    for generation in range(0, generations):

        next_parents = {}
        total_inverse_cost = 0

        # selection 100 new children
        for child_id in range(0, 250):
            visited += 1

            parent1_id = random_weighted_parent(probabilty_ranges)
            parent2_id = random_weighted_parent(probabilty_ranges)

            parent1 = parents[parent1_id]
            parent2 = parents[parent2_id]

            child = reproduce(parent1, parent2)
            if (random.random() <= mutation_rate):
                child['path'] = mutate(child['path'])
            child['cost'] = calculate_path_cost(graph, child['path'])
            next_parents[child_id] = child

            total_inverse_cost += 1 / child['cost']

        # calculate fitness for children
        for child_id in next_parents:
            next_parents[child_id]['probability'] = (1 / next_parents[child_id]['cost']) / total_inverse_cost

        # repeat
        parents = next_parents

    cheapest_child_path = getCheapestChild(parents)
    cheapest_path_cost = calculate_path_cost(graph, cheapest_child_path)
    return cheapest_child_path, cheapest_path_cost, visited

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

def append_costs_to_csv(data, filename='genetic.csv'):

    with open(filename, mode='a', newline='') as file:

        writer = csv.writer(file)

        writer.writerow(data)

##################################################################

generations = 125
mutation_rate = .05
path, path_length, nodes_expanded = genetic(g, n, generations, mutation_rate)

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