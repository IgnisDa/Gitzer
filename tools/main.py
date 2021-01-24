import argparse
import datetime
import http.server
import json
import multiprocessing
import os
import pathlib
import shutil
import socketserver
import subprocess
import sys
import tarfile
import tempfile
import webbrowser
from contextlib import closing

try:
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import HTTPError, Request, urlopen


sys.path.insert(
    0,
    str(
        pathlib.Path(__file__).parent / "_vendor" / "lib" / "python3.8" / "site-packages"
    ),
)
import gunicorn.app.base  # noqa: E402
from gitzer.wsgi import application  # noqa: E402


def expanduser(path):
    expanded = os.path.expanduser(path)
    if path.startswith("~/") and expanded.startswith("//"):
        expanded = expanded[1:]
    return expanded


HOME = pathlib.Path(expanduser("~/"))
GITZER_PATH = pathlib.Path(HOME) / ".gitzer"
GITZER_RELEASES_API = "https://api.github.com/repos/IgnisDa/Gitzer/releases/latest"
LAST_UPDATED_FILENAME = "LAST_UPDATED"
VERSION_FILE = "VERSION"


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
            "  - Downloading {} ({:.2f} MB)".format(gzip_name, size / 1024 / 1024),
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
        script_path = os.path.join(GITZER_PATH, "main.py")
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


class Updater:
    """Automatically checks for updates every 10 days and prompts user to update
    if update is available."""

    def check_last_updated(self):
        if LAST_UPDATED_FILENAME not in os.listdir(GITZER_PATH):
            with open(GITZER_PATH / LAST_UPDATED_FILENAME, "w") as last_updated_file:
                last_updated_file.write(str(datetime.datetime.now()))
        else:
            with open(GITZER_PATH / LAST_UPDATED_FILENAME) as last_updated_file:
                last_updated = datetime.datetime.strptime(
                    last_updated_file.read(), "%Y-%m-%d %H:%M:%S.%f"
                )
                ten_days_ago = datetime.timedelta(days=10)
                if datetime.datetime.now() - last_updated > ten_days_ago:
                    return self.prompt_user()
                else:
                    return False

    def prompt_user(self):
        prompt = input("Would you like to check for an update [y/n]? ")
        if prompt.lower() in ["y", "yes"]:
            with open(GITZER_PATH / VERSION_FILE) as version_file:
                version = version_file.read().strip()
                request = Request(GITZER_RELEASES_API, headers={"User-Agent": "Gitzer"})

                with closing(urlopen(request)) as response:
                    data = json.loads(response.read())
                tag_name = data["tag_name"].lstrip("v")
                return version.replace(".", "") > tag_name.replace(".", "")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(GITZER_PATH), **kwargs)


class TCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def backend(port):
    options = {
        "bind": "%s:%s" % ("127.0.0.1", port),
        "workers": 1,
        "capture_output": True,
        "accesslog": str(GITZER_PATH / "gunicorn.log"),
        "errorlog": str(GITZER_PATH / "gunicorn.error.log"),
    }
    StandaloneApplication(application, options).run()


def frontend(port):
    client_address = ("127.0.0.1:", str(port))
    gitzer_url = "http://" + "".join(client_address) + "/"
    with TCPServer(("", port), Handler) as httpd:
        print("Access Gitzer at:", gitzer_url)
        webbrowser.open("http://127.0.0.1:8533/")
        httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Start the Gitzer servers")
    parser.add_argument("-n", "--no-browser", dest="no_browser", action="store_true")
    update = Updater()
    if update.check_last_updated():
        installer = Installer()
        installer.install()
    args = parser.parse_args()
    if args.no_browser:
        print("ok")
    backend_port = 8534
    frontend_port = 8533
    p1 = multiprocessing.Process(target=backend, args=(backend_port,))
    p2 = multiprocessing.Process(target=frontend, args=(frontend_port,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down servers")
