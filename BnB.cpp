#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm>

class Item 
{
public:
    int value;
    int weight;
    int index;

    Item(int value, int weight, int index) : value(value), weight(weight), index(index) {}
};

int main(int argc, char* argv[])
{
    // Check cmd line arguments
    if (argc < 3) 
    {
        std::cout << "Usage: <filename> <cut-off time in seconds>" << std::endl;
        return 1;
    }

    std::string filename = argv[1];
    int cutoffTime = std::stoi(argv[2]);
    std::ifstream file(filename);

    // Read items
    int numItems;
    int maxWeight;
    file >> numItems >> maxWeight;

    std::vector<Item> items;
    for (int i = 0; i < numItems; ++i) 
    {
        int value, weight;
        file >> value >> weight;
        items.emplace_back(value, weight, i);
        // std::cout << "Item " << (i+1) << ": Value = " << value << ", Weight = " << weight << std::endl;
    }   

    // Start recoding time
    auto startTime = std::chrono::high_resolution_clock::now();
    std::sort(items.begin(), items.end(), [](const Item& a, const Item& b)
    {
        return static_cast<double>(a.value) / a.weight > static_cast<double>(b.value) / b.weight;

    });
    auto endTime = std::chrono::high_resolution_clock::now();
    // for (const Item& item : items) std::cout << "Value: " << item.value << ", Weight: " << item.weight << std::endl;
    auto elapsedTime = std::chrono::duration_cast<std::chrono::seconds>(endTime - startTime).count();
    std::cout << "Time spent: " << elapsedTime;
}