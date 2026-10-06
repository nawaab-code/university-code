#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

namespace fs = std::filesystem;

class SafeFiles {
    fs::path root_;
    fs::path resolve(const fs::path& relative) const {
        if (relative.empty() || relative.is_absolute()) throw std::invalid_argument("path must be relative");
        for (const auto& part : relative) {
            if (part == ".." || part == ".") throw std::invalid_argument("traversal components are forbidden");
        }
        const auto target = root_ / relative;
        // Reject symlinks in every existing component, including the target file.
        fs::path current = root_;
        for (const auto& part : relative) {
            current /= part;
            if (fs::is_symlink(fs::symlink_status(current))) throw std::invalid_argument("symlink is forbidden");
        }
        return target;
    }
public:
    explicit SafeFiles(const fs::path& root) : root_(fs::absolute(root).lexically_normal()) {
        fs::create_directories(root_);
        if (fs::is_symlink(fs::symlink_status(root_))) throw std::invalid_argument("root cannot be a symlink");
    }
    void write(const fs::path& path, const std::string& text) const {
        std::ofstream out(resolve(path), std::ios::binary | std::ios::trunc);
        if (!out || !(out << text)) throw std::runtime_error("write failed");
    }
    std::string read(const fs::path& path) const {
        std::ifstream in(resolve(path), std::ios::binary);
        if (!in) throw std::runtime_error("read failed");
        return {std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>()};
    }
};

int main() {
    try {
        SafeFiles files("safe_data");
        files.write("note.txt", "Confined file content\n");
        std::cout << "Safe read: " << files.read("note.txt");
        for (const fs::path& attack : {fs::path("../secret.txt"), fs::path("/etc/passwd")}) {
            try { std::cout << files.read(attack); }
            catch (const std::exception& e) { std::cout << "Rejected " << attack << ": " << e.what() << '\n'; }
        }
    } catch (const std::exception& e) {
        std::cerr << "File error: " << e.what() << '\n';
        return 1;
    }
}
