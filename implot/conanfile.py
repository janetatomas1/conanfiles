
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class ImPlot3D(ConanFile):
    name = "implot"
    commit = "3da8bd34299965d3b0ab124df743fe3e076fa222"
    version = "0.16.0"
    license = ""
    author = ""
    url = "https://github.com/epezent/implot"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"
    requires = [
        "imgui/1.90.5"
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(f'git clone {self.url} && cd {self.name} && git checkout {self.commit}')

    def _configure_cmake(self):
        variables = {
            'CMAKE_CXX_COMPILER': "clang++",
            'CMAKE_C_COMPILER': 'clang'
        } if self.settings.compiler == "clang" else {}
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
