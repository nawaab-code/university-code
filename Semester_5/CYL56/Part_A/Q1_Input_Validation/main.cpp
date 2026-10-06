#include <iostream>
#include <regex>
#include <string>

bool valid_email(const std::string& value) {
    // A practical classroom pattern; full RFC email syntax needs a dedicated parser.
    static const std::regex pattern(R"(^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$)");
    return std::regex_match(value, pattern);
}

bool valid_age(const std::string& value) {
    static const std::regex digits(R"(^[0-9]{1,3}$)");
    if (!std::regex_match(value, digits)) return false;
    const int age = std::stoi(value);
    return age >= 1 && age <= 120;
}

int main() {
    for (const std::string email : {"alice@example.com", "bad@@example.com", "a@site"}) {
        std::cout << "Email " << email << ": " << (valid_email(email) ? "YES" : "NO") << '\n';
    }
    for (const std::string age : {"25", "0", "121", "twenty"}) {
        std::cout << "Age " << age << ": " << (valid_age(age) ? "YES" : "NO") << '\n';
    }
    std::string email, age;
    std::cout << "Enter email: ";
    std::getline(std::cin, email);
    std::cout << "Enter age: ";
    std::getline(std::cin, age);
    std::cout << "Your email: " << (valid_email(email) ? "YES" : "NO") << '\n';
    std::cout << "Your age: " << (valid_age(age) ? "YES" : "NO") << '\n';
}
