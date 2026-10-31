import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get


class GLObjects(ConanFile):
    name = "globjects"
    version = "2.0.0"
    commit = "10c1ce98944212656805a2c0533e5b29ded9bc14"
    author = ""
    url = "https://github.com/cginternals/globjects"
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

    def requirements(self):
        # globjects' public headers include glbinding and glm.
        self.requires("glbinding/3.5.0", transitive_headers=True)
        self.requires("glm/1.0.1", transitive_headers=True)
        # glbinding's headers include KHR/khrplatform.h but its package doesn't
        # expose it; linux finds the system copy, windows has none.
        self.requires("khrplatform/cci.20200529", transitive_headers=True)

    def generate(self):
        tc = CMakeToolchain(self)
        # globjects' CMakeLists doesn't link khrplatform, so add its include dir directly
        khr_include = os.path.join(self.dependencies["khrplatform"].package_folder, "include")
        tc.cache_variables["CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES"] = khr_include.replace("\\", "/")
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/archive/{self.commit}.tar.gz")

    def _configure_cmake(self):
        variables = {
            'BUILD_SHARED_LIBS': 'ON' if self.options.shared else 'OFF',
            'OPTION_BUILD_TESTS': 'OFF',
            'OPTION_BUILD_EXAMPLES': 'OFF',
            'OPTION_BUILD_DOCS': 'OFF',
        }
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/{self.name}-{self.commit}",
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
        self.cpp_info.libs = ["globjectsd" if self.settings.build_type == "Debug" else "globjects"]
