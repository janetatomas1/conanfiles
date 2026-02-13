from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


class XYZLabs(ConanFile):
    name = "xyzlabs"
    version = "3.0.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/janetatomas1/xyzlabs"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "include/*"

    def requirements(self):
        self.requires("imgui/1.92.0")

        for r in [
            "glfw/3.4",
            "spdlog/1.15.3",
            "boost/1.88.0",
            "implot/0.16.0",
            "stb/cci.20240531",
            "nlohmann_json/3.11.3",
            "concurrentqueue/1.0.4",
            "glew/2.2.0",
        ]:
            self.requires(r)

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
