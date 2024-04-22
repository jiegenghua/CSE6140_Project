import os
import time
from pathlib import Path

class Item:
    def __init__(self, value, weight, index):
        self.value = value
        self.weight = weight
        self.index = index

class FPTAS:
    def __init__(self, inputFile, cutoff, epsilon=0.1):
        self.epsilon = epsilon
        self.cutoff = cutoff
        self.inputFile = inputFile
        self.outputDir = os.path.join(Path(__file__).resolve().parent, 'output')
        Path(self.outputDir).mkdir(parents=True, exist_ok=True)
        self.items = []
        self.max_weight = 0
        self.load_items()

    def load_items(self):
        with open(self.inputFile, 'r') as file:
            lines = file.readlines()
        self.max_weight = int(lines[0].strip().split()[1])
        for index, line in enumerate(lines[1:]):
            value, weight = map(float, line.strip().split())
            self.items.append(Item(value, int(weight), index))

    def fptas_knapsack(self):
        start_time = time.time()
        max_value = max(item.value for item in self.items)
        n = len(self.items)
        K = max_value * self.epsilon / n  # Scaling factor for FPTAS
        scaled_items = [Item(int(item.value / K), item.weight, item.index) for item in self.items]
        dp = [0] * (self.max_weight + 1)
        
        # Fill the dp array
        for item in scaled_items:
            for weight in range(self.max_weight, item.weight - 1, -1):
                if weight >= item.weight:
                    dp[weight] = max(dp[weight], dp[weight - item.weight] + item.value)

        # Trace-back to determine which items were selected
        selected_indices = []
        weight = self.max_weight
        for i in reversed(range(len(scaled_items))):
            item = scaled_items[i]
            if weight >= item.weight and dp[weight] == dp[weight - item.weight] + item.value:
                selected_indices.append(item.index)  # Add item index
                weight -= item.weight  # Reduce weight by item's weight
                if weight == 0:
                    break  # Stop if the knapsack is full or no more weight capacity

        selected_indices.sort()  # Sort indices for output consistency
        approximate_total_value = int(dp[self.max_weight] * K)
        end_time = time.time()
        self.write_output_file(approximate_total_value, selected_indices, end_time - start_time)

    def write_output_file(self, bestValue, selected_indices, time_taken):
        output_base = os.path.splitext(os.path.basename(self.inputFile))[0]
        sol_filename = "{}_{}_{}.sol".format(output_base, 'FPTAS', self.cutoff)
        outputFileSol = os.path.join(self.outputDir, sol_filename)
        with open(outputFileSol, 'w') as f:
            f.write(f"{bestValue}\n")
            f.write(','.join(map(str, selected_indices)) + '\n')  # Correct indices output

    def runFPTAS(self):
        self.fptas_knapsack()

# Example of how to use the class
if __name__ == "__main__":
    inputFile = 'path_to_your_input_file.txt'
    cutoff = 60  # cutoff time in seconds
    fptas_solver = FPTAS(inputFile, cutoff)
    fptas_solver.runFPTAS()
