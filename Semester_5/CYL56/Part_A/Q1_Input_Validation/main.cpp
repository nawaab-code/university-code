#include <iostream>
#include <regex>
#include <string>

bool email_ok(const std::string& email) {
    return std::regex_match(email, std::regex(R"([\w.%+-]+@[\w.-]+\.[A-Za-z]{2,})"));
}

bool age_ok(const std::string& age) {
    if (!std::regex_match(age, std::regex(R"([0-9]{1,3})"))) return false;
    int n = std::stoi(age);
    return n >= 1 && n <= 120;
}

int main() {
    for (const auto& email : {"alice@example.com", "bad@@example.com"})
        std::cout << email << ": " << (email_ok(email) ? "YES" : "NO") << '\n';
    for (const auto& age : {"25", "0", "121", "abc"})
        std::cout << age << ": " << (age_ok(age) ? "YES" : "NO") << '\n';

    std::string email, age;
    std::cout << "Email: "; std::getline(std::cin, email);
    std::cout << "Age: "; std::getline(std::cin, age);
    std::cout << "Email valid? " << (email_ok(email) ? "YES" : "NO") << '\n';
    std::cout << "Age valid? " << (age_ok(age) ? "YES" : "NO") << '\n';
}
