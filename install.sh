
set -e

rm third-party -rf

conan export fmt/
conan export gtest/
conan export spdlog/
conan export xyzlabs/
conan export imgui/
conan export implot/

conan install xyzlabs/ --build=missing --settings build_type=Release --output-folder=./third-party/gcc --deployer=full_deploy --profile:all=$(pwd)/profiles/gcc
conan install xyzlabs/ --build=missing --settings build_type=Release --output-folder=./third-party/clang --deployer=full_deploy --profile:all=$(pwd)/profiles/clang

rm -f CMakeUserPresets.json
