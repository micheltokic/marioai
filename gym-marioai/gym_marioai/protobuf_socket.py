import socket

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

from .mario_pb2 import MarioMessage, Init, Action, State


class ProtobufSocket:
    """
      
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg:MarioMessage, delim=True):
        """
        send protobuf message with optional message length header.

        - netty server only accepts messages without header.
        - plain java server expects the length header
        """
        if delim:
            size = msg.ByteSize()
            self.sock.send(_VarintBytes(size))
        self.sock.send(msg.SerializeToString())


    def receive(self):
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

    def receive_daniel(self):
        """ daniels version """
        chunks = []
        bytes_recd = 0
        msg_len = 0
        length = []
        length_read = False

        while not length_read:
            chunk = self.sock.recv(1)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            length.append(chunk)
            try:
                ln = b''.join(length)
                msg_len, _ = _DecodeVarint32(ln, 0)
                length_read = True
            except:
                pass

        while bytes_recd < msg_len:
            chunk = self.sock.recv(msg_len)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        proto_msg = MarioMessage()
        proto_msg.ParseFromString(b''.join(chunks))
        return proto_msg
