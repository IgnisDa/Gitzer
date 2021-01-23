#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile
from contextlib import closing

try:
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import HTTPError, Request, urlopen


def colored_print(color, message):
    colors = dict(
        SUCCESS="\033[92m",
        INFO="\033[96m",
        WARNING="\033[93m",
        FAIL="\033[91m",
        END="\033[0m",
    )

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
GITZER_RELEASES_API = "https://api.github.com/repos/IgnisDa/Gitzer/releases/latest"


class Installer:
    """ The installer class that installs Gitzer on the machine """

    def get_download_url(self):
        request = Request(GITZER_RELEASES_API, headers={"User-Agent": "Gitzer"})

        with closing(urlopen(request)) as response:
            data = json.loads(response.read())
        tag_name = data["tag_name"].lstrip("v")
        gzip_name = "gitzer-{}.tar.gz".format(tag_name)
        assets = data["assets"]
        for asset in assets:
            if asset["name"] == gzip_name:
                return asset["browser_download_url"], gzip_name

    def download_release(self):
        gzip_url, gzip_name = self.get_download_url()
        try:
            r = urlopen(gzip_url)
        except HTTPError as e:
            if e.code == 404:
                raise RuntimeError("Could not find {} file".format(gzip_name))

        meta = r.info()
        size = int(meta["Content-Length"])
        colored_print(
            "INFO",
            "  - Downloading {} ({:.2f}MB)".format(gzip_name, size / 1024 / 1024),
        )

        with self.gitzer_temp_directory() as dir_:
            tar = os.path.join(dir_, gzip_name)
            with open(tar, "wb") as f:
                block_size = 8192
                current = 0
                while True:
                    buffer = r.read(block_size)
                    if not buffer:
                        break
                    current += len(buffer)
                    f.write(buffer)
            return tar

    def install(self):
        colored_print("INFO", "Installing Gitzer...")
        self.uninstall()
        gitzer_tar = self.download_release()
        with tarfile.open(gitzer_tar, "r:gz") as tar_file:
            temporary_dir = self.gitzer_temp_directory()
            tar_file.extractall(temporary_dir)
            shutil.move(temporary_dir / "build", GITZER_PATH)
        self.set_git_alias()
        colored_print("SUCCESS", "Gitzer was installed on your system successfully!")

    def gitzer_temp_directory(self):
        return pathlib.Path(tempfile.mkdtemp())

    def set_git_alias(self):
        colored_print("INFO", "Adding associated git alias...")
        command = "git config --global --replace-all alias.gitzer ".split()
        script_path = os.path.join(GITZER_PATH, "simple-server.py")
        alias = f"!python {script_path}"
        command.append(alias)
        subprocess.check_call(command)

    def uninstall(self):
        colored_print(
            "WARNING", "Removing Gitzer directories from your system (if found)..."
        )
        try:
            shutil.rmtree(GITZER_PATH)
            self.unset_git_alias()
        except FileNotFoundError:
            pass

    def unset_git_alias(self):
        colored_print("WARNING", "Removing associated git alias...")
        command = "git config --global --unset-all alias.gitzer"
        subprocess.check_call(command.split())


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
