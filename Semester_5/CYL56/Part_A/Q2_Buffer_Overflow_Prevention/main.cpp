#include <cstring>
#include <iostream>
#include <stdexcept>
#include <string>

class SafeBuffer {
    char data[16]{}; // 15 characters and a terminating '\0'.
public:
    void store(const std::string& text) {
        if (text.size() >= sizeof(data)) throw std::length_error("buffer is full");
        std::memcpy(data, text.c_str(), text.size() + 1);
    }
    const char* get() const { return data; }
};

int main() {
    SafeBuffer buffer;
    for (const auto& text : {"safe input", "this string is too long"}) {
        try {
            buffer.store(text);
            std::cout << "Stored: " << buffer.get() << '\n';
        } catch (const std::length_error& error) {
            std::cout << "Rejected: " << error.what() << '\n';
        }
    }
}
