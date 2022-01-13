import socket
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
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.lock = threading.Lock()

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

        # Used to show the effects of threading
        time.sleep(1)

        # Build the string outside the lock for 2 reasons:
        # 1. To save time under the lock.
        # 2. `print` seems to flush each string, so if we pass comma separated 
        #    pieces, each one gets flushed sequenctially which causes tests to 
        #    fail.
        output = '[' + str(datetime.datetime.fromtimestamp(
            seconds_since_epoch)) + '] user ' + str(user_id) + ": " + str(msg)
        with self.lock:
            # Make sure only 1 thread write to stdout at a time.
            print(output)


def run_server(address):
    with socket.socket() as server:
        # Release the server on quit
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(1000)  # Listen to up to 1000 connections

        while True:
            client, address = server.accept()  # Hang until a connection comes through
            handler = HandleClient(client)
            handler.start()


def main(argv):
    if len(argv) != 2:
        print(f'USAGE: {argv[0]} <address>')
        return 1
    try:
        addr = argv[1].split(':')
        run_server((addr[0], int(addr[1])))
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
