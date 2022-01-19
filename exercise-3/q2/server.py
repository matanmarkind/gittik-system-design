import socket
import pathlib
import threading
import time
import datetime
import struct
from cli import CommandLineInterface
from connection import Connection
from listener import Listener

cli = CommandLineInterface()
# https://docs.python.org/3/library/struct.html#format-characters
# Semantic meaning: user_id, time, msg_len
# Must match the client.
_HEADER_FORMAT = '<LLI'
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)


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
        headers = self.connection.receive(_HEADER_SIZE)

        # Parse the headers.
        user_id, seconds_since_epoch, msg_len = struct.unpack(
            _HEADER_FORMAT, headers)

        # Wait to receive the message.
        msg = self.connection.receive(msg_len).decode('utf8')

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

    listener = Listener(host=address[0], port=int(address[1]))
    with listener:
        while True:
            # Wait for a connection synchronously, then handle it in another
            # thread.
            HandleClient(listener.accept(), data).start()

if __name__ == '__main__':
    cli.main()
