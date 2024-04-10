import sys

def read_knapsack_data(filename):
    with open(filename, 'r') as file:
        num_items, capacity = map(int, file.readline().split())
        values, weights = [], []

        for _ in range(num_items):
            value, weight = map(int, file.readline().split())
            values.append(value)
            weights.append(weight)

        return values, weights, capacity

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <max time in seconds>")
        return 1

    filename = sys.argv[1]
    max_time_seconds = int(sys.argv[2])

    try:
        values, weights, capacity = read_knapsack_data(filename)
    except IOError:
        print("Error: File '%s' not found." % filename)
        return 1
    except ValueError:
        print("Error: Invalid data format in the input file.")
        return 1

    # print("Read %d items with a total capacity of %d" % (len(values), capacity))
    # print("Values:", values)
    # print("Weights:", weights)

    return 0

if __name__ == "__main__":
    sys.exit(main())
