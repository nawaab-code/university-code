#include <iostream>
#include <regex>
#include <string>
#include <vector>

bool isValidEmail(const std::string& email) {
    static const std::regex pattern(
        R"(^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$)");
    return std::regex_match(email, pattern);
}

bool isValidAge(const std::string& age) {
    static const std::regex digits(R"(^[0-9]{1,3}$)");
    if (!std::regex_match(age, digits)) {
        return false;
    }

    const int value = std::stoi(age);
    return value >= 1 && value <= 120;
}

int main() {
    const std::vector<std::string> emails = {
        "student@example.com", "student.example.com", "user@domain"
    };
    const std::vector<std::string> ages = {"21", "0", "121", "twenty"};

    std::cout << "Email validation (YES = valid)\n";
    for (const auto& email : emails) {
        std::cout << email << ": " << (isValidEmail(email) ? "YES" : "NO") << '\n';
    }

    std::cout << "\nAge validation (YES = valid)\n";
    for (const auto& age : ages) {
        std::cout << age << ": " << (isValidAge(age) ? "YES" : "NO") << '\n';
    }
}
