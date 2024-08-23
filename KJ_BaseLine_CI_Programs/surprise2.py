import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import random
from math import radians, sin, cos, sqrt, atan2
from New_P_Success import Success_Prob
from call_prop import call_prop_fun
from find_coord import call_find_coord

random.seed(40)
np.random.seed(40)
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 12,
    'font.weight': 'bold',
    'mathtext.fontset': 'stix'
})


def generate_points(N, min_distance=12, max_distance=40, area_size=100, max_attempts=10000):
    points = []
    attempts = 0
    while len(points) < N and attempts < max_attempts:
        candidate = (random.uniform(0, area_size), random.uniform(0, area_size))
        if len(points) == 0 or all(min_distance <= np.sqrt((candidate[0]-p[0])**2 + (candidate[1]-p[1])**2) <= max_distance for p in points):
            points.append(candidate)
        attempts += 1
    if len(points) < N:
        print(f"Warning: Could only generate {len(points)} points out of {N} requested.")
    return np.array(points)

# def compute_distance_matrix(coordinates):
#     num_locations = len(coordinates)
#     distances = np.zeros((num_locations, num_locations))
#     for i in range(num_locations):
#         for j in range(num_locations):
#             distances[i, j] = np.linalg.norm(coordinates[i] - coordinates[j])
#     return distances

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
    print(" Inside run a sample = ", V, initial_location)
    Prop_algo_Param = call_prop_fun(V, initial_location, P)
    print(" Prop_algo_param = ", Prop_algo_Param)
    dist_travelled = initial_location - Prop_algo_Param[0]
    time_to_fly = 2 * dist_travelled / 50
    V_after_flight = max(temp_V - time_to_fly, 0)
    temp_V = V_after_flight
    beta = Success_Prob(Prop_algo_Param[0])
    C = Cvalue(Prop_algo_Param[0])
    attempts = 0
    while temp_V >= C and P > C/(beta*temp_V) :
        channel_Sample = np.random.choice([0, 1], p=[1-beta, beta])
        output = channel_Sample * data_sample
        temp_V = temp_V - C
        attempts = attempts + 1
        if output == 1:
            print("Break",attempts)
            break
        P_new = (P * (1-beta)) / (P * (1-beta) + (1 - P))
        P = P_new
    return (temp_V, attempts, Prop_algo_Param[0])

# def haversine_distance(lat1, lon1, lat2, lon2):
#     R = 6371  # Earth's radius in kilometers
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1-a))
#     distance = R * c
#     return distance


def plot_uav_path(coordinates, uav_positions):
    plt.figure(figsize=(6, 6))  # Reduced figure size
    
    # Plot nodes and their 6km radius
    for i, (x, y) in enumerate(coordinates):
        
        plt.plot(x, y, 'ro', markersize=8)  # Node markers
        if(i!=0):
            circle = plt.Circle((x, y), 8, fill=True, color='royalblue', alpha=0.4)  # Shaded, more visible circles
            plt.gca().add_artist(circle)
            # circle_edge = plt.Circle((x, y), 6, fill=False, color='black', alpha=0.4, linewidth=2)  # Circle edge
            # plt.gca().add_artist(circle_edge)
            plt.text(x, y, f'CH{i}', fontsize=18, ha='right', va='bottom', fontweight='bold') 
        if(i==0):
            plt.text(x, y, f'H   ', fontsize=18, ha='right', va='top', fontweight='bold')

    # Plot UAV path
    uav_x, uav_y = zip(*uav_positions)
    plt.plot(uav_x, uav_y, 'b-', linewidth=2, label='UAV Path')
    plt.plot(uav_x, uav_y, 'go', markersize=6, label='UAV Positions')  # Slightly smaller UAV position markers

    # Calculate and display distances between consecutive UAV positions
    for i in range(len(uav_positions) - 1):
        x1, y1 = uav_positions[i]
        x2, y2 = uav_positions[i+1]
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        plt.text(mid_x, mid_y, f'{distance:.2f}', fontsize=10, ha='center', va='bottom',  fontweight='bold',bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    plt.xlim(20, 70)
    plt.ylim(40, 100)
    plt.xticks(fontsize=14,fontweight = 'bold')
    plt.yticks(fontsize=14, fontweight = 'bold')
    plt.xlabel('X (km)', fontsize=15, fontweight = 'bold')
    plt.ylabel('Y (km)', fontsize=15, fontweight = 'bold')
    plt.title(f' Initial Energy = {600} KJ, P = {P_init}', fontsize=18,fontweight = 'bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Create a custom legend
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='red', marker='o', linestyle='None', markersize=6),
                    Line2D([0], [0], color='blue', linestyle='-', linewidth=1.5),
                    Line2D([0], [0], color='green', marker='o', linestyle='None', markersize=6),
                    Line2D([0], [0], color='royalblue', marker='o', linestyle='None', markersize=8, markerfacecolor='none')]
    plt.legend(custom_lines, ['CH', 'UAV Path', 'UAV Positions', 'LoRa coverage'],  loc='best' , fontsize=18, prop={'weight': 'bold'})
    plt.savefig("UAV_Tour.pdf")
    plt.tight_layout()
    plt.show()



