from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get


class SDL(ConanFile):
    name = "sdl"
    version = "3.4.14"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/libsdl-org/SDL/"
    settings = "os", "compiler", "build_type", "arch"
    # SDL3 builds a shared library by default. Declaring it lets CMakeDeps point the
    # target at SDL3.dll on Windows, so consumers can copy it with $<TARGET_RUNTIME_DLLS>.
    package_type = "shared-library"
    exports_sources = "src/*", "include/*"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/releases/download/release-{self.version}/SDL3-{self.version}.tar.gz")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"SDL3-3.4.14"
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["SDL3"]

    def deploy(self):
        self.copy("*", src="include", dst="include")
        self.copy("*", src="lib", dst="lib")
        self.copy_deps("*")
