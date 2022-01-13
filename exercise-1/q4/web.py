from functools import partial
from datetime import datetime
import socket
import pathlib
import threading
import time
import http.server
import struct


def generate_index_html(data_dir):
    _INDEX_HTML = '''
    <html>
        <title>Brain Computer Interface</title>
        <body>
            <ul>
                {users}
            </ul>
        </body>
    </html>
    '''
    _USER_LINE_HTML = '''
    <li><a href="/users/{user_id}">user {user_id}</a></li>
    '''
    users_html = []
    for user_dir in data_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    return _INDEX_HTML.format(users='\n'.join(users_html))


def generate_thoughts_html(data_dir, user_id):
    _THOUGHTS_HTML = '''
    <html>
        <head>
            <title> Brain Computer Interface: User {user_id} </title>
        </head>
        <body>
            <table>
                {thoughts}
            </table>
        </body>
    </html>
    '''
    _THOUGHT_LINE_HTML = '''
    <tr>
        <td>{timestamp}</td>
        <td>{message}</td>
    </tr>
    '''
    user_dir = data_dir / str(user_id)
    thoughts_html = []
    for thought_file in user_dir.iterdir():
        timestamp = datetime.strptime(
            thought_file.name[:-4], "%Y-%m-%d_%H-%M-%S")
        thoughts_html.append(_THOUGHT_LINE_HTML.format(
            timestamp=str(timestamp),
            message=thought_file.open().read()))
    return _THOUGHTS_HTML.format(
        user_id=str(user_id),
        thoughts='\n'.join(thoughts_html))


class Handler(http.server.BaseHTTPRequestHandler):
    def __init__(self, data_dir, *args, **kwrags):
        self.data_dir = data_dir
        super().__init__(*args, **kwrags)

    def do_GET(self):
        if self.path == '/':
            return self.index()
        elif self.path.startswith('/users/'):
            return self.users()

        self.send_response(404)
        self.end_headers()
        return

    def index(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        # HTML doesn't seem to require Content-length.
        self.end_headers()

        html = generate_index_html(self.data_dir).encode('utf8')
        self.wfile.write(html)

    def users(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        user_id = int(self.path.split('/')[2])
        html = generate_thoughts_html(self.data_dir, user_id).encode('utf8')
        self.wfile.write(html)


def run_webserver(address, data_dir):
    handler = partial(Handler, data_dir)
    http_server = http.server.HTTPServer(address, handler)
    http_server.serve_forever()


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        addr = argv[1].split(':')
        data_dir = pathlib.Path(argv[2])
        run_webserver((addr[0], int(addr[1])), data_dir)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
