from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


class AbstractPackage(ConanFile):
    name = "abstractpackage"
    version = "5.0.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/janetatomas1/xyzlabs.git"
    settings = "os", "compiler", "build_type", "arch"
    requires = [
        "xyzlabs/5.0.0",
        "opencv/4.12.0",
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        pass

    def build(self):
        pass

    def package(self):
        pass
