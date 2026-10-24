#include <iostream>
#include <regex>
#include <string>

bool email_ok(const std::string& email) {
    std::regex email_pattern(R"([\w.%+-]+@[\w.-]+\.[A-Za-z]{2,})");
    return std::regex_match(email, email_pattern);
}

bool age_ok(const std::string& age) {
    std::regex age_pattern(R"([0-9]{1,3})");

    // Check the text before converting it to an integer.
    if (!std::regex_match(age, age_pattern)) {
        return false;
    }

    int age_number = std::stoi(age);
    return age_number >= 1 && age_number <= 120;
}

int main() {
    // Store both inputs as text so they can be validated.
    std::string email;
    std::string age;

    // Prompt the user to enter their email and age.
    std::cout << "Email: ";
    std::getline(std::cin, email);

    std::cout << "Age: ";
    std::getline(std::cin, age);

    // Validate the user input and display the results.
    std::cout << "Email valid? " << (email_ok(email) ? "YES" : "NO") << '\n';
    std::cout << "Age valid? " << (age_ok(age) ? "YES" : "NO") << '\n';

    return 0;
}
