import socket
import struct
import time

# https://docs.python.org/3/library/struct.html#format-characters
# Semantic meaning: user_id, time, msg_len
# Must match the server.
_HEADER_FORMAT = '<LLI'


def upload_thought(address, user_id, thought):
    with socket.socket() as connection:
        connection.connect(address)

        # Serialize the data into the expected format.
        header = struct.pack(_HEADER_FORMAT, user_id,
                             int(time.time()), len(thought))
        connection.sendall(header + thought.encode('utf8'))


def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        addr = argv[1].split(':')
        upload_thought((addr[0], int(addr[1])), int(argv[2]), argv[3])
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
