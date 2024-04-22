import os
import time
import numpy as np
from pathlib import Path
#  Class for each item
class Item:
    def __init__(self, value, weight, index):
        self.value = value
        self.weight = weight
        self.index = index
        self.ratio = float(value) / weight  # Ensure floating-point division

class FPTAS():
    def __init__(self, inputFile, cutoff):
        file = open(inputFile, 'r')
        Lines = file.readlines()
        Lines = [list(map(float, line.split())) for line in Lines]
        n = int(Lines[0][0])
        W = Lines[0][1]
        values, weights = np.split(np.array(Lines[1:]), 2, axis=1)
        values = values.flatten()
        weights = weights.flatten()
        self.value = values
        self.weight = weights
        self.cutoff = cutoff
        self.W = W
        self.n = n
        self.method = "FPTAS"
        self.outputDir = os.path.join(Path(__file__).resolve().parent,'output')
        Path(self.outputDir).mkdir(parents=True, exist_ok=True)
        output_base = os.path.splitext(os.path.basename(inputFile))[0]
        sol_filename = "{}_{}_{}.sol".format(output_base, self.method, self.cutoff)
        self.outputFileSol = os.path.join(self.outputDir, sol_filename)
        trace_filename = "{}_{}_{}.trace".format(output_base, self.method, self.cutoff)
        self.outputFileTrace = os.path.join(self.outputDir, trace_filename)

    def fptas_knapsack(self, items, max_weight, epsilon):
        if epsilon <= 0:
            raise ValueError("Epsilon must be greater than zero.")

        # Filter out items with non-positive weights or weights exceeding the capacity before processing
        valid_items = [item for item in items if item.weight > 0 and item.weight <= max_weight]
        if not valid_items:
            return 0, []

        max_value = max(item.value for item in valid_items)
        n = len(valid_items)
        K = max_value / (epsilon * n) if n > 0 else 1  # Avoid division by zero

        # Scale down the values of the items and ensure no weight becomes zero after scaling
        scaled_items = [Item(int(item.value / K), max(1, int(item.weight)), item.index) for item in valid_items]

        # Initialize the dynamic programming table
        dp = [0] * (max_weight + 1)

        # Dynamic programming to find the best value with scaled values
        for item in scaled_items:
            item_weight = max(1, int(item.weight))  # Ensure weight is at least 1
            for weight in range(max_weight, item_weight - 1, -1):
                dp[weight] = max(dp[weight], dp[weight - item_weight] + item.value)

        # Calculate the approximate total value
        approximate_total_value = int(dp[max_weight] * K)

        # Reconstruct the solution to find which items are included
        selected_indices = []
        weight = max_weight
        for i in reversed(range(len(scaled_items))):
            item = scaled_items[i]
            if weight >= item.weight and dp[weight] == dp[weight - item.weight] + item.value:
                selected_indices.append(item.index)
                weight -= item.weight

        selected_indices.reverse()
        return approximate_total_value, selected_indices

    def runFPTAS(self):
        epsilon = 0.1
        items = []
        for index in range(self.n):
            items.append(Item(self.value[index], self.weight[index], index))
        items.sort(key=lambda item: item.ratio, reverse=True)

        max_weight = int(self.W)
        OPT, X = self.fptas_knapsack(items, max_weight, epsilon)
        self.write_output_file(X, OPT)

    def write_output_file(self, bestX, bestValue):
        indices = [str(index) for index in bestX]
        with open(self.outputFileSol, 'w+') as f:
            f.write(f"{int(bestValue)}\n")
            f.write(",".join(indices) + "\n")
