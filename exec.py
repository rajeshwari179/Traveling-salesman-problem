import sys
import time
import math
import numpy as np
from brute_force_tsp import brute_force_tsp
from approx_tsp import approx_tsp, read_dataset, create_graph
from Simulated_Annealing import Simulated_Annealing, read_tsp_file, calculate_distance


def write_output(file_name, quality, tour):
    with open(file_name, 'w') as file:
        file.write(f"{quality}\n")
        file.write(','.join(map(str, tour)))


def main():
    if len(sys.argv) != 7 and len(sys.argv) != 9:
        print("Usage: exec instance algorithm cutoff_time [seed]")
        sys.exit(1)

    filename_index = sys.argv.index("-inst")
    filename = sys.argv[filename_index+1]
    algorithm_index = sys.argv.index("-alg")
    algorithm = sys.argv[algorithm_index+1]
    cutoff_time_index = sys.argv.index("-time")
    cutoff_time = sys.argv[cutoff_time_index+1]
    if(len(sys.argv) == 9):
        seed_index = sys.argv.index("-seed")
        seed = sys.argv[seed_index+1]
    else:
        seed = 0

    if(algorithm == "BF"):
        points = read_dataset(filename)
        time_limit_bruteforce = cutoff_time
        tour, total_distance = brute_force_tsp(points, float(time_limit_bruteforce))
        
        # print("Exact Brute-Force Solution for time and place: ",i, place)
        # print("Tour:", min_tour)
        # print("Cost:", min_cost)
        # print(f"Time Taken: {bruteforce_duration:.2f} seconds")

        # pass
        output_file = "output/"+filename[:-4] + "_" + algorithm + "_" + str(cutoff_time) + ".sol"
        write_output(output_file, total_distance, tour)


    elif(algorithm == "Approx"):
        
        points = read_dataset(filename)
        # Create a graph from the points
        graph = create_graph(points)
        # Choose a root vertex (e.g., the first vertex)
        root_vertex = 0

        # Run the 2-approximation algorithm
        # start_time = time.time()
        tour, total_distance = approx_tsp(graph, root_vertex)
        # end_time = time.time()
        # pass
        # outputfile = 'output/' + filename[5:]
        output_file = "output/"+filename[:-4] + "_" + algorithm + "_"+ str(seed) + ".sol"
        write_output(output_file, total_distance, tour)
        
        
    else:
        
        # file_path = filename
        city_coordinates = read_tsp_file(filename)

        # Calculate distances
        distances = np.zeros((len(city_coordinates) + 1, len(city_coordinates) + 1), dtype=int)
        for i in range(len(city_coordinates)):
            for j in range(i + 1, len(city_coordinates)):
                distances[i + 1][j + 1] = distances[j + 1][i + 1] = calculate_distance(city_coordinates[i], city_coordinates[j])

        # Apply simulated annealing to find the best path
        tour, total_distance = Simulated_Annealing(city_coordinates, num_runs=10, distances=distances)

        # Print results
        # print("Best TSP path for {}: {}".format(filename, best_path))
        # print("Total Distance:", Min_distance)
        
        # pass   
        output_file = "output/"+filename[:-4] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(seed) + ".sol"
        write_output(output_file, total_distance, tour)       
    
    
    
if __name__ == "__main__":
    main()
