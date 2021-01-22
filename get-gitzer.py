#!/usr/bin/env python3
import argparse
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile


def colored_print(color, message):
    colors = dict(SUCCESS="\033[92m", WARNING="\033[93m", FAIL="\033[91m", END="\033[0m")

    if color not in colors:
        raise ValueError(f"The color should be among {list(colors.keys())}")
    print(colors[color] + message + colors["END"])


def expanduser(path):
    expanded = os.path.expanduser(path)
    if path.startswith("~/") and expanded.startswith("//"):
        expanded = expanded[1:]
    return expanded


HOME = pathlib.Path(expanduser("~/"))
GITZER_PATH = pathlib.Path(HOME) / ".gitzer"


class Installer:
    def uninstall(self):
        colored_print(
            "WARNING", "Removing Gitzer directories from your system (if found)..."
        )
        try:
            shutil.rmtree(GITZER_PATH)
            self.unset_git_alias()
        except FileNotFoundError:
            pass

    def gitzer_temp_directory(self):
        return pathlib.Path(tempfile.mkdtemp())

    def install(self):
        colored_print("SUCCESS", "Installing Gitzer...")
        self.uninstall()
        with tarfile.open("gitzer.tar.gz", "r:gz") as tar_file:
            temporary_dir = self.gitzer_temp_directory()
            tar_file.extractall(temporary_dir)
            shutil.move(temporary_dir / "build", GITZER_PATH)
        self.set_git_alias()

    def unset_git_alias(self):
        colored_print("WARNING", "Removing associated git alias...")
        command = "git config --global --unset-all alias.gitzer"
        subprocess.check_call(command.split())

    def set_git_alias(self):
        colored_print("WARNING", "Adding associated git alias...")
        command = "git config --global --replace-all alias.gitzer ".split()
        script_path = os.path.join(GITZER_PATH, "simple-server.py")
        alias = f"!python {script_path}"
        command.append(alias)
        subprocess.check_call(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The installer for the Gitzer tool")
    parser.add_argument(
        "-u",
        "--uninstall",
        dest="uninstall",
        action="store_true",
        help="run get-gitzer.py with this flag to uninstall it from your system",
    )
    args = parser.parse_args()
    uninstall = args.uninstall
    installer = Installer()
    if uninstall:
        installer.uninstall()
    else:
        installer.install()
