
set -e

rm third-party -rf

conan export fmt/
conan export gtest/
conan export spdlog/
conan export ompl/
conan export xyzlabs/
conan export dataframe/
conan export imgui/
conan export implot/
conan export implot3d/
conan export opencv/
conan export bgfx/

conan install abstractpackage/ --build=missing --output-folder=./third-party/gcc --deployer-folder=third-party/gcc --deployer=full_deploy --profile:all=$(pwd)/profiles/gcc
conan install abstractpackage/ --build=missing --output-folder=./third-party/clang --deployer-folder=third-party/clang --deployer=full_deploy --profile:all=$(pwd)/profiles/clang

rm -f CMakeUserPresets.json
