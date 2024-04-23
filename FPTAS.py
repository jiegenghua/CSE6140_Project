import os

def fptas_knapsack(items, max_weight, epsilon):
    max_value = max(item['value'] for item in items)
    n = len(items)
    K = max_value * epsilon / n

    scaled_items = [{'value': int(item['value'] / K), 'weight': item['weight']} for item in items]

    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for weight in range(max_weight + 1):
            if scaled_items[i - 1]['weight'] <= weight:
                dp[i][weight] = max(dp[i - 1][weight], dp[i - 1][weight - scaled_items[i - 1]['weight']] + scaled_items[i - 1]['value'])
            else:
                dp[i][weight] = dp[i - 1][weight]

    selected_items = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i) 
            w -= items[i - 1]['weight']

    approximate_total_value = int(dp[n][max_weight] * K)
    return approximate_total_value, selected_items

def parse_and_solve_knapsack(filepath, epsilon):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    n_items, max_weight = map(int, lines[0].strip().split())
    items = []

    for line in lines[1:n_items+1]:
        value, weight = map(int, line.strip().split())
        items.append({'value': value, 'weight': weight})

    total_value, selected_items = fptas_knapsack(items, max_weight, epsilon)
    return total_value, selected_items

def save_solution(instance_name, method, cutoff, total_value, selected_items):
    file_name = f"{instance_name}_{method}_{cutoff}.sol"
    with open(file_name, 'w') as file:
        file.write(f"{total_value}\n")
        file.write(",".join(map(str, selected_items)))

def main(file_paths, epsilon):
    method = "approx"
    cutoff = int(epsilon * 1000) 
    
    for file_path in file_paths:
        instance_name = os.path.basename(file_path)
        try:
            total_value, selected_items = parse_and_solve_knapsack(file_path, epsilon)
            save_solution(instance_name, method, cutoff, total_value, selected_items)
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

epsilon = 0.1  # 10% approximation error
file_paths = [
    os.path.join('small', f'small_{i}') for i in range(1, 11)
]
main(file_paths, epsilon)
