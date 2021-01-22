import argparse
import multiprocessing
import pathlib
import sys

sys.path.insert(
    0,
    str(
        pathlib.Path(__file__).parent / "_vendor" / "lib" / "python3.8" / "site-packages"
    ),
)
import gunicorn.app.base  # noqa: E402
from gitzer.wsgi import application  # noqa: E402


def _half_cpu_count():
    return int(multiprocessing.cpu_count() / 2)


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
        "workers": _half_cpu_count(),
        "capture_output": True,
        "accesslog": "gunicorn.log",
        "errorlog": "gunicorn.error.log",
    }
    StandaloneApplication(application, options).run()


def frontend(port):
    import http.server
    import socketserver

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Start the Gitzer servers")
    parser.add_argument(
        "--backend-port",
        dest="backend_port",
        type=int,
        help="the port on which the backend server will run",
        default=8534,
    )
    parser.add_argument(
        "--frontend-port",
        dest="frontend_port",
        type=int,
        help="the port on which the frontend server will run",
        default=8533,
    )
    args = parser.parse_args()
    backend_port = args.backend_port
    frontend_port = args.frontend_port
    p1 = multiprocessing.Process(target=backend, args=(backend_port,))
    p2 = multiprocessing.Process(target=frontend, args=(frontend_port,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    main()
