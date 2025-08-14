
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class ImPlot3D(ConanFile):
    name = "implot3d"
    commit = "68818c1388515eb986227ed44ef03385f86a5d4a"
    version = "0.2.0"
    license = ""
    author = ""
    url = "https://github.com/brenocq/implot3d"
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
        variables = {'CMAKE_CXX_COMPILER': "clang++"} if self.settings.compiler == "clang" else {}
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
