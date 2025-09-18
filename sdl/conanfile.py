
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get

class SDL(ConanFile):
    name = "sdl"
    version = "3.2.22"
    license = "Proprietary"
    url = "https://github.com/libsdl-org/SDL"
    settings = "os", "compiler", "build_type", "arch"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f'{self.url}/releases/download/release-{self.version}/SDL3-{self.version}.tar.gz')

    def _configure_cmake(self):
        variables = {
            'CMAKE_CXX_COMPILER': "clang++",
            'CMAKE_C_COMPILER': 'clang'
        } if self.settings.compiler == "clang" else {}
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/SDL3-{self.version}",
            variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
