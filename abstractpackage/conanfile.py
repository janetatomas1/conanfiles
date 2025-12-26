from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get


class AbstractPackage(ConanFile):
    name = "abstractpackage"
    version = "0.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/janetatomas1/conanfiles"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "include/*"

    def requirements(self):
        deps = [
            "glfw/3.4",
            "spdlog/1.15.3",
            "boost/1.88.0",
            "xtensor/0.26.0",
            "pybind11/3.0.1",
            "ompl/1.7.0",
            "xyzlabs/3.0.0",
            "dataframe/3.6.0",
            "imgui/1.92.0",
            "implot/0.16.0",
            "implot3d/0.2.0",
            "stb/cci.20240531",
            "nlohmann_json/3.11.3",
            "concurrentqueue/1.0.4",
            "gtest/1.17.0",
            "pocketfft/0.0.0.cci.20240801",
            "sdl/3.2.22",
        ]

        if self.settings.compiler == "gcc":
            deps.append("symengine/0.14.0")
            deps.append("opencv/4.12.0")
            deps.append("open3d/0.19.0")
            deps.append("magnum/1.0.0")

        for d in deps:
            self.requires(d)

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
