import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get, replace_in_file


class GTest(ConanFile):
    name = "gtest"
    version = "1.17.0"
    license = "BSD-3-Clause"
    author = ""
    url = "https://github.com/google/googletest"
    settings = "os", "compiler", "build_type", "arch"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/archive/refs/tags/v{self.version}.tar.gz", strip_root=True)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        # googletest builds with warnings as errors on msvc and clang-cl, so new
        # compiler warnings in its own headers break the build
        replace_in_file(
            self,
            os.path.join(self.source_folder, "googletest", "cmake", "internal_utils.cmake"),
            "-GS -W4 -WX",
            "-GS -W4",
        )
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        # Same names as googletest's own GTestConfig.cmake: find_package(GTest), GTest::gtest_main, ...
        self.cpp_info.set_property("cmake_file_name", "GTest")
        for lib, requires in [
            ("gtest", []),
            ("gtest_main", ["gtest"]),
            ("gmock", ["gtest"]),
            ("gmock_main", ["gmock"]),
        ]:
            component = self.cpp_info.components[lib]
            component.libs = [lib]
            component.requires = requires
            component.set_property("cmake_target_name", f"GTest::{lib}")
            if self.settings.os == "Linux":
                component.system_libs = ["pthread"]
