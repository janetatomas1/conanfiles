from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


class Ironcast(ConanFile):
    name = "ironcast"
    version = "0.4.0"
    license = "Proprietary"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/janetatomas1/ironcast.git"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "include/*"

    # Backend libraries to build: ironcast::opengl, ironcast::sdlgpu, ironcast::webgpu and ironcast::vulkan.
    options = {
        "opengl": [True, False],
        "sdlgpu": [True, False],
        "webgpu": [True, False],
        "vulkan": [True, False],
    }
    default_options = {
        "opengl": True,
        "sdlgpu": True,
        "webgpu": True,
        "vulkan": True,
    }

    def config_options(self):
        # SDL_GPU has no web driver, and there is no Vulkan in the browser
        if self.settings.os == "Emscripten":
            del self.options.sdlgpu
            del self.options.vulkan

    def configure(self):
        # imgui builds only the renderer backends ironcast uses
        for backend in ["opengl", "sdlgpu", "webgpu", "vulkan"]:
            if self.options.get_safe(backend) is not None:
                setattr(self.options["imgui"], backend, self.options.get_safe(backend))

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
        ]:
            self.requires(r, transitive_headers=True)

        # libassert depends on cpptrace, which does not support Emscripten
        if self.settings.os != "Emscripten":
            self.requires("libassert/2.2.1", transitive_headers=True)

        if self.options.opengl:
            for r in ["glbinding/3.5.0", "opengl/system", "globjects/2.0.0"]:
                self.requires(r, transitive_headers=True)

        if self.options.webgpu:
            for r in ["dawn/20261023.194543", "sdl3webgpu/1.0"]:
                self.requires(r, transitive_headers=True)

        if self.options.get_safe("vulkan"):
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
        tc.variables["IRONCAST_OPENGL"] = bool(self.options.opengl)
        tc.variables["IRONCAST_SDLGPU"] = bool(self.options.get_safe("sdlgpu"))
        tc.variables["IRONCAST_WEBGPU"] = bool(self.options.webgpu)
        tc.variables["IRONCAST_VULKAN"] = bool(self.options.get_safe("vulkan"))
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(
            f"git clone {self.url} {self.name} --recursive && cd {self.name} && git checkout {self.version}",
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
        self.cpp_info.libs = ["ironcast"]

    def deploy(self):
        self.copy("*", src="include", dst="include")
        self.copy("*", src="lib", dst="lib")
        self.copy_deps("*")
