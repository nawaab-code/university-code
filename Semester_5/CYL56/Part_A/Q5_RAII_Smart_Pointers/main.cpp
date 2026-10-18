#include <iostream>
#include <memory>
#include <stdexcept>

class IntegerArray {
    std::size_t size;
    std::unique_ptr<int[]> data;
public:
    explicit IntegerArray(std::size_t n) : size(n), data(std::make_unique<int[]>(n)) {}
    int& at(std::size_t i) {
        if (i >= size) throw std::out_of_range("invalid index");
        return data[i];
    }
};

int main() {
    {
        IntegerArray numbers(3);
        numbers.at(0) = 10;
        std::cout << "First: " << numbers.at(0) << '\n';
        try { numbers.at(3) = 99; }
        catch (const std::out_of_range& error) { std::cout << "Rejected: " << error.what() << '\n'; }
    } // unique_ptr frees the array here.
    std::cout << "Array released automatically.\n";
}
