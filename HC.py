import sys
import random
import time
import numpy as np

def cost(X, value, weight):
    totalValue = np.dot(np.array(X), np.array(value))
    totalWeight = np.dot(np.array(X), np.array(weight))
    return totalValue, totalWeight

def generateNeighbors(X):
    newX = list(X)
    chosenID = random.choice(range(len(X)))
    newX[chosenID] = 1 - newX[chosenID]
    return newX

'''
def generateManyNeighbors(X):    
'''
'''
    Returns a list of of all neighbours in the Neighbourhood of packing            
    Parameters: X(numpy array): numpy array of 1/0 to indicate a specified packing            
    Returns: neighbourhood (list): a list of of all neighbours in the Neighbourhood of packing                    
    The size of the 1-flip neighborhood = 100'''
'''
    neighbourhood = []
    for i in range(0, 100):
        temp = list(X)
        neighbourhood.append(temp)
        if neighbourhood[i][i] == 1:
            neighbourhood[i][i] = 0
        else:
            neighbourhood[i][i] = 1
            
    return neighbourhood
'''



def hill_climbing(X0, values, weights, W, maxiter, run_id, output_filename):
    start = time.time()
    X = X0[:]
    bestX = X[:]
    bestValue, bestWeight = cost(X, values, weights)
    trace_data = []
    trace_time0 = time.time() - start
    trace_data.append((trace_time0, bestValue))

    for _ in range(maxiter):
        newX = generateNeighbors(X)
        newValue, newWeight = cost(newX, values, weights)

        if newWeight <= W and newValue > bestValue:
            X = newX[:]
            bestX = newX[:]
            bestValue = newValue
            trace_time = time.time() - start
            trace_data.append((trace_time, bestValue))

    trace_filename = f"{output_filename}_{run_id}.trace"
    write_trace_file(trace_data, trace_filename)
    return bestX, (bestValue, bestWeight)


def read_input_file(inputFile):
    with open(inputFile, 'r') as file:
        lines = file.readlines()
    first_line = lines[0].split()
    n = int(first_line[0])  # number of items
    W = float(first_line[1])  # target weight
    
    
    item_data = np.array([list(map(float, line.split())) for line in lines[1:-1]])
    values, weights = item_data[:, 0], item_data[:, 1]
    
    OPT = np.array(list(map(int, lines[-1].split())))
    total_value_OPT = np.sum(values * OPT)
    return n, W, values, weights, total_value_OPT


def write_trace_file(trace_data, trace_filename):
    with open(trace_filename, 'w+') as f2:
        for time_stamp, value in trace_data:
            f2.write(str(time_stamp) + ',' + str(int(value)) + '\n')

def main(inputFile, outputFileSol, iters=6666, cutoff=20, randSeed=42):
    start = time.time()
    n, W, values, weights, total_value_OPT = read_input_file(inputFile)
    random.seed(randSeed)
    
    results = []
    for run_id in range(20):
        X0 = np.random.binomial(1, 0.1, n)  # random start
        
        # check the initial state exceeds the W
        while np.dot(X0, weights) > W:
            X0 = np.random.binomial(1, 0.1, n)

        bestX, bestValueWeight = hill_climbing(X0, values, weights, W, iters, run_id, outputFileSol)
        # Append result only if it is less than or equal to the optimal value
        # if bestValueWeight[0] <= total_value_OPT:
            # results.append(bestValueWeight[0])
        results.append(bestValueWeight[0])
       
    best_result = max(results)
    best_index = results.index(best_result)
    best_solution = bestX  # store the best solution found
    mean_val = np.mean(results)
    error = (total_value_OPT - mean_val) / total_value_OPT

    print("OPT:", total_value_OPT)
    print("Total value: min, max, mean:", min(results), max(results), mean_val)
    print("Time taken:", (time.time() - start) / len(results))
    print("Error:", error)

    outputFileSol = outputFileSol if outputFileSol.endswith(".sol") else outputFileSol + ".sol"
    write_output_file(best_solution, best_result, outputFileSol)

def write_output_file(bestX, bestValue, outputFileSol):
    with open(outputFileSol, 'w+') as f:
        f.write(f"{int(bestValue)}\n")  # the best value as an integer
        indices = [str(index) for index, value in enumerate(bestX) if value == 1]
        f.write(",".join(indices) + "\n")  # the indices of selected items

if __name__ == "__main__":
    input_filename = './DATASET/large_scale/large_3'
    output_filename = './Output/large_3/large_3'
    main(input_filename, output_filename)







