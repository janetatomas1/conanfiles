
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get

class DataFrame(ConanFile):
    name = "dataframe"
    version = "3.6.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/hosseinmoein/DataFrame"
    settings = "os", "compiler", "build_type", "arch"
    requires = []

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f'https://github.com/hosseinmoein/DataFrame/archive/refs/tags/{self.version}.tar.gz')

    def _configure_cmake(self):
        variables = {
            'CMAKE_CXX_COMPILER': "clang++",
            'CMAKE_C_COMPILER': 'clang'
        } if self.settings.compiler == "clang" else {}
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/DataFrame-{self.version}",
            variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
