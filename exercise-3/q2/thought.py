import struct
from datetime import date, datetime

class Thought:
    # https://docs.python.org/3/library/struct.html#format-characters
    # Semantic meaning: user_id, time, msg_len
    # Must match the client.
    HEADER_FORMAT = '<LLI'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id  # int
        self.timestamp = timestamp  # datetime
        self.thought = thought  # str

    def __eq__(self, other):
        return (type(other) == Thought and
            self.user_id == other.user_id and
            self.timestamp == other.timestamp and
            self.thought == other.thought)

    def __str__(self):
        return f'[{self.timestamp}] user {self.user_id}: {self.thought}'

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'

    def serialize(self):
        seconds_since_epoch = int(datetime.timestamp(self.timestamp))
        header = struct.pack(
            Thought.HEADER_FORMAT,
            self.user_id,
            seconds_since_epoch,
            len(self.thought))
        return header + self.thought.encode('utf8')
    
    def deserialize(msg):
        user_id, seconds_since_epoch, thought_len = struct.unpack(
            Thought.HEADER_FORMAT, msg[0:Thought.HEADER_SIZE])
        thought = msg[Thought.HEADER_SIZE:].decode('utf8')
        return Thought(
            user_id,
            datetime.fromtimestamp(seconds_since_epoch),
            thought)

        

# thought1 = Thought(1, datetime(2000, 1, 1, 12, 0), "I'm hungry")
# print(thought1)
# print(repr(thought1))
# print(thought1.serialize())
# thought2 = Thought.deserialize(thought1.serialize())
# print(thought2)
# print(thought1 == thought2)
# print(thought1 != thought2)