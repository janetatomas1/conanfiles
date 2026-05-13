from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


class ContiniumWave(ConanFile):
    name = "continiumwave"
    version = "3.0.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "http://192.168.0.101:3000/tomas.janeta/xyzlabs.git"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "include/*"
    requires = [
        "xyzlabs/5.0.0",
        "xtensor/0.26.0",
        "stb/cci.20240531",
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(
            f"git clone git@github.com:janetatomas1/xyzlabs.git --recursive && cd xyzlabs && git checkout {self.version}",
            cwd=self.source_folder,
        )

    def _configure_cmake(self):
        variables = (
            {"CMAKE_CXX_COMPILER": "clang++", "CMAKE_C_COMPILER": "clang"}
            if self.settings.compiler == "clang"
            else {}
        )
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/{self.name}", variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
