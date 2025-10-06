
rmdir /s /q third-party

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
conan export sdl/

conan install abstractpackage/ --build=missing --output-folder=./third-party/gcc --deployer-folder=third-party/gcc --deployer=full_deploy --profile:all=%CD%/profiles/msvc

rm CMakeUserPresets.json
