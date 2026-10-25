import pathlib

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import replace_in_file


class SDL3WebGPU(ConanFile):
    name = "sdl3webgpu"
    commit = "4fa9d70935e41c075f664b231ee10a64262a8ac7"
    version = "1.0"
    license = "MIT"
    author = ""
    url = "https://github.com/eliemichel/sdl3webgpu"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = ["CMakeLists.txt"]
    package_type = "static-library"

    def requirements(self):
        self.requires("sdl/3.4.14", transitive_headers=True)
        self.requires("dawn/20261023.194543", transitive_headers=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(
            f"git clone {self.url} && cd {self.name} && git checkout {self.commit}"
        )
        # Upstream's Emscripten branch predates WGPUStringView in emdawnwebgpu's webgpu.h
        source = f"{self.source_folder}/{self.name}/sdl3webgpu.c"
        replace_in_file(self, source, 'fromCanvasHTMLSelector.selector = "canvas";',
                        'fromCanvasHTMLSelector.selector = (WGPUStringView){ "canvas", WGPU_STRLEN };')
        replace_in_file(self, source, "surfaceDescriptor.label = NULL;",
                        "surfaceDescriptor.label = (WGPUStringView){ NULL, WGPU_STRLEN };")

    def _configure_cmake(self):
        variables = {"SDL3WEBGPU_DIR": pathlib.PureWindowsPath(f"{self.build_folder}/{self.name}").as_posix()}
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
        self.cpp_info.libs = ["sdl3webgpu"]
        if self.settings.os == "Macos":
            self.cpp_info.frameworks = ["CoreVideo", "IOKit", "QuartzCore", "Cocoa"]
