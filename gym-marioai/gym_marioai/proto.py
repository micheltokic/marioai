import socket

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

from .mario_pb2 import MarioMessage, Init, Action, State


class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg:MarioMessage, delim=False):
        """
        send protobuf message with optional message length header.

        - netty server only accepts messages without header.
        - plain java server expects the length header
        """
        if delim:
            size = msg.ByteSize()
            self.sock.send(_VarintBytes(size))
        serialized = msg.SerializeToString()
        self.sock.send(serialized)

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
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


if __name__ == "__main__":
    """ for testing 
    to run code here, remove the prepended . from .mario_pb2 import
    """
    state = MarioMessage()
    state.type = MarioMessage.Type.STATE
    state.state.state = 42
    state_data = state.SerializeToString()

    print(bytearray(state_data))
    for b in bytearray(state_data):
        print(b, end=' ')
    print()
    
    s2 = MarioMessage()
    s2.ParseFromString(state_data)

    print('recovered:\n', s2)


    # init_message = MarioMessage()
    # init_message.type = MarioMessage.Type.INIT
    # init_message.init.difficulty = 2
    # init_message.init.seed = 1000
    # init_message.init.r_field_w = 11
    # init_message.init.r_field_h = 5
    # init_message.init.level_length = 80
    # init_s = init_message.SerializeToString()
    # # init_m = MarioMessage()
    # # init_m.ParseFromString(init_s)

    # s = MySocket()
    # s.connect("localhost", 8080)
    # s.mysend(init_s)

    # data = s.myreceive(len(state_data)+1)

    # for i in range(100):
    #     action_message = MarioMessage()
    #     action_message.type = MarioMessage.Type.ACTION
    #     action_message.action.up = random.random() > 0.5
    #     action_message.action.right = random.random() > 0.5
    #     action_message.action.down = random.random() > 0.5
    #     action_message.action.left = random.random() > 0.5
    #     action_message.action.speed = random.random() > 0.5
    #     action_message.action.jump = random.random() > 0.5
    #     action_s = action_message.SerializeToString()
    #     s.mysend(action_s)
    #     data = s.myreceive(len(state_data)+1)

    # s.disconnect()
    # pass
