import os
import numpy as np
from pathlib import Path

class Item:
    def __init__(self, value, weight, index):
        self.value = value
        self.weight = weight
        self.index = index
        self.ratio = float(value) / weight  # Ensure floating-point division

class FPTAS:
    def __init__(self, inputFile, epsilon):
        self.epsilon = epsilon
        self.inputFile = inputFile
        self.method = "FPTAS"
        self.outputDir = Path('output')
        self.outputDir.mkdir(parents=True, exist_ok=True)

        with open(inputFile, 'r') as file:
            lines = file.readlines()
            n, W = map(int, lines[0].split())
            items = [Item(int(line.split()[0]), int(line.split()[1]), i) 
                     for i, line in enumerate(lines[1:], start=1)]

        self.items = items
        self.max_weight = W
        self.n = n

    def fptas_knapsack(self):
        max_value = max(item.value for item in self.items)
        K = max_value / (self.epsilon * self.n)

        scaled_items = [Item(int(item.value / K), item.weight, item.index) 
                        for item in self.items if item.weight <= self.max_weight and item.weight > 0]

        dp = [0] * (self.max_weight + 1)
        for item in scaled_items:
            for weight in range(self.max_weight, item.weight - 1, -1):
                dp[weight] = max(dp[weight], dp[weight - item.weight] + item.value)

        approximate_total_value = int(dp[self.max_weight] * K)
        selected_indices = []
        weight = self.max_weight
        for item in reversed(scaled_items):
            if weight >= item.weight and dp[weight] == dp[weight - item.weight] + item.value:
                selected_indices.append(item.index)
                weight -= item.weight

        selected_indices.sort()
        return approximate_total_value, selected_indices

    def run(self):
        OPT, X = self.fptas_knapsack()
        self.write_output_file(X, OPT)

    def write_output_file(self, selected_indices, best_value):
        output_file_name = f"{Path(self.inputFile).stem}_{self.method}_{int(self.epsilon*1000)}.sol"
        output_file_path = self.outputDir / output_file_name
        with open(output_file_path, 'w') as f:
            f.write(f"{best_value}\n")
            f.write(",".join(map(str, selected_indices)) + "\n")

# Usage Example
epsilon = 0.1  # 10% approximation error
file_paths = [f'small/small_{i}' for i in range(1, 11)]

for file_path in file_paths:
    fptas = FPTAS(file_path, epsilon)
    fptas.run()
