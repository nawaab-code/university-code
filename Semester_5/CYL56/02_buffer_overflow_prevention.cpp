#include <algorithm>
#include <array>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>

template <std::size_t Capacity>
class SafeBuffer {
    static_assert(Capacity > 0, "Buffer capacity must be positive");

public:
    void store(const std::string& input) {
        if (input.size() >= Capacity) {
            throw std::length_error(
                "Input needs " + std::to_string(input.size() + 1) +
                " bytes, but buffer capacity is " + std::to_string(Capacity));
        }

        buffer_.fill('\0');
        std::copy(input.begin(), input.end(), buffer_.begin());
    }

    const char* data() const noexcept {
        return buffer_.data();
    }

    static constexpr std::size_t capacity() noexcept {
        return Capacity;
    }

private:
    std::array<char, Capacity> buffer_{};
};

int main() {
    SafeBuffer<16> buffer;

    try {
        buffer.store("Secure input");
        std::cout << "Stored safely: " << buffer.data() << '\n';

        buffer.store("This text is too long for the fixed buffer");
    } catch (const std::length_error& error) {
        std::cout << "Overflow prevented: " << error.what() << '\n';
    }
}
