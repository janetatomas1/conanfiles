from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get


class Open3D(ConanFile):
    name = "open3d"
    version = "0.19.0"
    license = "MIT"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/isl-org/Open3D/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"header_only": [True, False]}
    default_options = {"header_only": False}
    requires = []

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/archive/refs/tags/v{self.version}.tar.gz")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/Open3D-{self.version}"
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
