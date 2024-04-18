import heapq
import sys
from decimal import Decimal, getcontext

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
            value, weight = map(int, file.readline().split())
            items.append(Item(value, weight, index))

        # Sort items based on their value-to-weight ratio in descending order
        items.sort(key=lambda item: item.ratio, reverse=True)

        # # Print the values, weights, and ratios of each item
        # print("Sorted Items from read_file_bnb:")
        # for item in items:
        #     print("Value: {}, Weight: {}, Ratio: {:.10f}".format(item.value, item.weight, item.ratio))

        return items, max_weight


# Using BnB to solve the knapsack problem
def bnb(filename):
    # Initialization
    items, capacity  = read_file_bnb(filename)
    max_val = 0
    selected_items = []
    pq = []

    # a dummy root
    root = Node(item_index_sorted=-1, value=0, weight=0, lb=0, items_included=[])
    heapq.heappush(pq, (-root.lb, root))  # Push root

    while pq:
        # # Debug: Print the queue state
        # print_queue(pq)

        # Check the upper bound from the max values of solutions found 
        _, current = heapq.heappop(pq)
        
        # Check if current node is a leaf node
        if current.item_index_sorted == len(items) - 1:
            # Check if this leaf node's solution is better and within the capacity
            if current.weight <= capacity and current.value > max_val:
                max_val = current.value
                selected_items = current.items_included[:] # pass the shallow copy
            continue  # Go to the next item in the priority queue after updating max_value if necessary
        
        # Check if this full-capacity node's solution is better and the capacity is fully utilized
        if current.weight == capacity and current.value > max_val:
            max_val = current.value
            selected_items = current.items_included[:] # pass the shallow copy
            
        # # Debug: print the current max_val after each node
        # print("Current max value: {}, Current items: {}".format(max_val, selected_items))
        # print("Node chosen now: value: {}, weight: {}, lb: {}".format(current.value, current.weight, current.lb))

        # Extend to child nodes
        nex_item_idx = current.item_index_sorted + 1

        # Node with the next item included
        include = Node(nex_item_idx, current.value + items[nex_item_idx].value, current.weight + items[nex_item_idx].weight, 0, current.items_included + [items[nex_item_idx].index])
        if include.weight <= capacity:
            include.lb = get_bound(include, capacity, items)
            # print("Including item Lower bound: {}".format(include.lb))
            if include.lb > max_val:
                heapq.heappush(pq, (-include.lb, include))
                # print("Including item {}".format(items[nex_item_idx].index))

        # Node without the next item included
        exclude = Node(nex_item_idx, current.value, current.weight, 0, current.items_included)
        exclude.lb = get_bound(exclude, capacity, items)
        # print("Excluding item Lower bound: {}".format(exclude.lb))

        if exclude.lb > max_val:
            heapq.heappush(pq, (-exclude.lb, exclude))
            # print("Excluding item {}".format(items[nex_item_idx].index))

        # print("\n")
    return max_val, selected_items, len(items)

# def print_queue(pq):
#     print("Current queue:")
#     for neg_lb, node in pq:
#         print("Value: {}, Weight: {}, Items: {}, Lower bound: {}".format(node.value, node.weight, node.items_included, -neg_lb))
#     print()

def indices_to_binary(selected_indices, total_items):
    binary_list = [0] * total_items
    for index in selected_indices:
        binary_list[index] = 1
    return binary_list

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <max time in seconds>")
        return 1

    filename = sys.argv[1]

    max_value, selected_indices, length = bnb(filename)

    binary_result = indices_to_binary(selected_indices, length)

    print("Maximum value:", max_value)
    # print(selected_indices)
    print(" ".join(map(str, binary_result)))

    return 0

if __name__ == "__main__":
    sys.exit(main())
