#include <filesystem>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>

namespace fs = std::filesystem;

class SecureFileHandler {
public:
    explicit SecureFileHandler(fs::path baseDirectory)
        : baseDirectory_(fs::absolute(std::move(baseDirectory)).lexically_normal()) {
        fs::create_directories(baseDirectory_);
        baseDirectory_ = fs::weakly_canonical(baseDirectory_);
    }

    void write(const fs::path& relativePath, const std::string& contents) const {
        const fs::path path = validate(relativePath);
        std::ofstream output(path);
        if (!output) {
            throw std::runtime_error("Could not open safe path for writing");
        }
        output << contents;
    }

    std::string read(const fs::path& relativePath) const {
        const fs::path path = validate(relativePath);
        std::ifstream input(path);
        if (!input) {
            throw std::runtime_error("Could not open safe path for reading");
        }
        return {std::istreambuf_iterator<char>(input),
                std::istreambuf_iterator<char>()};
    }

private:
    fs::path validate(const fs::path& userPath) const {
        if (userPath.empty() || userPath.is_absolute()) {
            throw std::invalid_argument("Only non-empty relative paths are allowed");
        }

        static const std::set<std::string> sensitiveDirectories = {
            "dev", "etc", "proc", "root", "sys", "system32", "windows"
        };

        for (const auto& component : userPath) {
            const std::string value = component.string();
            if (value == ".." || sensitiveDirectories.count(value) != 0) {
                throw std::invalid_argument("Unsafe path component: " + value);
            }
        }

        const fs::path candidate =
            fs::weakly_canonical(baseDirectory_ / userPath);
        if (!isInsideBase(candidate)) {
            throw std::invalid_argument("Path escapes the permitted directory");
        }
        return candidate;
    }

    bool isInsideBase(const fs::path& candidate) const {
        auto basePart = baseDirectory_.begin();
        auto candidatePart = candidate.begin();
        while (basePart != baseDirectory_.end()) {
            if (candidatePart == candidate.end() || *basePart != *candidatePart) {
                return false;
            }
            ++basePart;
            ++candidatePart;
        }
        return true;
    }

    fs::path baseDirectory_;
};

int main() {
    try {
        SecureFileHandler files("safe_files");
        files.write("message.txt", "Secure file contents\n");
        std::cout << "Safe read succeeded: " << files.read("message.txt");

        files.read("../../etc/passwd");
    } catch (const std::exception& error) {
        std::cout << "Malicious path rejected: " << error.what() << '\n';
    }
}
