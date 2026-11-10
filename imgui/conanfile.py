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
    # Dear ImGui Test Engine, built into the library with the test_engine option. It has its own license
    # (imgui_test_engine/LICENSE.txt): free for individuals, open-source projects and small companies.
    test_engine_url = "https://github.com/ocornut/imgui_test_engine"
    test_engine_version = "1.92.9b"
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
        # Dear ImGui Test Engine, for GUI tests: its hooks in imgui (IMGUI_ENABLE_TEST_ENGINE) and the engine
        "test_engine": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "opengl": True,
        "sdlgpu": True,
        "webgpu": True,
        "vulkan": True,
        "test_engine": False,
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
        tc.variables["IMGUI_TEST_ENGINE"] = bool(self.options.test_engine)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        get(self, f"{self.url}/archive/refs/tags/v{self.version}.tar.gz")
        # Fetched whatever the options: source() is shared by every configuration
        get(self, f"{self.test_engine_url}/archive/refs/tags/v{self.test_engine_version}.tar.gz")

    def _configure_cmake(self):
        variables = {
            "IMGUI_DIR": pathlib.PureWindowsPath(f"{self.build_folder}/{self.name}-{self.version}").as_posix(),
            "IMGUI_TEST_ENGINE_DIR": pathlib.PureWindowsPath(
                f"{self.build_folder}/imgui_test_engine-{self.test_engine_version}/imgui_test_engine"
            ).as_posix(),
        }
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
        # With a component, CMakeDeps uses only the component's info: the defines have to be set on it.
        core = self.cpp_info.components["core"]
        core.libs = ["imgui"]
        if self.options.webgpu:
            core.defines.append("IMGUI_IMPL_WEBGPU_BACKEND_DAWN")
        if self.options.get_safe("vulkan"):
            core.defines.append("IMGUI_IMPL_VULKAN_NO_PROTOTYPES")
        if self.options.test_engine:
            core.defines += ["IMGUI_ENABLE_TEST_ENGINE", "IMGUI_TEST_ENGINE_ENABLE_COROUTINE_STDTHREAD_IMPL=1"]
            if self.settings.os == "Linux":
                core.system_libs.append("pthread")
