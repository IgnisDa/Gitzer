#!/usr/bin/env python3
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile


def expanduser(path):
    expanded = os.path.expanduser(path)
    if path.startswith("~/") and expanded.startswith("//"):
        expanded = expanded[1:]
    return expanded


HOME = pathlib.Path(expanduser("~/"))
GITZER_PATH = pathlib.Path(HOME) / ".gitzer"


class Installer:
    def uninstall(self):
        try:
            shutil.rmtree(GITZER_PATH)
            self.unset_git_alias()
        except FileNotFoundError:
            pass

    def gitzer_temp_directory(self):
        return tempfile.mkdtemp()

    def install(self):
        self.uninstall()
        with tarfile.open("gitzer.tar.gz", "r:gz") as tar_file:
            temporary_dir = pathlib.Path(self.gitzer_temp_directory())
            tar_file.extractall(temporary_dir)
            shutil.move(temporary_dir / "build", GITZER_PATH)
        self.set_git_alias()

    def unset_git_alias(self):
        command = "git config --global --unset-all alias.gitzer"
        subprocess.check_call(command.split())

    def set_git_alias(self):
        command = "git config --global --replace-all alias.gitzer ".split()
        script_path = os.path.join(GITZER_PATH, "simple-server.py")
        alias = f"!python {script_path}"
        command.append(alias)
        subprocess.check_call(command)


if __name__ == "__main__":
    installer = Installer()
    installer.install()
