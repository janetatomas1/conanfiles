import pathlib

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import get


class ImGui(ConanFile):
    name = "imgui"
    commit = "68818c1388515eb986227ed44ef03385f86a5d4a"
    version = "1.92.9b-docking"
    license = ""
    author = ""
    url = "https://github.com/ocornut/imgui"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = [
        "CMakeLists.txt",
        "imguiConfig.cmake.in",
    ]
    requires = ["sdl/3.4.14"]
    package_type = "library"
    # Renderer backends to build; imgui_impl_sdl3 is always built.
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "opengl": [True, False],
        "sdlgpu": [True, False],
        "webgpu": [True, False],
        "vulkan": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
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

    def requirements(self):
        if self.options.webgpu:
            self.requires("dawn/20261023.194543", transitive_headers=True)
        # imgui_impl_vulkan; same version ironcast forces (vk-bootstrap pins an older one)
        if self.options.get_safe("vulkan"):
            self.requires("vulkan-headers/1.4.357.0", transitive_headers=True, force=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["IMGUI_OPENGL"] = bool(self.options.opengl)
        tc.variables["IMGUI_SDLGPU"] = bool(self.options.get_safe("sdlgpu"))
        tc.variables["IMGUI_WEBGPU"] = bool(self.options.webgpu)
        tc.variables["IMGUI_VULKAN"] = bool(self.options.get_safe("vulkan"))
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/archive/refs/tags/v{self.version}.tar.gz")

    def _configure_cmake(self):
        variables = {"IMGUI_DIR": pathlib.PureWindowsPath(f"{self.build_folder}/{self.name}-{self.version}").as_posix()}
        cmake = CMake(self)
        cmake.configure(
            build_script_folder=f"{self.build_folder}/", variables=variables
        )
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.components["core"].libs = ["imgui"]
        self.cpp_info.libs = ["imgui"]
        self.cpp_info.defines = []
        if self.options.webgpu:
            self.cpp_info.defines.append("IMGUI_IMPL_WEBGPU_BACKEND_DAWN")
        if self.options.get_safe("vulkan"):
            self.cpp_info.defines.append("IMGUI_IMPL_VULKAN_NO_PROTOTYPES")
