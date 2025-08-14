
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get


class FMT(ConanFile):
    name = "fmt"
    version = "11.1.3"
    license = "fmt"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/fmtlib/fmt"
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
        get(self, f"{self.url}/archive/refs/tags/{self.version}.zip")

    def _configure_cmake(self):
        variables = {
            'CMAKE_CXX_COMPILER': "clang++",
            'CMAKE_C_COMPILER': 'clang'
        } if self.settings.compiler == "clang" else {}
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/{self.name}-{self.version}",
            variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