def can_return_home(current_position, home_position, remaining_energy):
    dist_to_home = np.linalg.norm(home_position - current_position) * 1000  # Convert to meters
    energy_needed = 2 * dist_to_home / 50  # Assuming 50 m/s speed and round trip
    return remaining_energy >= energy_needed

# Main execution
N = int(input("Enter the number of points: "))
coordinates = generate_points(N)
print("Generated coordinates:")
print(coordinates)

Initial_V = 3529
P_init = 0.8

# distance_matrix = compute_distance_matrix(coordinates)
# print("Distance matrix:")
# print(distance_matrix)

visited = [False] * len(coordinates)
V = Initial_V
current_position = coordinates[0]
uav_positions = [current_position]
visited[0] = True
home_position = coordinates[0]
Req_serviced = 0
while V > 0 and not all(visited):
    next_location, distance = next_closest_location(current_position, coordinates, visited)
    print(f"Next location = {next_location}, Initial distance = {distance:.2f} km")
    if next_location is None:
        break
    P = P_init

    temporary_V, attempts, dist_away = Run_a_sample_path(V, distance*1000, P)
    print(f"temp_V = {temporary_V:.2f}, dist_away = {dist_away:.2f} m")

    direction = coordinates[next_location] - current_position
    direction = direction / np.linalg.norm(direction)
    optimal_distance = distance - dist_away/1000
    print(f"Optimal distance to fly = {optimal_distance:.2f} km")
    potential_uav_position = current_position + direction * optimal_distance

    # Check if UAV can return home from the potential new position
    if can_return_home(potential_uav_position, home_position, temporary_V):
        Req_serviced = Req_serviced + 1
        uav_position = potential_uav_position
        print(f"UAV Position = ({uav_position[0]:.2f}, {uav_position[1]:.2f})")
        uav_positions.append(uav_position)
        current_position = uav_position
        visited[next_location] = True
        V = temporary_V
        print(f"Remaining energy: V = {V:.2f}")
    else:
        print("Not enough energy to safely return home. Ending mission.")
        break

    print("---")

print(" Request Service = ",Req_serviced)
# After the loop, ensure UAV returns home
if current_position is not home_position:
    direction_home = home_position - current_position
    dist_to_home = np.linalg.norm(direction_home)
    if can_return_home(current_position, home_position, V):
        uav_positions.append(home_position)
        print("UAV successfully returned home.")
    else:
        print("Warning: UAV doesn't have enough energy to return home!")

# Plot the path
plot_uav_path(coordinates, uav_positions)

# Print UAV positions
print("\nUAV positions:")
for i, pos in enumerate(uav_positions):
    print(f"Position {i}: ({pos[0]:.2f}, {pos[1]:.2f})")

# Print distances between UAV positions
print("\nDistances between UAV positions:")
for i in range(len(uav_positions) - 1):
    distance = np.linalg.norm(np.array(uav_positions[i+1]) - np.array(uav_positions[i]))
#     print(f"Distance between position {i} and {i+1}: {distance:.2f} km")
