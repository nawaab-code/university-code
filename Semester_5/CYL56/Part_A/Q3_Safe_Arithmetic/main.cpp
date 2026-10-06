#include <iostream>
#include <limits>
#include <stdexcept>
#include <utility>

int safe_add(int a, int b) {
    const int max = std::numeric_limits<int>::max();
    const int min = std::numeric_limits<int>::min();
    if ((b > 0 && a > max - b) || (b < 0 && a < min - b)) {
        throw std::overflow_error("addition overflows int");
    }
    return a + b;
}

int safe_multiply(int a, int b) {
    const int max = std::numeric_limits<int>::max();
    const int min = std::numeric_limits<int>::min();
    if (a > 0) {
        if ((b > 0 && a > max / b) || (b < 0 && b < min / a))
            throw std::overflow_error("multiplication overflows int");
    } else if (a < 0) {
        if ((b > 0 && a < min / b) || (b < 0 && a < max / b))
            throw std::overflow_error("multiplication overflows int");
    }
    return a * b;
}

int main() {
    const int max = std::numeric_limits<int>::max();
    const int min = std::numeric_limits<int>::min();
    for (const auto& [a, b] : {std::pair{20, 22}, std::pair{max, 1}, std::pair{min, -1}}) {
        try { const int result = safe_add(a, b); std::cout << a << " + " << b << " = " << result << '\n'; }
        catch (const std::overflow_error& e) { std::cout << "Addition rejected: " << e.what() << '\n'; }
    }
    for (const auto& [a, b] : {std::pair{6, 7}, std::pair{max, 2}, std::pair{min, -1}}) {
        try { const int result = safe_multiply(a, b); std::cout << a << " * " << b << " = " << result << '\n'; }
        catch (const std::overflow_error& e) { std::cout << "Multiplication rejected: " << e.what() << '\n'; }
    }
}
