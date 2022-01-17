from functools import partial
from datetime import datetime
from pydoc import cli
import socket
import pathlib
import threading
import time
import http.server
import struct
from cli import CommandLineInterface
from website import Website

cli = CommandLineInterface()
website = Website()

data_dir = pathlib.Path('')

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

@website.route('/')
def index():
    return 200, generate_index_html(data_dir)

@website.route('/users/([0-9]+)')
def user(user_id):
    return 200, generate_thoughts_html(data_dir, user_id)

@cli.command
def run(address, data):
    # Convert inputs from strings.
    global data_dir
    data_dir = pathlib.Path(data)
    address = address.split(':')
    website.run((address[0], int(address[1])))

if __name__ == '__main__':
    cli.main()