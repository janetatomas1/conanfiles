import argparse
import glob
import os
import platform
import shutil
from pathlib import Path


def find_emscripten_cmake():
    emsdk_root = os.environ['EMSDK']

    return next(Path(emsdk_root).rglob("Emscripten.cmake"))


def find_node():
    return shutil.which("node")


def run(cmd):
    print(cmd)
    ret = os.system(cmd)
    if ret != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def main(
    package,
    compilers,
    deploy_directory,
    build_types,
    jobs,
    optimalizations
):
    recipes = glob.glob("*/conanfile.py")

    for recipe in recipes:
        run(f"conan export {recipe}/")

    for compiler in compilers:
        if compiler == "emscripten":
            build_vars = f'tools.build:vars=["-DCMAKE_TOOLCHAIN_FILE={find_emscripten_cmake()}", "-DCMAKE_CROSSCOMPILING_EMULATOR={find_node()}"]'

        for build_type in build_types:
            optimalizations_flags = ""
            if optimalizations is not None:
                if compiler != "msvc":
                    optimalizations_flags = f" -c tools.build:cxxflags+=-{optimalizations} -c tools.build:cxxflags+=-{optimalizations}"
                
            run(
                f"conan install {package} "
                f"--build=missing "
                f"--settings build_type={build_type} "
                f"--output-folder={deploy_directory}/{compiler}/{build_type.lower()} "
                f"--deployer=full_deploy "
                f"--profile:all={os.getcwd()}/profiles/{compiler} "
                f"-c tools.build:jobs={jobs}"
                f"{optimalizations_flags}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--main", help="Main package")
    compilers = ["msvc"] if platform.system() == "Windows" else ["gcc"]
    parser.add_argument(
        "--compilers", nargs="+", default=compilers, help="Compilers to use"
    )
    parser.add_argument(
        "--deploy-directory", default="third-party", help="Output directory"
    )
    parser.add_argument(
        "--build-types",
        nargs="+",
        default=["Release", "Debug"],
        help="Build types to build",
    )

    parser.add_argument("--optimalizations", default="O2", help="Level of compiler optimizations")

    parser.add_argument("--jobs", default=None, help="Number of parallel jobs")
    args = parser.parse_args()

    main(
        args.main,
        args.compilers,
        args.deploy_directory,
        args.build_types,
        args.jobs,
        args.optimalizations
    )
