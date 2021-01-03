import socket
import random

from mario_pb2 import MarioMessage, Init, Action, State

TO_MSGLEN = 3
FROM_MSGLEN = 4


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

    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self, length):
        chunks = []
        bytes_recd = 0
        while bytes_recd < length:
            chunk = self.sock.recv(min(length - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


if __name__ == "__main__":
    state = MarioMessage()
    state.type = MarioMessage.Type.STATE
    state.state.state = 42
    state_data = state.SerializeToString()

    init_message = MarioMessage()
    init_message.type = MarioMessage.Type.INIT
    init_message.init.difficulty = 2
    init_message.init.seed = 1000
    init_message.init.r_field_w = 11
    init_message.init.r_field_h = 5
    init_message.init.level_length = 80
    init_s = init_message.SerializeToString()
    # init_m = MarioMessage()
    # init_m.ParseFromString(init_s)

    s = MySocket()
    s.connect("localhost", 8080)
    s.mysend(init_s)

    data = s.myreceive(len(state_data)+1)

    for i in range(100):
        action_message = MarioMessage()
        action_message.type = MarioMessage.Type.ACTION
        action_message.action.up = random.random() > 0.5
        action_message.action.right = random.random() > 0.5
        action_message.action.down = random.random() > 0.5
        action_message.action.left = random.random() > 0.5
        action_message.action.speed = random.random() > 0.5
        action_message.action.jump = random.random() > 0.5
        action_s = action_message.SerializeToString()
        s.mysend(action_s)
        data = s.myreceive(len(state_data)+1)

    s.disconnect()
    pass
