import pathlib

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


class ImPlot3D(ConanFile):
    name = "implot"
    commit = "3da8bd34299965d3b0ab124df743fe3e076fa222"
    version = "1.0"
    license = ""
    author = ""
    url = "https://github.com/epezent/implot"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = ["CMakeLists.txt", "implotConfig.cmake.in"]
    requires = ["imgui/1.92.0"]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(
            f"git clone {self.url} && cd {self.name} && git checkout {self.commit}"
        )

    def _configure_cmake(self):
        variables = (
            {"CMAKE_CXX_COMPILER": "clang++", "CMAKE_C_COMPILER": "clang"}
            if self.settings.compiler == "clang"
            else {}
        )
        variables["IMPLOT_DIR"] = pathlib.PureWindowsPath(
            f"{self.build_folder}/{self.name}"
        ).as_posix()
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/", variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package_info(self):
        self.cpp_info.components["core"].libs = ["implot"]
        self.cpp_info.libs = ["implot"]

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
