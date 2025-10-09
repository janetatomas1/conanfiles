
rmdir /s /q third-party

conan export fmt/
conan export spdlog/
conan export xyzlabs/
conan export imgui/
conan export implot/
conan export implot3d/

conan install abstractpackage/ --build=missing --output-folder=./third-party/gcc --deployer-folder=third-party/gcc --deployer=full_deploy --profile:all=%CD%/profiles/msvc

 CMakeUserPresets.json
