import os
import time
import numpy as np
from pathlib import Path

# Class for each item
class Item:
    def __init__(self, value, weight, index):
        self.value = value
        self.weight = weight
        self.index = index
        self.ratio = float(value) / weight  # Ensure floating-point division

class FPTAS:
    def __init__(self, inputFile, cutoff):
        self.inputFile = inputFile
        self.cutoff = cutoff
        self.outputDir = os.path.join(Path(__file__).resolve().parent, 'output')
        Path(self.outputDir).mkdir(parents=True, exist_ok=True)
        output_base = os.path.splitext(os.path.basename(inputFile))[0]
        self.outputFileSol = os.path.join(self.outputDir, f"{output_base}_FPTAS_{cutoff}.sol")
        self.outputFileTrace = os.path.join(self.outputDir, f"{output_base}_FPTAS_{cutoff}.trace")

        with open(inputFile, 'r') as file:
            lines = file.readlines()
            n, W = map(int, lines[0].strip().split())
            items = []
            for index, line in enumerate(lines[1:n+1], start=0):
                try:
                    value, weight = map(float, line.strip().split())
                    items.append(Item(value, weight, index))
                except ValueError as e:
                    print(f"Skipping line in {inputFile} due to error: {e}")
                    continue
            self.items = items
            self.W = W

    def fptas_knapsack(self, epsilon):
        start_time = time.time()
        valid_items = [item for item in self.items if item.weight > 0 and item.weight <= self.W]
        if not valid_items:
            return 0, []

        max_value = max(item.value for item in valid_items)
        n = len(valid_items)
        K = max_value * epsilon / n

        scaled_items = [Item(int(item.value / K), item.weight, item.index) for item in valid_items]
        dp = [0] * (self.W + 1)

        for item in scaled_items:
            for weight in range(self.W, item.weight - 1, -1):
                dp[weight] = max(dp[weight], dp[weight - item.weight] + item.value)

        approximate_total_value = int(dp[self.W] * K)
        end_time = time.time()

        # Reconstruct the solution (optional)
        # ... (This section would reconstruct which items are included in the solution)

        return approximate_total_value, end_time - start_time

    def run(self, epsilon):
        approx_value, exec_time = self.fptas_knapsack(epsilon)
        with open(self.outputFileSol, 'w+') as f:
            f.write(f"{approx_value}\n")
        print(f"Processed {self.inputFile}: Approx Value = {approx_value}, Time = {exec_time}s")

def main():
    epsilon = 0.1
    file_paths = [os.path.join('data', f'data_{i}.txt') for i in range(1, 11)]
    results = []

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"Data file missing: {file_path}")
            continue

        solver = FPTAS(file_path, epsilon)
        solver.run(epsilon)
        # Assume solution file exists and contains the correct total value for comparison
        solution_file_path = os.path.join('solutions', os.path.basename(file_path).replace('.txt', '.sol'))

        if os.path.exists(solution_file_path):
            with open(solution_file_path, 'r') as sol_file:
                official_total_value = int(sol_file.read().strip())
            with open(solver.outputFileSol, 'r') as sol_file:
                approx_total_value = int(sol_file.read().strip())
            approximation_ratio = approx_total_value / official_total_value if official_total_value != 0 else float('inf')
            results.append({
                'File': file_path,
                'Approximate Total Value': approx_total_value,
                'Official Total Value': official_total_value,
                'Approximation Ratio': approximation_ratio
            })

    for result in results:
        print(result)

if __name__ == '__main__':
    main()
