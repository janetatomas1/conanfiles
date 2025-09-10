
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import shutil
import glob
import os
import pathlib

class AbstractPackage(ConanFile):
    name = "bgfx"
    version = "1.0.0"
    license = "Proprietary"
    url = "https://github.com/bkaradzic/bgfx.git"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone https://github.com/bkaradzic/bx.git && cd bx && git checkout eda38395ddfdeba08c46653b93b8d5bb21f2c863")
        self.run("git clone https://github.com/bkaradzic/bimg.git && cd bimg && git checkout a1a2ae3c129d8c33e765eecd91801bffd985c317")
        self.run("git clone https://github.com/bkaradzic/bgfx.git && cd bgfx && git checkout 53293f07a8eaa763fd6b87f5b06b46db67a3f59a")


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