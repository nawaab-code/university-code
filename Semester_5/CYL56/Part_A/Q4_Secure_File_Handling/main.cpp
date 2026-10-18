#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>

namespace fs = std::filesystem;
const fs::path root = "safe_data";

fs::path safe_path(const fs::path& name) {
    if (name.empty() || name.is_absolute()) throw std::invalid_argument("absolute/empty path");
    fs::path path = root;
    for (const auto& part : name) {
        if (part == ".." || part == ".") throw std::invalid_argument("path traversal");
        path /= part;
        if (fs::is_symlink(fs::symlink_status(path))) throw std::invalid_argument("symlink");
    }
    return path;
}

int main() {
    fs::create_directory(root);
    if (fs::is_symlink(fs::symlink_status(root))) throw std::invalid_argument("root symlink");
    std::ofstream out(safe_path("note.txt"));
    if (!(out << "Safe content\n")) throw std::runtime_error("write failed");
    out.close();
    std::ifstream file(safe_path("note.txt"));
    if (!file) throw std::runtime_error("read failed");
    std::string line;
    std::getline(file, line);
    std::cout << "Read: " << line << '\n';
    for (const auto& attack : {fs::path("../secret.txt"), fs::path("/etc/passwd")}) {
        try { std::ifstream blocked(safe_path(attack)); }
        catch (const std::invalid_argument& error) {
            std::cout << "Rejected " << attack << ": " << error.what() << '\n';
        }
    }
}
