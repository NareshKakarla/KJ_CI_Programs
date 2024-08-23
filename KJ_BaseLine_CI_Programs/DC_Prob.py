import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import random
from New_P_Success import Success_Prob
from call_prop import call_prop_fun
import scipy.stats as stats

random.seed(40)
np.random.seed(40)

coordinates = np.array([[45.86067094, 87.78679037],
 [31.5763628 , 75.64780588],
 [60.92768371, 58.53217096],
 [28.50233976 ,53.3327862 ],
 [57.28743001, 79.0486658 ]])

def next_closest_location(current_position, coordinates, visited):
    distances = np.array([np.linalg.norm(current_position - coord) for coord in coordinates])
    unvisited_indices = np.where(np.logical_not(visited))[0]
    if len(unvisited_indices) == 0:
        return None, None
    closest_unvisited = unvisited_indices[np.argmin(distances[unvisited_indices])]
    return closest_unvisited, distances[closest_unvisited]

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
    P_temp = P*beta
    output = 0
    while temp_V >= C and P > C/(beta*temp_V) :
        channel_Sample = np.random.choice([0, 1], p=[1-beta, beta])
        output = channel_Sample * data_sample
        temp_V = temp_V - C
        attempts = attempts + 1
        if output == 1:
            break
        P_total = P_temp + (1-P_temp)
        P_new = (P * (1-beta)) / (P * (1-beta) + (1 - P))
        P = P_new
    return (temp_V, attempts, Prop_algo_Param[0], output, P, beta)

def can_return_home(current_position, home_position, remaining_energy):
    dist_to_home = np.linalg.norm(home_position - current_position) * 1000  # Convert to meters
    energy_needed = 2 * dist_to_home / 50  # Assuming 50 m/s speed and round trip
    return remaining_energy >= energy_needed

# Main execution
def Optimal_attempts_fun(runs, Initial_V, P_init):
    num_nodes = len(coordinates)
    service_requests = []
    residual_energies = []
    data_collection_rates = []
    
    for i in range(runs):
        visited = [False] * len(coordinates)
        V = Initial_V
        current_position = coordinates[0]
        uav_positions = [current_position]
        visited[0] = True
        home_position = coordinates[0]
        Req_serviced = 0
        node_successes = np.zeros(num_nodes)
        
        while V > 0 and not all(visited):
            next_location, distance = next_closest_location(current_position, coordinates, visited)
            if next_location is None:
                break
            P = P_init
            temporary_V, attempts, dist_away, otpt, P4, beta = Run_a_sample_path(V, distance*1000, P)
            direction = coordinates[next_location] - current_position
            direction = direction / np.linalg.norm(direction)
            optimal_distance = distance - dist_away/1000
            potential_uav_position = current_position + direction * optimal_distance
            
            if can_return_home(potential_uav_position, home_position, temporary_V):
                if otpt == 1:  # Successful data collection
                    node_successes[next_location] = 1
                Req_serviced += 1
                uav_position = potential_uav_position
                uav_positions.append(uav_position)
                current_position = uav_position
                visited[next_location] = True
                V = temporary_V
            else:
                break
        
        service_requests.append(Req_serviced)
        residual_energies.append(V)
        data_collection_rates.append(np.sum(node_successes) / (num_nodes - 1))
    
    return service_requests, residual_energies, data_collection_rates

# def calculate_confidence_interval(data, confidence=0.95):
#     n = len(data)
#     mean = np.mean(data)
#     se = stats.sem(data)
#     ci = se * stats.t.ppf((1 + confidence) / 2, n - 1)
#     return mean, ci

# if __name__ == "__main__":
#     runs = 100
#     Initial_V = 500
#     P_init = 0.2
    
#     service_requests, residual_energies, data_collection_rates = Optimal_attempts_fun(runs, Initial_V, P_init)
    
#     metrics = [service_requests, residual_energies, data_collection_rates]
#     metric_names = ["Service Requests", "Residual Energy", "Data Collection Rate"]
    
#     for metric, name in zip(metrics, metric_names):
#         mean, ci = calculate_confidence_interval(metric)
#         print(f"{name}: {mean:.4f} ± {ci:.4f}")

#     # Plotting
#     fig, axs = plt.subplots(3, 1, figsize=(10, 15))
#     for i, (metric, name) in enumerate(zip(metrics, metric_names)):
#         mean, ci = calculate_confidence_interval(metric)
#         axs[i].hist(metric, bins=20, edgecolor='black')
#         axs[i].axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Mean: {mean:.4f}')
#         axs[i].axvline(mean-ci, color='g', linestyle='dashed', linewidth=2, label=f'95% CI')
#         axs[i].axvline(mean+ci, color='g', linestyle='dashed', linewidth=2)
#         axs[i].set_title(f"Distribution of {name}")
#         axs[i].set_xlabel(name)
#         axs[i].set_ylabel("Frequency")
#         axs[i].legend()
    
#     plt.tight_layout()
#     plt.savefig("Optimal_metrics_distribution.pdf")
#     plt.show()