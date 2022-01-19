import socket, sys

class Connection:
    def __init__(self, connection):
        # `connection` is an open state, after `accept`  for a server, and after
        # `connect` for a client.
        self.connection = connection

    def __repr__(self):
        src = self.connection.getsockname()
        dst = self.connection.getpeername()
        return f'<Connection from {src} to {dst}>'

    def send(self, data):
        self.connection.sendall(data)

    def receive(self, size):
        chunks = []
        while size > 0:
            chunk = self.connection.recv(size)
            if not chunk:
                raise RuntimeError('incomplete data')
            chunks.append(chunk)
            size -= len(chunk)
        return b''.join(chunks)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    MESSAGE = b'Hello, world!'
    ADDRESS = ('127.0.0.1', 8000)
    if sys.argv[1] == 'server':
        with socket.socket() as server:
            # Release the server on quit
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(ADDRESS)
            server.listen(1000)  # Listen to up to 1000 connections
            client, _ = server.accept()  # Hang until a connection comes through

            connection = Connection(client)
            print(connection)
            data = connection.receive(len(MESSAGE))
            assert data == MESSAGE
            print(data)

            connection.close()

    elif sys.argv[1] == 'client':
        with socket.socket() as client:
            client.connect(ADDRESS)
            connection = Connection(client)
            print(connection)
            connection.send(MESSAGE)
            connection.close()