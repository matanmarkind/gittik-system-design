import socket
import pathlib
import threading
import time
import datetime
import struct
from cli import CommandLineInterface

cli = CommandLineInterface()
# https://docs.python.org/3/library/struct.html#format-characters
# Semantic meaning: user_id, time, msg_len
# Must match the client.
_HEADER_FORMAT = '<LLI'
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)


# Hang on  `connection` until data of `size` bytes has arrived.
# Return the data.
def receive_all(connection, size):
    chunks = []
    while size > 0:
        chunk = connection.recv(size)
        if not chunk:
            raise RuntimeError('incomplete data')
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)


class HandleClient(threading.Thread):
    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.lock = threading.Lock()
        self.data_dir = data_dir

    def __del__(self):
        self.connection.close()

    # calling Thread.start triggers `run` to run in a separate
    # thread.
    def run(self):
        # Wait to receive the headers.
        headers = receive_all(self.connection, _HEADER_SIZE)

        # Parse the headers.
        user_id, seconds_since_epoch, msg_len = struct.unpack(
            _HEADER_FORMAT, headers)

        # Wait to receive the message.
        msg = receive_all(self.connection, msg_len).decode('utf8')

        output_dir = self.data_dir / str(user_id)
        timestamp = datetime.datetime.fromtimestamp(seconds_since_epoch)
        output_file = output_dir /  f'{timestamp:%Y-%m-%d_%H-%M-%S}.txt'
        with self.lock:
            output_dir.mkdir(parents=True, exist_ok=True)
            if output_file.exists():
                msg = '\n' + msg
            with output_file.open('a') as f:
                f.write(msg)


@cli.command
def run(address, data):
    # Convert inputs from strings.
    address = address.split(':')
    data = pathlib.Path(data)

    with socket.socket() as server:
        # Release the server on quit
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((address[0], int(address[1])))
        server.listen(1000)  # Listen to up to 1000 connections

        while True:
            client, _ = server.accept()  # Hang until a connection comes through
            handler = HandleClient(client, data)
            handler.start()

if __name__ == '__main__':
    cli.main()
