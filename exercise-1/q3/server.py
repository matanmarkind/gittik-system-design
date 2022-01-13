import socket
import pathlib
import threading
import time
import datetime
import struct

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


def run_server(address, data_dir):
    with socket.socket() as server:
        # Release the server on quit
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(1000)  # Listen to up to 1000 connections

        while True:
            client, address = server.accept()  # Hang until a connection comes through
            handler = HandleClient(client, data_dir)
            handler.start()


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        addr = argv[1].split(':')
        data_dir = pathlib.Path(argv[2])
        run_server((addr[0], int(addr[1])), data_dir)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
