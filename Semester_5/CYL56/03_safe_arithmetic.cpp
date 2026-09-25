#include <iostream>
#include <limits>
#include <stdexcept>

long long safeAdd(long long left, long long right) {
    const auto maximum = std::numeric_limits<long long>::max();
    const auto minimum = std::numeric_limits<long long>::min();

    if ((right > 0 && left > maximum - right) ||
        (right < 0 && left < minimum - right)) {
        throw std::overflow_error("signed integer addition overflow");
    }
    return left + right;
}

long long safeMultiply(long long left, long long right) {
    const auto maximum = std::numeric_limits<long long>::max();
    const auto minimum = std::numeric_limits<long long>::min();

    if (left == 0 || right == 0) {
        return 0;
    }

    const bool overflow =
        (left > 0 && right > 0 && left > maximum / right) ||
        (left > 0 && right < 0 && right < minimum / left) ||
        (left < 0 && right > 0 && left < minimum / right) ||
        (left < 0 && right < 0 && left < maximum / right);

    if (overflow) {
        throw std::overflow_error("signed integer multiplication overflow");
    }
    return left * right;
}

int main() {
    try {
        std::cout << "120 + 30 = " << safeAdd(120, 30) << '\n';
        std::cout << "12 * -4 = " << safeMultiply(12, -4) << '\n';

        const auto maximum = std::numeric_limits<long long>::max();
        std::cout << safeAdd(maximum, 1) << '\n';
    } catch (const std::overflow_error& error) {
        std::cout << "Exception caught: " << error.what() << '\n';
    }

    try {
        const auto maximum = std::numeric_limits<long long>::max();
        std::cout << safeMultiply(maximum, 2) << '\n';
    } catch (const std::overflow_error& error) {
        std::cout << "Exception caught: " << error.what() << '\n';
    }
}
