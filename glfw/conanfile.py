
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get


class GLFW(ConanFile):
    name = "glfw"
    version = "3.4"
    license = "ZLIB license"
    author = ""
    url = "https://github.com/glfw/glfw"
    settings = "os", "compiler", "build_type", "arch"
    package_type = "library"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/archive/refs/tags/{self.version}.tar.gz")

    def _configure_cmake(self):
        variables = (
            {"CMAKE_CXX_COMPILER": "clang++", "CMAKE_C_COMPILER": "clang"}
            if self.settings.compiler == "clang"
            else {}
        )
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

    def package_info(self):
        self.cpp_info.libs = ["glfw3"]
