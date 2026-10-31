import argparse
import glob
import json
import os
import platform
import shutil
import subprocess
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


def all_requires(recipes):
    requires = []
    for recipe in recipes:
        out = subprocess.check_output(["conan", "inspect", recipe, "--format=json"], text=True)
        info = json.loads(out)
        requires.append(f"--requires={info['name']}/{info['version']}")
    return " ".join(requires)


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
        run(f"conan export {recipe}")

    # A bare --requires install has no conanfile generate(), so request the generators explicitly
    target = package if package is not None else f"{all_requires(recipes)} -g CMakeToolchain -g CMakeDeps"

    for compiler in compilers:
        toolchain_flags = ""
        profile_flags = f"--profile:all={os.getcwd()}/profiles/{compiler} "
        if compiler == "emscripten":
            # Native build profile so Conan knows it is cross-building (and lets find_package see its deps)
            profile_flags = (
                f"--profile:host={os.getcwd()}/profiles/emscripten "
                f"--profile:build={os.getcwd()}/profiles/gcc "
            )
            toolchain_flags = (
                f""" -c tools.cmake.cmaketoolchain:user_toolchain="['{find_emscripten_cmake()}']\""""
                f""" -c tools.cmake.cmaketoolchain:extra_variables="{{'CMAKE_CROSSCOMPILING_EMULATOR': '{find_node()}'}}\""""
            )

        for build_type in build_types:
            jobs_flags = f" -c tools.build:jobs={jobs}" if jobs is not None else ""
            optimalizations_flags = ""
            if optimalizations is not None:
                if compiler != "msvc":
                    optimalizations_flags = f" -c tools.build:cxxflags+=-{optimalizations}"
                
            run(
                f"conan install {target} "
                f"--build=missing "
                f"--settings build_type={build_type} "
                f"--output-folder={deploy_directory}/{compiler}/{build_type.lower()} "
                f"--deployer=full_deploy "
                f"{profile_flags}"
                f"{jobs_flags}"
                f"{optimalizations_flags}"
                f"{toolchain_flags}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--main", help="Main package (if omitted, all packages are deployed)")
    compilers = ["msvc", "clang-cl"] if platform.system() == "Windows" else ["gcc", "clang", "emscripten"]
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
