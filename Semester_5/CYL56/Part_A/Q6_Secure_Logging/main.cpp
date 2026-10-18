#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>

class Logger {
    std::ofstream file;
public:
    explicit Logger(const std::string& name) : file(name, std::ios::app) {
        if (!file) throw std::runtime_error("cannot open log");
    }
    void log(const std::string& level, const std::string& message) {
        if (message.empty()) throw std::invalid_argument("empty message");
        std::time_t now = std::time(nullptr);
        file << std::put_time(std::localtime(&now), "%Y-%m-%d %H:%M:%S")
             << " [" << level << "] " << message << '\n';
        file.flush();
        if (!file) throw std::runtime_error("log write failed");
    }
};

int main() {
    Logger log("app.log");
    log.log("INFO", "Started");
    log.log("WARNING", "Failed login");
    log.log("ERROR", "Example error");
    try { log.log("INFO", ""); }
    catch (const std::invalid_argument& error) { std::cout << "Rejected: " << error.what() << '\n'; }
    std::cout << "Wrote three log entries.\n";
}
