import shutil

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get


class OpenCV(ConanFile):
    name = "opencv"
    version = "4.12.0"
    url = "https://github.com/opencv/opencv"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "include/*"
    requires = []

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/archive/refs/tags/{self.version}.tar.gz")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/{self.name}-{self.version}"
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        shutil.copytree(
            f"{self.package_folder}/include/opencv4/opencv2",
            f"{self.package_folder}/include/opencv2",
        )
