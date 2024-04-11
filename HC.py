# import the packages
import time
import sys
import random


def evaluate_knapsack(items, knapsack):
    total_weight = sum(items[i][1] for i in knapsack)
    total_value = sum(items[i][0] for i in knapsack)
    return total_weight, total_value

def get_neighbors(knapsack, num_items):
    neighbors = []
    for i in range(num_items):
        new_knapsack = knapsack.copy()
        if i in new_knapsack:
            new_knapsack.remove(i)
        else:
            new_knapsack.add(i)
        neighbors.append(new_knapsack)
    return neighbors

def hill_climbing(items, max_weight):
    current_knapsack = set()
    while True:
        neighbors = get_neighbors(current_knapsack, len(items))
        current_weight, current_value = evaluate_knapsack(items, current_knapsack)
        best_neighbor = None
        best_value = current_value
        for neighbor in neighbors:
            weight, value = evaluate_knapsack(items, neighbor)
            if weight <= max_weight and value > best_value:
                best_value = value
                best_neighbor = neighbor

        if best_neighbor is None or best_value == current_value:
            break  
        current_knapsack = best_neighbor

    # binary output file as desired
    output_list = [1 if i in current_knapsack else 0 for i in range(len(items))]

    return output_list, best_value



def read_input_file(input_filename):
    with open(input_filename, 'r') as file:
        n, W = map(int, file.readline().split())
        items = [tuple(map(int, line.split())) for line in file.readlines()]
    return items, W

 
def write_output_file(output_filename, output_list):
    with open(output_filename, 'w') as file:
        for item in output_list:
            file.write(f"{item}\n")    
 


def main(input_filename, output_filename):
    items, W = read_input_file(input_filename)
    output_list, _ = hill_climbing(items, W)
    write_output_file(output_filename, output_list)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.in> <output_file.out>")
        sys.exit(1)
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    main(input_filename, output_filename)



    