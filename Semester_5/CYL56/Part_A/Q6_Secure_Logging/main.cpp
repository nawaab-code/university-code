#include <chrono>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>

enum class Severity { INFO, WARNING, ERROR };

class Logger {
    std::ofstream out_;
public:
    explicit Logger(const std::string& path) : out_(path, std::ios::app) {
        if (!out_) throw std::runtime_error("cannot open log file: " + path);
    }
    void log(Severity level, const std::string& message) {
        if (message.empty()) throw std::invalid_argument("log message cannot be empty");
        const char* label = level == Severity::INFO ? "INFO" : level == Severity::WARNING ? "WARNING" : "ERROR";
        auto now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        out_ << std::put_time(std::localtime(&now), "%Y-%m-%d %H:%M:%S") << " [" << label << "] " << message << '\n';
        out_.flush();
        if (!out_) throw std::runtime_error("log write failed");
    }
};

int main() {
    try {
        Logger log("app.log");
        log.log(Severity::INFO, "Application started");
        log.log(Severity::WARNING, "Failed login detected");
        log.log(Severity::ERROR, "Example error");
        try { log.log(Severity::INFO, ""); }
        catch (const std::invalid_argument& e) { std::cout << "Rejected: " << e.what() << '\n'; }
        std::cout << "Wrote three entries to app.log\n";
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
