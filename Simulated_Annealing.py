import numpy as np

def read_tsp_file(file_path):
    #  extract city coordinates
    with open(file_path, 'r') as file:
        lines = file.readlines()

    coordinates_section = False
    coordinates = []

    for line in lines:
      
        if line.startswith("NODE_COORD_SECTION"):
            coordinates_section = True
            continue
        # Break when reaching the end of the file
        elif line.startswith("EOF"):
            break

        if coordinates_section:
            # Parse and store city coordinates
            parts = line.split()
            coordinates.append((int(parts[0]), float(parts[1]), float(parts[2])))

    return coordinates

def calculate_distance(coord1, coord2):
    # Euclidean distance between two coordinates
    x1, y1 = coord1[1], coord1[2]
    x2, y2 = coord2[1], coord2[2]
    distance = round(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    return distance

def Dist_full_path(path, distances):
    #  total distance of a given path using a distance matrix
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distances[path[i]][path[i + 1]]
    return total_distance

def Simulated_Annealing(coordinates, Temp=11000, cooling_rate=0.99, stopping_Temp=1e-5, num_runs=10, distances=[]):
    num_cities = len(coordinates)

    if num_cities < 3:
        return list(range(num_cities)), 0  #case with less than 3 cities

    best_path = None
    Min_distance = float('inf')

    for _ in range(num_runs):
        # Initialize a random path
        path = np.random.permutation(num_cities)
        current_distance = Dist_full_path(list(path) + [path[0]], distances)

        while Temp > stopping_Temp:
            # Randomly swap two cities in the path
            i, j = np.random.choice(num_cities, size=2, replace=False)
            new_path = path.copy()
            new_path[i], new_path[j] = new_path[j], new_path[i]

            new_distance = Dist_full_path(list(new_path) + [new_path[0]], distances)
            delta_distance = new_distance - current_distance

            # Accept the new path with a probability determined by the annealing schedule
            if delta_distance < 0 or np.random.rand() < np.exp(-delta_distance / Temp):
                path = new_path
                current_distance = new_distance

                # Update the best path if a shorter path is found
                if current_distance < Min_distance:
                    best_path = path.copy()
                    Min_distance = current_distance

            # Reduce temperature according to the cooling rate
            Temp *= cooling_rate

    return list(best_path) + [best_path[0]], Min_distance

# filenames = ["Atlanta.tsp", "Berlin.tsp", "Boston.tsp", "Champaign.tsp", "Cincinnati.tsp", "Denver.tsp", "NYC.tsp", "Philadelphia.tsp", "Roanoke.tsp", "SanFrancisco.tsp", "Toronto.tsp", "UKansasState.tsp","UMissouri.tsp" ]

# if _name_ == "_main_":
#     for filename in filenames:
#         file_path = filename
#         city_coordinates = read_tsp_file(file_path)

#         # Calculate distances
#         distances = np.zeros((len(city_coordinates) + 1, len(city_coordinates) + 1), dtype=int)
#         for i in range(len(city_coordinates)):
#             for j in range(i + 1, len(city_coordinates)):
#                 distances[i][j] = distances[j][i] = calculate_distance(city_coordinates[i], city_coordinates[j])

#         # Apply simulated annealing to find the best path
#         best_path, Min_distance = Simulated_Annealing(city_coordinates, num_runs=10)

#         # Print results
#         print("Best TSP path for {}: {}".format(filename, best_path))
#         print("Total Distance:", Min_distance)