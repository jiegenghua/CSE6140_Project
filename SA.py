import sys
import os
import random
import time

import matplotlib.pyplot as plt
import numpy as np
import os
class SA():
    def __init__(self, inputFile, cutoff, randSeed):
        file = open(inputFile, 'r')
        Lines = file.readlines()
        Lines = [list(map(float, line.split())) for line in Lines]
        n = int(Lines[0][0])
        W = Lines[0][1]
        temp = inputFile.split('\\')
        outputFileSol = '.\\'+'output\\' + temp[-1] + "\\" + temp[-1] + '_' + 'SA' + '_' + str(cutoff) + '_' + str(
            randSeed) + '.sol'
        temp = inputFile.split('\\')
        outputFileTrace = '.\\'+'output\\' + temp[-1] + "\\" + temp[-1] + '_' + 'SA' + '_' + str(cutoff) + '_' + str(
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
        return [totalValue, totalWeight]

    def generateNeighbors(self, X):
        chosenID = random.choice(range(self.n))
        newX = list(X)
        newX[chosenID] = 1-X[chosenID]
        return newX

    def SA(self, maxiter, X0, T0, dR):
        n = self.n
        minTemperature = 5
        T = T0
        X = X0
        bestX = [0]*n
        currCost = self.cost(X)[0]
        bestCost = currCost
        avgCostList = []
        tol = 0.1
        cal = 0
        f2 = open(self.outputFileTrace, 'w+')
        start = time.time()
        while T > minTemperature:
            i = 0
            if len(avgCostList) >= 10 and abs(np.mean(avgCostList)-np.mean(avgCostList[:-1])) < tol:
                print("converge!!!!!!!")
                break
            while i < maxiter:
                while True:
                    newX = self.generateNeighbors(X)
                    if self.cost(newX)[1] <= self.W:
                        break
                if self.cost(newX)[0] > currCost:
                    X = newX[:]
                    currCost = self.cost(newX)[0]
                else:
                    r = random.uniform(0, 1)
                    if r < np.exp((self.cost(newX)[0]-self.cost(X)[0])/T):
                        X = newX[:]
                        currCost = self.cost(newX)[0]
                if currCost > bestCost:
                    bestX = X[:]
                    bestCost = currCost
                    avgCostList.append(bestCost)
                    tt = time.time()-start
                    f2.write(str(tt)+','+str(bestCost)+'\n')
                i += 1
                cal += 1
            T *= dR
        f2.close()
        return bestX, bestCost

    def runSA(self):
        random.seed(self.seed)
        dR = 0.95
        T = 1000
        iters = 50
        start = time.time()
        X0 = np.random.binomial(1, 0.1, self.n)
        sol = self.SA(iters, X0, T, dR)
        time_all = time.time()-start
        indices = [str(index) for index, value in enumerate(sol[0]) if value == 1]
        f = open(self.outputFileSol, 'w+')
        f.write(str(sol[1])+'\n')
        f.write(",".join(indices) + "\n")
        f.close()
        return time_all





















