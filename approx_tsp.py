import math
import time

# Function to calculate Euclidean distance between two points
def euclidean_distance(point1, point2):
    return round(math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))

# Function to construct a minimum spanning tree using Prim's algorithm
def mst_prim(graph, root):
    n = len(graph)
    visited = [False] * n
    key = [float('inf')] * n
    predecessors = [None] * n
    key[root] = 0

    for _ in range(n):
        u = min((val, idx) for idx, val in enumerate(key) if not visited[idx])[1]
        visited[u] = True

        for v, cost in graph[u].items():
            if not visited[v] and cost < key[v]:
                key[v] = cost
                predecessors[v] = u

    return predecessors

# 2-approximation algorithm based on MST
def approx_tsp(graph, root):
    predecessors = mst_prim(graph, root)

    # Construct the MST adjacency list
    mst = {i: {} for i in range(len(predecessors))}
    for v, u in enumerate(predecessors):
        if u is not None:
            cost = graph[u][v]
            mst[u][v] = cost
            mst[v][u] = cost

    # Perform an iterative preorder walk of the MST
    preorder_walk = []
    distances_in_tour = []  # To store distances in the tour
    stack = [root]

    while stack:
        current = stack.pop()
        preorder_walk.append(current)
        stack.extend(neighbor for neighbor in mst[current] if neighbor not in preorder_walk)

    # Ensure the tour starts and ends at the root vertex
    preorder_walk.append(root)

    # Calculate distances in the tour
    for i in range(len(preorder_walk) - 1):
        distances_in_tour.append(graph[preorder_walk[i]][preorder_walk[i + 1]])

    return preorder_walk, sum(distances_in_tour)

# Read the dataset from a file
def read_dataset(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract points from the NODE_COORD_SECTION
    points = [tuple(map(float, line.split()[1:])) for line in lines if line.strip() and line.split()[0].isdigit()]

    return points

# Create a graph from the points
def create_graph(points):
    n = len(points)
    graph = {i: {} for i in range(n)}

    for i in range(n):
        for j in range(i + 1, n):
            cost = euclidean_distance(points[i], points[j])
            graph[i][j] = cost
            graph[j][i] = cost

    return graph

# Example usage
# if __name__ == "__main__":
#     # Replace 'your_dataset.tsp' with the actual dataset file
#     dataset_filename = 'DATA/DATA/UMissouri.tsp'
#     points = read_dataset(dataset_filename)

#     # Create a graph from the points
#     graph = create_graph(points)

#     # Choose a root vertex (e.g., the first vertex)
#     root_vertex = 0

#     # Run the 2-approximation algorithm
#     start_time = time.time()
#     approx_tour, distances_in_tour = approx_tsp(graph, root_vertex)
#     end_time = time.time()
    
#     # Print the tour and distances
#     print("2-Approximation Algorithm Based on MST for: ", dataset_filename)
#     print("Tour:", approx_tour)
#     print("Distances in Tour:", distances_in_tour)
#     print("Total Distance:", sum(distances_in_tour))
#     print(f"Time Taken: {end_time - start_time:.5f} seconds")
