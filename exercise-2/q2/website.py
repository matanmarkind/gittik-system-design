import socket
import http.server
import functools
import re

# Shared state between Website which registers and Handler which is the actual
# server.
paths = {}  # {path : fn}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        fn = None
        for path, f in paths.items():
            if path.fullmatch(self.path):
                fn = f
                break
        else:
            self.send_response(404)
            self.end_headers()
            return
        
        status, body = f(*self.path.split('/')[2:])
        if status != 200:
            self.send_response(status)
            self.end_headers()
            return

        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(body.encode('utf8'))


class Website:
    def route(self, path):

        def gen_wrapper(f):
            paths[re.compile(path)] = f
            return f

        return gen_wrapper

    def run(self, address):
        http_server = http.server.HTTPServer(address, Handler)
        http_server.serve_forever()
