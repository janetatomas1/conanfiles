
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get


class GTest(ConanFile):
    name = "gtest"
    version = "1.16.0"
    license = "MIT"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/google/googletest"
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
        variables = {
            'CMAKE_CXX_COMPILER': "clang++",
            'CMAKE_C_COMPILER': 'clang'
        } if self.settings.compiler == "clang" else {}
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/googletest-{self.version}",
            variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
