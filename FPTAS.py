import os
from pathlib import Path

class FPTAS:
    def __init__(self, inputFile, cutoff, epsilon=0.1):
        self.inputFile = inputFile
        self.cutoff = cutoff
        self.epsilon = epsilon
        self.outputDir = os.path.join(Path(__file__).resolve().parent, 'output')
        Path(self.outputDir).mkdir(parents=True, exist_ok=True)

    def fptas_knapsack(self, n, items, max_weight):
        max_value = max(item['value'] for item in items)
        K = max_value * self.epsilon / n

        scaled_items = [{'value': int(item['value'] / K), 'weight': int(item['weight'])} for item in items]
        dp = [[0] * (int(max_weight) + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for weight in range(int(max_weight) + 1):
                if scaled_items[i - 1]['weight'] <= weight:
                    dp[i][weight] = max(dp[i - 1][weight], dp[i - 1][weight - scaled_items[i - 1]['weight']] + scaled_items[i - 1]['value'])
                else:
                    dp[i][weight] = dp[i - 1][weight]

        selected_items = []
        w = int(max_weight)
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(i - 1)  # Corrected to 0-based index
                w -= scaled_items[i - 1]['weight']

        approximate_total_value = int(dp[n][max_weight] * K)
        return approximate_total_value, selected_items

    def parse_and_solve_knapsack(self):
        with open(self.inputFile, 'r') as file:
            lines = file.readlines()

        n_items, max_weight = map(int, lines[0].strip().split())
        items = []

        for line in lines[1:n_items + 1]:
            value, weight = map(float, line.strip().split())
            items.append({'value': value, 'weight': weight})

        return self.fptas_knapsack(n_items, items, int(max_weight))

    def save_solution(self, total_value, selected_items):
        instance_name = os.path.splitext(os.path.basename(self.inputFile))[0]
        file_name = f"{instance_name}_FPTAS_{self.cutoff}.sol"
        file_path = os.path.join(self.outputDir, file_name)
        with open(file_path, 'w') as file:
            file.write(f"{total_value}\n")
            file.write(",".join(map(str, selected_items)))

    def runFPTAS(self):
        try:
            total_value, selected_items = self.parse_and_solve_knapsack()
            self.save_solution(total_value, selected_items)
        except Exception as e:
            print(f"Error processing file {self.inputFile}: {str(e)}")

# Example usage
if __name__ == "__main__":
    epsilon = 0.1  # 10% approximation error
    file_paths = [os.path.join('small', f'small_{i}') for i in range(1, 11)]
    for file_path in file_paths:
        agent = FPTAS(file_path, 1000, epsilon)
        agent.runFPTAS()
