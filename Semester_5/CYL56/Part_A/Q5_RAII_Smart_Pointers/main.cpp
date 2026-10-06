#include <cstddef>
#include <iostream>
#include <memory>
#include <stdexcept>

class IntegerArray {
    std::size_t size_;
    std::unique_ptr<int[]> data_;
public:
    explicit IntegerArray(std::size_t size) : size_(size), data_(std::make_unique<int[]>(size)) {}
    int& at(std::size_t index) {
        if (index >= size_) throw std::out_of_range("array index out of bounds");
        return data_[index];
    }
    const int& at(std::size_t index) const {
        if (index >= size_) throw std::out_of_range("array index out of bounds");
        return data_[index];
    }
};

int main() {
    {
        IntegerArray numbers(3);
        numbers.at(0) = 10;
        numbers.at(2) = 30;
        std::cout << "First: " << numbers.at(0) << ", last: " << numbers.at(2) << '\n';
        try { std::cout << numbers.at(3); }
        catch (const std::out_of_range& e) { std::cout << "Rejected: " << e.what() << '\n'; }
    } // unique_ptr releases the array here.
    std::cout << "Array scope ended; memory released automatically.\n";
}
