import sys
import random
import time
import numpy as np
import os
from pathlib import Path
class HC():
    def __init__(self, inputFile, cutoff, randSeed):
        file = open(inputFile, 'r')
        Lines = file.readlines()
        Lines = [list(map(float, line.split())) for line in Lines]
        n = int(Lines[0][0])
        W = Lines[0][1]
        self.method = "HC"
        self.outputDir = os.path.join(Path(__file__).resolve().parent,'output')
        Path(self.outputDir).mkdir(parents=True, exist_ok=True)
        values, weights = np.split(np.array(Lines[1:]), 2, axis=1)
        values = values.flatten()
        weights = weights.flatten()
        self.value = values
        self.weight = weights
        self.seed = randSeed
        self.cutoff = cutoff
        self.W = W
        self.n = n
        output_base = os.path.splitext(os.path.basename(inputFile))[0]
        sol_filename = "{}_{}_{}_{}.sol".format(output_base, self.method, self.cutoff, self.seed)
        self.outputFileSol = os.path.join(self.outputDir, sol_filename)
        trace_filename = "{}_{}_{}_{}.trace".format(output_base, self.method, self.cutoff, self.seed)
        self.outputFileTrace = os.path.join(self.outputDir, trace_filename)

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
                if trace_time>self.cutoff:
                    break
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
        a = 0.1
        X0 = np.random.binomial(1, a, self.n)
        # check the initial state exceeds the W
        while np.dot(X0, self.weight) > self.W:
            a = a*0.1
            X0 = np.random.binomial(1, a, self.n)
        bestX, bestValueWeight = self.hill_climbing(X0, iters)
        results.append(bestValueWeight[0])
        self.write_output_file(bestX, max(results))

    def write_output_file(self, bestX, bestValue):
        with open(self.outputFileSol, 'w+') as f:
            f.write(f"{int(bestValue)}\n")  # the best value as an integer
            indices = [str(index) for index, value in enumerate(bestX) if value == 1]
            f.write(",".join(indices) + "\n")  # the indices of selected items








