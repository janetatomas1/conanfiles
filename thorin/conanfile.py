from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


class Thorin(ConanFile):
    name = "thorin"
    version = "0.2.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/janetatomas1/thorin.git"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "include/*"

    def requirements(self):
        for r in [
            "yoga/3.2.0",
            "function2/4.2.5",
            "sdl/3.4.14",
            "spdlog/1.17.0",
            "implot/1.0",
            "implot3d/1.0",
            "stb/cci.20240531",
            "nlohmann_json/3.11.3",
            "concurrentqueue/1.0.4",
            "imgui/1.92.9b-docking",
            "gtest/1.17.0",
            "glbinding/3.5.0",
            "opengl/system",
            "globjects/2.0.0",
            "dawn/20261023.194543",
            "sdl3webgpu/1.0",
        ]:
            self.requires(r, transitive_headers=True)

        # libassert depends on cpptrace, which does not support Emscripten
        if self.settings.os != "Emscripten":
            self.requires("libassert/2.2.1", transitive_headers=True)

        # Vulkan is not available on Emscripten
        if self.settings.os != "Emscripten":
            # vulkan-headers also ships vulkan-hpp (vulkan/vulkan.hpp)
            # force: vk-bootstrap/1.4.350 pins vulkan-headers/1.4.350.0
            self.requires("vulkan-headers/1.4.357.0", transitive_headers=True, force=True)
            for r in [
                "volk/1.4.357.0",
                "vk-bootstrap/1.4.350",
                "vulkan-memory-allocator/3.3.0",
            ]:
                self.requires(r, transitive_headers=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(
            f"git clone {self.url} --recursive && cd thorin && git checkout {self.version}",
            cwd=self.source_folder,
        )

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/{self.name}"
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["thorin"]

    def deploy(self):
        self.copy("*", src="include", dst="include")
        self.copy("*", src="lib", dst="lib")
        self.copy_deps("*")
