from connection import Connection
import socket, sys


class Listener:
    def __init__(
        self, port=1000, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.server = socket.create_server(
            address=(host, port),
            backlog=backlog,
            reuse_port=reuseaddr)

    def __repr__(self):
        host, port = self.server.getsockname()
        backlog = self.backlog
        reuseaddr = self.reuseaddr
        return f'{self.__class__.__name__}({port=}, {host=}, {backlog=}, {reuseaddr=})'
    
    def start(self):
        self.server.listen()
    def stop(self):
        self.server.close()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def accept(self):
        client, _ = self.server.accept()
        return Connection(client)

if __name__ == '__main__':
    MESSAGE = b'Hello, world!'
    HOST = '127.0.0.1'
    PORT = 8000
    if sys.argv[1] == 'server':
        with Listener(host=HOST, port=PORT) as listener:
            print(listener)

            connection = listener.accept()
            data = connection.receive(len(MESSAGE))
            assert data == MESSAGE
            print(data)

    elif sys.argv[1] == 'client':
        with Connection.connect(HOST, PORT) as connection:
            print(connection)
            connection.send(MESSAGE)