#include <array>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include <string>

class SafeBuffer {
    std::array<char, 16> data_{}; // 15 characters plus the NUL terminator.
public:
    void store(const std::string& value) {
        if (value.size() >= data_.size()) {
            throw std::length_error("input exceeds 15-character buffer capacity");
        }
        std::memcpy(data_.data(), value.c_str(), value.size() + 1);
    }
    const char* value() const { return data_.data(); }
};

int main() {
    SafeBuffer buffer;
    for (const std::string input : {"safe input", "this string is too long"}) {
        try {
            buffer.store(input);
            std::cout << "Stored: " << buffer.value() << '\n';
        } catch (const std::length_error& error) {
            std::cout << "Rejected: " << error.what() << '\n';
        }
    }
}
