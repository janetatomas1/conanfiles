
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import shutil
import glob
import os
import pathlib

class AbstractPackage(ConanFile):
    name = "bgfx"
    version = "0.0"
    license = "Proprietary"
    url = "https://github.com/bkaradzic/bgfx.git"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone https://github.com/bkaradzic/bx.git")
        self.run("git clone https://github.com/bkaradzic/bimg.git")
        self.run("git clone https://github.com/bkaradzic/bgfx.git")


    def build(self):
        self.run(f"make PREFIX=${self.package_folder}", cwd=f"{self.build_folder}/bgfx")
        self.run(f"make PREFIX=${self.package_folder} linux-gcc-release64 -j16", cwd=f"{self.build_folder}/bgfx")

    def package(self):
        os.mkdir(f'{self.package_folder}/lib')
        os.mkdir(f'{self.package_folder}/include')

        libs = glob.glob(f"{self.build_folder}/bgfx/.build/linux64_gcc/bin/lib*")

        for l in libs:
            shutil.copy(l, f'{self.package_folder}/lib/{pathlib.Path(l.replace('Release', '')).name}')
        
        shutil.copytree(
            f'{self.build_folder}/bgfx/include/bgfx',
            f'{self.package_folder}/include/bgfx'
        )
        shutil.copytree(
            f'{self.build_folder}/bimg/include/bimg',
            f'{self.package_folder}/include/bimg'
        )
        shutil.copytree(
            f'{self.build_folder}/bx/include/bx',
            f'{self.package_folder}/include/bx'
        )