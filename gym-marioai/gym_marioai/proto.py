import socket
import random
import struct

from .mario_pb2 import MarioMessage, Init, Action, State

# TO_MSGLEN = 3
# FROM_MSGLEN = 4


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

    # def mysend(self, msg):
    #     totalsent = 0
    #     while totalsent < len(msg):
    #         sent = self.sock.send(msg[totalsent:])
    #         if sent == 0:
    #             raise RuntimeError("socket connection broken")
    #         totalsent = totalsent + sent

    # def myreceive(self, length):
    #     chunks = []
    #     bytes_recd = 0
    #     while bytes_recd < length:
    #         chunk = self.sock.recv(min(length - bytes_recd, 2048))
    #         if chunk == b'':
    #             raise RuntimeError("socket connection broken")
    #         chunks.append(chunk)
    #         bytes_recd = bytes_recd + len(chunk)
    #     return b''.join(chunks)

    def send_proto(self, msg:MarioMessage):
        serialized = msg.SerializeToString()
        self.sock.send(serialized)

    def receive_proto(self):

        # read the size
        size = self.sock.recv(1)
        if size is None or size == b'':
            raise RuntimeError("socket connection broken")

        size = bytearray(size)[0]
        print('size:', size)

        # read the message
        msg = self.sock.recv(size)

        if msg is None or msg == b'':
            raise RuntimeError("socket connection broken")
        # print('msg:', msg)
        # print(bytearray(msg))
        # for b in bytearray(msg):
        #     print(b, end=' ')
        # print()
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
