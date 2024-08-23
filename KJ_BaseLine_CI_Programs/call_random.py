import numpy as np

# Coordinates of the locations
# coordinates = np.array([
# [15.33, 47.26],
# [10.68, 51.74],
# [21.72, 45.12],
# [24.48, 41.42]])

coordinates  =np.array([
[34.57, 78.19],
 [43.84, 81.29],
 [31.96, 85.12],
 [38.71, 74.36]])

# Function to compute pairwise distances
def compute_distance_matrix(coordinates):
    num_locations = len(coordinates)
    distances = np.zeros((num_locations, num_locations))

    for i in range(num_locations):
        for j in range(num_locations):
            distances[i, j] = np.linalg.norm(coordinates[i] - coordinates[j])

    return distances

# Compute distance matrix
distances = compute_distance_matrix(coordinates)

# Print the distance matrix
print("Distance Matrix:")
print(distances*1000)
