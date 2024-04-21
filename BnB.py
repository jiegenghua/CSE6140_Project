import heapq
import sys
from decimal import Decimal, getcontext
import time
import os
import random
import numpy as np

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
        self.item_index_sorted = item_index_sorted # this is the item idex to be considered for that node, also the level of tree
        self.value = value
        self.weight = weight
        self.lb = lb
        self.items_included = items_included


class BnB():
    def __init__(self, inputFile, cutoff):
        file = open(inputFile, 'r')
        Lines = file.readlines()
        Lines = [list(map(float, line.split())) for line in Lines]
        n = int(Lines[0][0])
        W = Lines[0][1]
        temp = inputFile.split('\\')
        outputFileSol = '.\\' + 'output\\' + temp[-1] + "\\" + temp[-1] + '_' + 'BnB' + '_' + str(cutoff) + '.sol'
        temp = inputFile.split('\\')
        outputFileTrace = '.\\' + 'output\\' + temp[-1] + "\\" + temp[-1] + '_' + 'BnB' + '_' + str(cutoff) + '.trace'
        os.makedirs(os.path.dirname(outputFileSol), exist_ok=True)
        os.makedirs(os.path.dirname(outputFileTrace), exist_ok=True)
        if 'large' in temp[-1]:
            values, weights = np.split(np.array(Lines[1:-1]), 2, axis=1)  # ignore the last line if it is large data
        else:
            values, weights = np.split(np.array(Lines[1:]), 2, axis=1)
        values = values.flatten()
        weights = weights.flatten()
        self.value = values
        self.weight = weights
        self.cutoff = cutoff
        self.W = int(W)
        self.n = n
        self.outputFileSol = outputFileSol
        self.outputFileTrace = outputFileTrace

    # Calculate the lb of the total value from the node.
    def get_bound(self, node, capacity, items):
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
    def read_file_bnb(self):
        items = []
        for index in range(self.n):
            items.append(Item(self.value[index], self.weight[index], index))
        items.sort(key=lambda item: item.ratio, reverse=True)
        return items, self.W

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

    # Using BnB to solve the knapsack problem
    def bnb(self):
        # Initialization
        start_time = time.time()
        items, capacity = self.read_file_bnb()
        epsilon = 0.1  # Define epsilon for FPTAS
        max_val = 0.0
        selected_items = []

        trace = []  # List to keep track of solution improvements over time

        # Determine the best initial value and corresponding items
        max_val, selected_items = self.fptas_knapsack(items, capacity, epsilon)
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

            # Check the upper bound from the max values of solutions found
            _, current = heapq.heappop(pq)
        
            # Check if current node is a leaf node
            if current.item_index_sorted == len(items) - 1:
                # Check if this leaf node's solution is better and within the capacity
                if current.weight <= capacity and current.value > max_val:
                    max_val = current.value
                    selected_items = current.items_included[:] # pass the shallow copy
                    trace.append((elapsed_time, max_val))  # Log this improvement
                    # print("Trace update at {:.2f}s with value {}".format(elapsed_time, max_val))

                continue  # Go to the next item in the priority queue after updating max_value if necessary
        
            # Check if this full-capacity node's solution is better and the capacity is fully utilized
            if current.weight == capacity and current.value > max_val:
                max_val = current.value
                selected_items = current.items_included[:] # pass the shallow copy
                trace.append((elapsed_time, max_val))  # Log this improvement
            nex_item_idx = current.item_index_sorted + 1

            # Node with the next item included
            include = Node(nex_item_idx, current.value + items[nex_item_idx].value, current.weight + items[nex_item_idx].weight, 0, current.items_included + [items[nex_item_idx].index])
            if include.weight <= capacity:
                include.lb = self.get_bound(include, capacity, items)
                # print("Including item Lower bound: {}".format(include.lb))
                if include.lb > max_val:
                    heapq.heappush(pq, (-include.lb, include))
                    # print("Including item {}".format(items[nex_item_idx].index))

            # Node without the next item included
            exclude = Node(nex_item_idx, current.value, current.weight, 0, current.items_included)
            exclude.lb = self.get_bound(exclude, capacity, items)
            # print("Excluding item Lower bound: {}".format(exclude.lb))

            if exclude.lb > max_val:
                heapq.heappush(pq, (-exclude.lb, exclude))
        elapsed_time = time.time() - start_time
        return max_val, selected_items, trace, elapsed_time

    def indices_to_binary(self, selected_indices, total_items):
        binary_list = [0] * total_items
        for index in selected_indices:
            binary_list[index] = 1
        return binary_list

    def runBnB(self):
        start_time = time.time()
        max_value, selected_indices, trace, elapsed_time = self.bnb()
        sol_filename = self.outputFileSol
        trace_filename = self.outputFileTrace

        # Write to solution file
        with open(sol_filename, 'w') as sol_file:
            sol_file.write("{}\n".format(max_value))
            sol_file.write(",".join(map(str, selected_indices)) + "\n")

        # Write to trace file
        with open(trace_filename, 'w') as trace_file:
            for t, val in trace:
                trace_file.write("{:.2f}, {}\n".format(t, val))

        total_time = time.time() - start_time
        print(total_time)
