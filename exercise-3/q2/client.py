import socket
import struct
import time
from cli import CommandLineInterface
from connection import Connection
from listener import Listener

cli = CommandLineInterface()

# https://docs.python.org/3/library/struct.html#format-characters
# Semantic meaning: user_id, time, msg_len
# Must match the server.
_HEADER_FORMAT = '<LLI'


@cli.command
def upload(address, user, thought):
    # Convert inputs from strings.
    address = address.split(':')
    user = int(user)

    with socket.socket() as client:
        client.connect((address[0], int(address[1])))
        connection = Connection(client)

        # Serialize the data into the expected format.
        header = struct.pack(_HEADER_FORMAT, user,
                             int(time.time()), len(thought))
        connection.send(header + thought.encode('utf8'))


if __name__ == '__main__':
    cli.main()