import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, save


class Dawn(ConanFile):
    name = "dawn"
    version = "20261023.194543"
    commit = "1716e88cc9e58398fab5d4473f7f2e858667b677"
    license = "BSD-3-Clause"
    author = ""
    url = "https://github.com/google/dawn"
    description = "Prebuilt Dawn (desktop) / emdawnwebgpu port (Emscripten), with webgpu.h and webgpu_cpp.h"
    settings = "os", "compiler", "build_type", "arch"
    package_type = "static-library"

    # Prebuilt release archives, keyed by (os, arch)
    _platforms = {
        ("Linux", "x86_64"): "ubuntu-latest",
        ("Windows", "x86_64"): "windows-latest",
        ("Macos", "armv8"): "macos-latest",
        ("Macos", "x86_64"): "macos-15-intel",
    }

    @property
    def _is_emscripten(self):
        return self.settings.os == "Emscripten"

    @property
    def _release_url(self):
        return f"{self.url}/releases/download/v{self.version}"

    def validate(self):
        if not self._is_emscripten and (str(self.settings.os), str(self.settings.arch)) not in self._platforms:
            raise ConanInvalidConfiguration(f"No prebuilt Dawn for {self.settings.os}/{self.settings.arch}")

    def package_id(self):
        # Prebuilt binaries: only MSVC cares about the build type (debug vs release CRT)
        if self.info.settings.compiler != "msvc":
            del self.info.settings.compiler
            del self.info.settings.build_type

    def build(self):
        if self._is_emscripten:
            get(self, f"{self._release_url}/emdawnwebgpu_pkg-v{self.version}.zip")
            return

        platform = self._platforms[(str(self.settings.os), str(self.settings.arch))]
        # Linux/macOS Release archives work for Debug too (and the Linux Debug one is ~850MB)
        build_type = "Debug" if self.settings.compiler == "msvc" and self.settings.build_type == "Debug" else "Release"
        get(self, f"{self._release_url}/Dawn-{self.commit}-{platform}-{build_type}.tar.gz", strip_root=True)

    def package(self):
        if self._is_emscripten:
            copy(self, "*", src=os.path.join(self.build_folder, "emdawnwebgpu_pkg"),
                 dst=os.path.join(self.package_folder, "emdawnwebgpu_pkg"))
            # --use-port must be passed on compile and link; a build module keeps the path relocatable
            save(self, os.path.join(self.package_folder, "cmake", "dawn-emdawnwebgpu.cmake"),
                 'set(_EMDAWNWEBGPU_PORT "${CMAKE_CURRENT_LIST_DIR}/../emdawnwebgpu_pkg/emdawnwebgpu.port.py")\n'
                 'target_compile_options(dawn::webgpu_dawn INTERFACE "--use-port=${_EMDAWNWEBGPU_PORT}")\n'
                 'target_link_options(dawn::webgpu_dawn INTERFACE "--use-port=${_EMDAWNWEBGPU_PORT}")\n')
            return

        copy(self, "LICENSE*", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "*", src=os.path.join(self.build_folder, "include"), dst=os.path.join(self.package_folder, "include"))
        for libdir in ["lib", "lib64"]:
            copy(self, "*webgpu_dawn.*", src=os.path.join(self.build_folder, libdir),
                 dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Dawn")
        self.cpp_info.set_property("cmake_target_name", "dawn::webgpu_dawn")

        if self._is_emscripten:
            # Same dirs the port adds; needed explicitly because clang-scan-deps (C++20 module scanning) ignores --use-port
            self.cpp_info.includedirs = [
                os.path.join("emdawnwebgpu_pkg", "webgpu", "include"),
                os.path.join("emdawnwebgpu_pkg", "webgpu_cpp", "include"),
            ]
            self.cpp_info.libdirs = []
            self.cpp_info.bindirs = []
            self.cpp_info.builddirs = ["cmake"]
            self.cpp_info.set_property("cmake_build_modules", [os.path.join("cmake", "dawn-emdawnwebgpu.cmake")])
            return

        self.cpp_info.libs = ["webgpu_dawn"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["dl", "rt", "pthread", "m"]
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs = ["user32", "onecore_apiset", "dxguid", "advapi32", "dbghelp"]
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks = ["CoreFoundation", "Foundation", "IOSurface", "QuartzCore", "Cocoa", "IOKit", "Metal"]
