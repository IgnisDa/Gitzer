import argparse
import http.server
import multiprocessing
import os
import pathlib
import socketserver
import subprocess
import sys
import webbrowser

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
GITZER_HOME = pathlib.Path(HOME) / ".local" / "ignisda-apps"
GITZER_PATH = pathlib.Path(GITZER_HOME) / "gitzer"
GITZER_RELEASES_API = "https://api.github.com/repos/IgnisDa/Gitzer/releases/latest"
LAST_UPDATED_FILENAME = "LAST_UPDATED"
VERSION_FILE = "VERSION"
GITZER_BACKEND_HOST = os.environ.get("GITZER_BACKEND_HOST", "127.0.0.1")
GITZER_FRONTEND_HOST = os.environ.get("GITZER_FRONTEND_HOST", "")
UPDATER_URL = "https://raw.githubusercontent.com/IgnisDa/Gitzer/main/get-gitzer.py"


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
        "bind": "%s:%s" % (GITZER_BACKEND_HOST, port),
        "workers": 1,
        "capture_output": True,
        "accesslog": str(GITZER_PATH / "gunicorn.log"),
        "errorlog": str(GITZER_PATH / "gunicorn.error.log"),
    }
    StandaloneApplication(application, options).run()


def frontend(port):
    client_address = ("127.0.0.1:", str(port))
    gitzer_url = "http://" + "".join(client_address) + "/"
    with TCPServer((GITZER_FRONTEND_HOST, port), Handler) as httpd:
        print("Access Gitzer at:", gitzer_url)
        if os.environ.get("GITZER_DONT_START_BROWSER") != "1":
            webbrowser.open("http://127.0.0.1:8533/")
        httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Start the Gitzer servers")
    parser.add_argument("-u", "--update", dest="update", action="store_true")
    args = parser.parse_args()
    if args.update:
        try:
            python = "python3" if sys.version_info.major == 3 else "python"
            subprocess.check_call(
                [
                    "curl",
                    "-sSL",
                    "https://raw.githubusercontent.com/IgnisDa/Gitzer/main/get-gitzer.py",  # noqa: E501
                    "-o",
                    "/tmp/get-gitzer.py",
                ]
            )
            subprocess.check_call([python, "/tmp/get-gitzer.py"])
        except Exception:
            raise RuntimeError(
                "We encountered some error. "
                "Please update manually from https://github.com/IgnisDa/Gitzer"
            )

    else:
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
