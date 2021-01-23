import argparse
import http.server
import multiprocessing
import os
import pathlib
import socketserver
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
GITZER_PATH = pathlib.Path(HOME) / ".gitzer"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=GITZER_PATH, **kwargs)


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
    argparse.ArgumentParser(description="Start the Gitzer servers")
    # args = parser.parse_args()
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
