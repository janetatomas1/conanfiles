
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps


class XYZLabs(ConanFile):
    name = "xyzlabs"
    version = "1.0.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/janetatomas1/xyzlabs"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "include/*"
    requires = [
        "glfw/3.4",
        "spdlog/1.15.3",
        "boost/1.88.0"
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(
            'git clone git@github.com:janetatomas1/xyzlabs.git --recursive',
            cwd=self.source_folder
        )

    def _configure_cmake(self):
        variables = {'CMAKE_CXX_COMPILER': "clang++"} if self.settings.compiler == "clang" else {}
        variables["CMAKE_TOOLCHAIN_FILE"] = f"{self.build_folder}/conan_toolchain.cmake"
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/{self.name}",
            variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
