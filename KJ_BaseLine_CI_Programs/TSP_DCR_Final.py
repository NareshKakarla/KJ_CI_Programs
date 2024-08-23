import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import random
from math import radians, sin, cos, sqrt, atan2
from call_prop import call_prop_fun
import scipy.stats as stats

random.seed(40)
np.random.seed(40)

coordinates = np.array([[45.86067094, 87.78679037],
 [31.5763628 , 75.64780588],
 [60.92768371, 58.53217096],
 [28.50233976 ,53.3327862 ],
 [57.28743001, 79.0486658 ]])

def generate_points(N, min_distance=12, max_distance=40, area_size=100, max_attempts=10000):
    points = []
    attempts = 0
    while len(points) < N and attempts < max_attempts:
        candidate = (random.uniform(0, area_size), random.uniform(0, area_size))
        if len(points) == 0 or all(min_distance <= np.sqrt((candidate[0]-p[0])**2 + (candidate[1]-p[1])**2) <= max_distance for p in points):
            points.append(candidate)
        attempts += 1
    return np.array(points)

def compute_distance_matrix(coordinates):
    num_locations = len(coordinates)
    distances = np.zeros((num_locations, num_locations))
    for i in range(num_locations):
        for j in range(num_locations):
            distances[i, j] = np.linalg.norm(coordinates[i] - coordinates[j])
    return distances

def solve_tsp(distance_matrix):
    n = len(distance_matrix)
    best_path = None
    best_distance = float('inf')
    
    for path in permutations(range(1, n)):
        path = (0,) + path + (0,)
        distance = sum(distance_matrix[path[i]][path[i+1]] for i in range(n))
        if distance < best_distance:
            best_distance = distance
            best_path = path
    
    return best_path

def Cvalue(i1):
    if 0 <= i1 < 2000:
        return 3
    elif 2000 <= i1 < 4000:
        return 6
    elif 4000 <= i1 < 6000:
        return 11
    elif 6000 <= i1 < 8000:
        return 20
    elif 8000 <= i1 < 10000:
        return 37
    elif i1 >= 10000:
        return 68

def Success_Prob(dist):
    return max(0, min(1, 1 - dist / 10000))

def Run_a_sample_path(V, initial_location, P):
    temp_V = V
    data_sample = np.random.choice([0, 1], p=[1-P, P])
    Prop_algo_Param = call_prop_fun(V, initial_location, P)
    dist_travelled = initial_location - Prop_algo_Param[0]
    time_to_fly = 2 * dist_travelled / 50
    V_after_flight = max(temp_V - time_to_fly, 0)
    temp_V = V_after_flight
    beta = Success_Prob(Prop_algo_Param[0])
    C = Cvalue(Prop_algo_Param[0])
    attempts = 0
    output  = 0
    while temp_V >= C and P > C/(beta*temp_V):
        channel_Sample = np.random.choice([0, 1], p=[1-beta, beta])
        output = channel_Sample * data_sample
        temp_V = temp_V - C
        attempts = attempts + 1
        if output == 1:
            break
        P_new = (P * (1-beta)) / (P * (1-beta) + (1 - P))
        P = P_new
    return (temp_V, attempts, Prop_algo_Param[0], output)

def can_return_home(current_position, home_position, remaining_energy):
    dist_to_home = np.linalg.norm(home_position - current_position) * 1000  # Convert to meters
    energy_needed = 2 * dist_to_home / 50  # Assuming 50 m/s speed and round trip
    return remaining_energy >= energy_needed

distance_matrix = compute_distance_matrix(coordinates)

def TSP_attempts(runs, Initial_V, P_init):
    num_nodes = len(coordinates)
    service_requests = []
    residual_energies = []
    data_collection_rates = []
    
    tsp_path = solve_tsp(distance_matrix)
    
    for j in range(runs):
        V = Initial_V
        Req_serviced = 0
        current_position = coordinates[0]
        home_position = coordinates[0]
        node_successes = np.zeros(num_nodes)
        
        for i in range(1, len(tsp_path)):
            next_location = tsp_path[i]
            distance = distance_matrix[tsp_path[i-1]][next_location]
            P = P_init
            temporary_V, attempts, dist_away, otpt = Run_a_sample_path(V, distance*1000, P)
            direction = coordinates[next_location] - current_position
            direction = direction / np.linalg.norm(direction)
            optimal_distance = distance - dist_away/1000
            potential_uav_position = current_position + direction * optimal_distance
            
            if can_return_home(potential_uav_position, home_position, temporary_V):
                if otpt == 1:  # Successful data collection
                    node_successes[next_location] = 1
                Req_serviced += 1
                current_position = potential_uav_position
                V = temporary_V
            else:
                break
        
        service_requests.append(Req_serviced)
        residual_energies.append(V)
        data_collection_rates.append(np.sum(node_successes) / (num_nodes - 1))
    
    return service_requests, residual_energies, data_collection_rates
