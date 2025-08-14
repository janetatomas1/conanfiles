
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get

class ImGui(ConanFile):
    name = "imgui"
    commit = "68818c1388515eb986227ed44ef03385f86a5d4a"
    version = "1.90.5"
    license = ""
    author = ""
    url = "https://github.com/ocornut/imgui"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f'https://github.com/ocornut/{self.name}/archive/refs/tags/v{self.version}.tar.gz')

    def _configure_cmake(self):
        variables = {
            'CMAKE_CXX_COMPILER': "clang++",
            'CMAKE_C_COMPILER': 'clang'
        } if self.settings.compiler == "clang" else {}
        variables["IMGUI_DIR"] = f"{self.build_folder}/{self.name}-{self.version}"
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/",
            variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
