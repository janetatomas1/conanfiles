
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import pathlib

class ImGui(ConanFile):
    name = "imgui"
    commit = "68818c1388515eb986227ed44ef03385f86a5d4a"
    version = "1.92.0"
    license = ""
    author = ""
    url = "https://github.com/ocornut/imgui"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"
    options = {
        "window_backend": ["GLFW", "SDL"],
    }
    default_options = {
        "window_backend": "SDL",
    }

    def requirements(self):
        if self.options.window_backend == "GLFW":
            self.requires("glfw/3.4")
        else:
            self.requires("sdl/3.2.22")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f'{self.url}/archive/refs/tags/v{self.version}.tar.gz')

    def _configure_cmake(self):
        variables = {
            'CMAKE_CXX_COMPILER': "clang++",
            'CMAKE_C_COMPILER': 'clang'
        } if self.settings.compiler == "clang" else {}
        variables["IMGUI_DIR"] = pathlib.PureWindowsPath(f"{self.build_folder}/{self.name}-{self.version}").as_posix()
        variables["USE_GLFW"] = self.options.window_backend == "GLFW"
        variables["USE_SDL"] = self.options.window_backend == "SDL"
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
