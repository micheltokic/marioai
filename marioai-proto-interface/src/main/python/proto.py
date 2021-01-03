import socket

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
    init_message = MarioMessage()
    init_message.type = MarioMessage.Type.INIT
    init_message.init.difficulty = 15
    init_message.init.seed = 2
    init_message.init.r_field_w = 3
    init_message.init.r_field_h = 4
    init_message.init.level_length = 5
    init_s = init_message.SerializeToString()
    # init_m = MarioMessage()
    # init_m.ParseFromString(init_s)

    s = MySocket()
    s.connect("localhost", 8080)

    s.mysend(init_s)
    data = s.myreceive(len(init_s)+1)

    response = MarioMessage()
    response.ParseFromString(data[1:])
    print(str(response))
    s.disconnect()
    pass
