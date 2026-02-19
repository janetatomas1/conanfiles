import argparse
import glob
import os
import platform
import shutil


def run(cmd):
    print(cmd)
    ret = os.system(cmd)
    if ret != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def main(package, compilers, deploy_directory, build_types):
    recipes = glob.glob("*/conanfile.py")

    for recipe in recipes:
        run(f"conan export {recipe}/")

    for compiler in compilers:
        for build_type in build_types:
            run(
                f"conan install {package} "
                f"--build=missing "
                f"--settings build_type={build_type} "
                f"--output-folder={deploy_directory}/{compiler}/{build_type.lower()} "
                f"--deployer=full_deploy "
                f"--profile:all={os.getcwd()}/profiles/{compiler}"
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
    args = parser.parse_args()

    main(args.main, args.compilers, args.deploy_directory, args.build_types)
