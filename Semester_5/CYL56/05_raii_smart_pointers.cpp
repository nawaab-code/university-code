#include <cstddef>
#include <iostream>
#include <memory>
#include <stdexcept>

class SafeIntegerArray {
public:
    explicit SafeIntegerArray(std::size_t size)
        : size_(size), values_(std::make_unique<int[]>(size)) {
        std::cout << "Allocated " << size_ << " integers\n";
    }

    ~SafeIntegerArray() {
        std::cout << "Array object left scope; smart pointer released the memory\n";
    }

    SafeIntegerArray(const SafeIntegerArray&) = delete;
    SafeIntegerArray& operator=(const SafeIntegerArray&) = delete;

    int& at(std::size_t index) {
        checkIndex(index);
        return values_[index];
    }

    const int& at(std::size_t index) const {
        checkIndex(index);
        return values_[index];
    }

    std::size_t size() const noexcept {
        return size_;
    }

private:
    void checkIndex(std::size_t index) const {
        if (index >= size_) {
            throw std::out_of_range("Array index " + std::to_string(index) +
                                    " is outside the valid range");
        }
    }

    std::size_t size_;
    std::unique_ptr<int[]> values_;
};

int main() {
    try {
        SafeIntegerArray numbers(5);
        for (std::size_t index = 0; index < numbers.size(); ++index) {
            numbers.at(index) = static_cast<int>((index + 1) * 10);
        }

        std::cout << "Element at index 2: " << numbers.at(2) << '\n';
        std::cout << numbers.at(8) << '\n';
    } catch (const std::out_of_range& error) {
        std::cout << "Bounds check caught: " << error.what() << '\n';
    }
}
