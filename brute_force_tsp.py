import itertools
import math
import time

# Function to calculate Euclidean distance between two points
def euclidean_distance(point1, point2):
    return round(math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))

def total_distance(path, points):
    # Calculate the total distance of a path
    return sum(euclidean_distance(points[path[i]], points[path[i+1]]) for i in range(len(path)-1))


# Exact brute-force solution with a time cut-off
def brute_force_tsp(points, time_limit):
    start_time = time.time()
    n = len(points)
    best_path = None
    best_distance = float('inf')

    for path in itertools.permutations(range(n)):
        path = list(path)
        path.append(path[0])
        current_distance = total_distance(path, points)
        if current_distance < best_distance:
            best_distance = current_distance
            best_path = path
        
        if time.time() - start_time > time_limit:
            break
        
    end_time = time.time()
    # print("Total time for computation = ", end_time-start_time)
    return best_path,best_distance

# [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 16, 10, 19, 17, 13, 9, 15, 14, 18, 0]