# import the packages
import time
import sys
import random

def cost(X, values, weights):
    total_value = sum(x * v for x, v in zip(X, values))
    total_weight = sum(x * w for x, w in zip(X, weights))
    return total_value, total_weight

def generate_all_neighbors(X):
    neighbors = []
    for i in range(len(X)):
        X_new = X[:]
        X_new[i] = 1 - X_new[i]
        neighbors.append(X_new)
    return neighbors

def hill_climbing(X0, values, weights, W):
    X_best = X0[:]
    X = X0[:]
    current_total_values, current_total_weight = cost(X, values, weights)
    max_total_values = current_total_values

    while True:
        improvement_found = False
        for neighbor in generate_all_neighbors(X):
            neighbor_total_values, neighbor_total_weight = cost(neighbor, values, weights)
            if neighbor_total_weight <= W and neighbor_total_values > current_total_values:
                X = neighbor[:]
                current_total_values = neighbor_total_values
                improvement_found = True
                if current_total_values > max_total_values:
                    max_total_values = current_total_values
                    X_best = X[:]
        if not improvement_found:
            break

    return max_total_values, X_best

def run_hc(n_runs, X0, values, weights, W):
    best_solution = None
    best_value = 0

    for _ in range(n_runs):
        solution_value, solution = hill_climbing(X0, values, weights, W)
        if solution_value > best_value:
            best_value = solution_value
            best_solution = solution

    return best_value, best_solution



def read_input_file(input_filename):
    with open(input_filename, 'r') as file:
        n, W = map(int, file.readline().split())
        items = [tuple(map(int, line.split())) for line in file.readlines()]
        values, weights = zip(*items)
    return n, W, values, weights

 
def write_output_file(output_filename, output_list):
    with open(output_filename, 'w') as file:
        for item in output_list:
            file.write(f"{item}\n")


def main(input_filename, output_filename):
    n, W, values, weights = read_input_file(input_filename)
    X0 = [random.randint(0, 1) for _ in range(n)]  # initial random solution
    max_total_values, X_best = run_hc(3, X0, values, weights, W)  
    print("Best Value:", max_total_values)
    output_list = [i + 1 for i, included in enumerate(X_best) if included == 1]
    write_output_file(output_filename, output_list)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.in> <output_file.out>")
        sys.exit(1)
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    main(input_filename, output_filename)



