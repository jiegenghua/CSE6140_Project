import sys
import random
import time
import numpy as np
import os
class HC():
    def __init__(self, inputFile, cutoff, randSeed):
        file = open(inputFile, 'r')
        Lines = file.readlines()
        Lines = [list(map(float, line.split())) for line in Lines]
        n = int(Lines[0][0])
        W = Lines[0][1]
        temp = inputFile.split('\\')
        outputFileSol = '.\\' + 'output\\' + temp[-1] + "\\" + temp[-1] + '_' + 'HC' + '_' + str(cutoff) + '_' + str(
            randSeed) + '.sol'
        temp = inputFile.split('\\')
        outputFileTrace = '.\\' + 'output\\' + temp[-1] + "\\" + temp[-1] + '_' + 'HC' + '_' + str(cutoff) + '_' + str(
            randSeed) + '.trace'
        os.makedirs(os.path.dirname(outputFileSol), exist_ok=True)
        os.makedirs(os.path.dirname(outputFileTrace), exist_ok=True)
        if 'large' in temp[-1]:
            values, weights = np.split(np.array(Lines[1:-1]), 2, axis=1)
        else:
            values, weights = np.split(np.array(Lines[1:]), 2, axis=1)
        values = values.flatten()
        weights = weights.flatten()
        self.value = values
        self.weight = weights
        self.seed = randSeed
        self.cutoff = cutoff
        self.W = W
        self.n = n
        self.outputFileSol = outputFileSol
        self.outputFileTrace = outputFileTrace

    def cost(self, X):
        totalValue = np.dot(np.array(X), np.array(self.value))
        totalWeight = np.dot(np.array(X), np.array(self.weight))
        return totalValue, totalWeight

    def generateNeighbors(self, X):
        newX = list(X)
        chosenID = random.choice(range(len(X)))
        newX[chosenID] = 1 - newX[chosenID]
        return newX

    def hill_climbing(self, X0, maxiter):
        start = time.time()
        X = X0[:]
        bestX = X[:]
        bestValue, bestWeight = self.cost(X)
        trace_data = []
        trace_time0 = time.time() - start
        trace_data.append((trace_time0, bestValue))

        for _ in range(maxiter):
            newX = self.generateNeighbors(X)
            newValue, newWeight = self.cost(newX)

            if newWeight <= self.W and newValue > bestValue:
                X = newX[:]
                bestX = newX[:]
                bestValue = newValue
                trace_time = time.time() - start
                trace_data.append((trace_time, bestValue))

        self.write_trace_file(trace_data, self.outputFileTrace)
        return bestX, (bestValue, bestWeight)

    def write_trace_file(self, trace_data, trace_filename):
        with open(trace_filename, 'w+') as f2:
            for time_stamp, value in trace_data:
                f2.write(str(time_stamp) + ',' + str(int(value)) + '\n')

    def run_HC(self):
        iters = 6666
        start = time.time()
        random.seed(self.seed)
        results = []
        X0 = np.random.binomial(1, 0.1, self.n)
        # check the initial state exceeds the W
        while np.dot(X0, self.weight) > self.W:
            X0 = np.random.binomial(1, 0.1, self.n)
        bestX, bestValueWeight = self.hill_climbing(X0, iters)
        results.append(bestValueWeight[0])
        self.write_output_file(bestX, max(results))

    def write_output_file(self, bestX, bestValue):
        with open(self.outputFileSol, 'w+') as f:
            f.write(f"{int(bestValue)}\n")  # the best value as an integer
            indices = [str(index) for index, value in enumerate(bestX) if value == 1]
            f.write(",".join(indices) + "\n")  # the indices of selected items








