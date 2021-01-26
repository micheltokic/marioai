import socket

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

from .mario_pb2 import MarioMessage


def serialize(msg:MarioMessage):
    """
    adds VarintBytes: a message header indicating the length of 
                    the following message
    and serializes the message to a byte array
    """
    return _VarintBytes(msg.ByteSize()) + msg.SerializeToString()


def create_action_message(action:int):
    """ create and serialize an action message """
    msg = MarioMessage()
    msg.type = MarioMessage.Type.ACTION
    msg.action = action
    return serialize(msg)


def create_reset_message():
    """ create and serialize a reset message """
    msg = MarioMessage()
    msg.type = MarioMessage.Type.RESET
    return serialize(msg)


class ProtobufSocket:
    """
    A wrapper for a TCP socket which provides methods to send and receive 
    protobuf messages of our MarioMessage protobuf specification.
    """
    def __init__(self, n_actions:int):
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        # pre-parse and cache often used messages
        self.reset_msg = create_reset_message()
        self.action_messages = [create_action_message(i) for i in \
                                range(n_actions)]

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg:MarioMessage):
        self.sock.send(serialize(msg))

    def send_init(self, difficulty, seed:int, 
            rf_width:int, rf_height:int, level_length:int,
            level_path:str, render:bool):
        """ send an INIT message """

        msg = MarioMessage()
        msg.type = MarioMessage.Type.INIT
        msg.init.render = render 
        msg.init.difficulty = difficulty
        msg.init.seed = seed
        msg.init.r_field_w = rf_width
        msg.init.r_field_h = rf_height
        msg.init.level_length = level_length
        msg.init.file_name = level_path
        self.sock.send(serialize(msg))

    def send_reset(self):
        """ send a RESET message """
        self.sock.send(self.reset_msg)

    def send_action(self, action:int):
        """ send an ACTION message """
        self.sock.send(self.action_messages[action])

    def receive(self):
        """ receive, parse and return a protobuf message """
        # parse the header
        buf = self.sock.recv(10)
        if buf is None or buf == b'':
            raise RuntimeError("socket connection broken")

        total_len, offset = _DecodeVarint32(buf, 0)
        msg = buf[offset:]
        remaining_len = total_len - len(msg)

        while remaining_len > 0:
            chunk = self.sock.recv(remaining_len)
            if chunk is None or chunk == b'':
                raise RuntimeError("socket connection broken")
            msg += chunk
            remaining_len -= len(chunk)

        parsed_msg = MarioMessage()
        parsed_msg.ParseFromString(msg)
        return parsed_msg

    def disconnect(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except OSError:
            pass

    # def receive_daniel(self):
    #     """ daniels version """
    #     chunks = []
    #     bytes_recd = 0
    #     msg_len = 0
    #     length = []
    #     length_read = False

    #     while not length_read:
    #         chunk = self.sock.recv(1)
    #         if chunk == b'':
    #             raise RuntimeError("socket connection broken")
    #         length.append(chunk)
    #         try:
    #             ln = b''.join(length)
    #             msg_len, _ = _DecodeVarint32(ln, 0)
    #             length_read = True
    #         except:
    #             pass

    #     while bytes_recd < msg_len:
    #         chunk = self.sock.recv(msg_len)
    #         if chunk == b'':
    #             raise RuntimeError("socket connection broken")
    #         chunks.append(chunk)
    #         bytes_recd = bytes_recd + len(chunk)

    #     proto_msg = MarioMessage()
    #     proto_msg.ParseFromString(b''.join(chunks))
    #     return proto_msg


