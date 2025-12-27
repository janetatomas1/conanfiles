
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import replace_in_file


class Magnum(ConanFile):
    name = "magnum"
    version = "1.0.0"
    license = "MIT"
    author = "Tomas Janeta tomas.janeta@proton.me>"
    url = "https://github.com/mosra/magnum/"
    corrade_url = "https://github.com/mosra/corrade/"
    magnum_commit = "bd52eb9be27f647cbec5475a920b79ce61953c8b"
    corrade_commit = "b65bcc0d08c8ef4b47a19ac37cdffb267e7c9994"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = [
        "CMakeLists.txt",
        "main.cpp"
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        self.run(f"git clone {self.url}")
        self.run(f"git checkout {self.magnum_commit}", cwd=f"{self.source_folder}/magnum")

        self.run(f"git clone {self.corrade_url}")
        self.run(f"git checkout {self.corrade_commit}", cwd=f"{self.source_folder}/corrade")


    def build(self):
        cmake = CMake(self)
        cmake.configure({
            "CMAKE_INSTALL_PREFIX": self.package_folder,
            "MAGNUM_WITH_GL": "ON"
        })
        
        self.run("cmake --build .", cwd=f"{self.build_folder}/corrade")
        self.run("cmake --build .", cwd=f"{self.build_folder}/magnum")

    def package(self):
        self.run("cmake --install .", cwd=f"{self.build_folder}/corrade")
        self.run("cmake --install .", cwd=f"{self.build_folder}/magnum")
