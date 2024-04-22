import heapq
import sys
from decimal import Decimal, getcontext
import time
import os
import random
from pathlib import Path

#  Class for each item
class Item:
    def __init__(self, value, weight, index):
        self.value = value
        self.weight = weight
        self.index = index
        self.ratio = float(value) / weight  # Ensure floating-point division


# Class for node in the tree for subproblem, recording total value, weight, and included items
class Node:
    def __init__(self, item_index_sorted, value, weight, lb, items_included):
        self.item_index_sorted = item_index_sorted
        self.value = value
        self.weight = weight
        self.lb = lb
        self.items_included = items_included

    # Define a less-than method for comparing two nodes
    def __lt__(self, other):
        # Reverse the logic if you push with negative lb to maintain a max-heap property
        return self.lb < other.lb


# Calculate the lb of the total value from the node.
def get_bound(node, capacity, items):
    if node.weight > capacity:
        return 0
    lb = node.value
    j = node.item_index_sorted + 1
    total_weight = node.weight

    # Add the whole items as many as possible
    while j < len(items) and total_weight + items[j].weight <= capacity:
        total_weight += items[j].weight
        lb += items[j].value
        j += 1
    # Add fractional part of the next item if it fits partially
    if j < len(items) and total_weight < capacity:
        remaining_capacity = capacity - total_weight
        lb += remaining_capacity * float(items[j].value) / items[j].weight

    return lb


# To read the values and weights from the file. Specificly for BnB to store items.
def read_file_bnb(filename):
    with open(filename, 'r') as file:
        numItems, max_weight = map(int, file.readline().split())
        items = []

        for index in range(numItems):
            value, weight = map(float, file.readline().split())
            items.append(Item(value, weight, index))

        # Sort items based on their value-to-weight ratio in descending order
        items.sort(key=lambda item: item.ratio, reverse=True)

        # # Print the values, weights, and ratios of each item
        # print("Sorted Items from read_file_bnb:")
        # for item in items:
        #     print("Value: {}, Weight: {}, Ratio: {:.10f}".format(item.value, item.weight, item.ratio))

        return items, max_weight


def fptas_knapsack(items, max_weight, epsilon):
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


class BnB():
    def __init__(self, inputFile, cutoff):
        self.filename = inputFile
        self.cutoff = cutoff
        self.items, self.capacity = read_file_bnb(inputFile)
        self.method = "BnB"
        self.outputDir = os.path.join(Path(__file__).resolve().parent,'output')

    # Using BnB to solve the knapsack problem
    def bnb(self):
        # Initialization
        start_time = time.time()
        epsilon = 0.1  # Define epsilon for FPTAS
        max_val = 0.0
        selected_items = []

        trace = []  # List to keep track of solution improvements over time

        # Determine the best initial value and corresponding items
        max_val, selected_items = fptas_knapsack(self.items, self.capacity, epsilon)
        trace.append((0, max_val))  # Log initial best value found

        # Initial root node for BnB
        pq = []

        # a dummy root
        root = Node(item_index_sorted=-1, value=0, weight=0, lb=0, items_included=[])
        heapq.heappush(pq, (-root.lb, root))  # Push root

        while pq:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > self.cutoff:  # Check if the cutoff time has been exceeded
                break
            # # Debug: Print the queue state
            # print_queue(pq)

            # Check the upper bound from the max values of solutions found
            _, current = heapq.heappop(pq)

            # Check if current node is a leaf node
            if current.item_index_sorted == len(self.items) - 1:
                # Check if this leaf node's solution is better and within the capacity
                if current.weight <= self.capacity and current.value > max_val:
                    max_val = current.value
                    selected_items = current.items_included[:]  # pass the shallow copy
                    trace.append((elapsed_time, max_val))  # Log this improvement
                    # print("Trace update at {:.2f}s with value {}".format(elapsed_time, max_val))

                continue  # Go to the next item in the priority queue after updating max_value if necessary

            # Check if this full-capacity node's solution is better and the capacity is fully utilized
            if current.weight == self.capacity and current.value > max_val:
                max_val = current.value
                selected_items = current.items_included[:]  # pass the shallow copy
                trace.append((elapsed_time, max_val))  # Log this improvement
                # print("Trace update at {:.2f}s with value {}".format(elapsed_time, max_val))

            # Debug: print the current max_val after each node
            # print("Current max value: {}, Current items: {}".format(max_val, selected_items))
            # print("Node chosen now: value: {}, weight: {}, lb: {}".format(current.value, current.weight, current.lb))

            # Extend to child nodes
            nex_item_idx = current.item_index_sorted + 1

            # Node with the next item included
            include = Node(nex_item_idx, current.value + self.items[nex_item_idx].value,
                           current.weight + self.items[nex_item_idx].weight, 0,
                           current.items_included + [self.items[nex_item_idx].index])
            if include.weight <= self.capacity:
                include.lb = get_bound(include, self.capacity, self.items)
                # print("Including item Lower bound: {}".format(include.lb))
                if include.lb > max_val:
                    heapq.heappush(pq, (-include.lb, include))
                    # print("Including item {}".format(items[nex_item_idx].index))

            # Node without the next item included
            exclude = Node(nex_item_idx, current.value, current.weight, 0, current.items_included)
            exclude.lb = get_bound(exclude, self.capacity, self.items)
            # print("Excluding item Lower bound: {}".format(exclude.lb))

            if exclude.lb > max_val:
                heapq.heappush(pq, (-exclude.lb, exclude))
                # print("Excluding item {}".format(items[nex_item_idx].index))

            # print("\n")
        elapsed_time = time.time() - start_time
        return max_val, selected_items, trace, elapsed_time

    def runBnB(self):
        start_time = time.time()
        # Note that you should call the bnb method, not the standalone bnb function
        max_value, selected_indices, trace, elapsed_time = self.bnb()
        output_base = os.path.splitext(os.path.basename(self.filename))[0]
        sol_filename = "{}_{}_{}.sol".format(output_base, self.method, self.cutoff)
        sol_filename = os.path.join(self.outputDir, sol_filename)
        trace_filename = "{}_{}_{}.trace".format(output_base, self.method, self.cutoff)
        trace_filename = os.path.join(self.outputDir, trace_filename)
        print("hahahah", trace_filename)
        # Write to solution file
        with open(sol_filename, 'w+') as sol_file:
            sol_file.write("{}\n".format(int(max_value)))  # Convert max_value to int
            sol_file.write(",".join(map(str, selected_indices)) + "\n")

        # Write to trace file
        with open(trace_filename, 'w+') as trace_file:
            for t, val in trace:
                trace_file.write("{:.2f},{}\n".format(t, int(val)))  # Convert trace values to int