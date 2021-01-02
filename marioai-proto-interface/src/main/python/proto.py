import socket

from action_pb2 import Action

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
        while totalsent < TO_MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < FROM_MSGLEN:
            chunk = self.sock.recv(min(FROM_MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)


if __name__ == "__main__":
    s = MySocket()
    s.connect("localhost", 8080)
    action = Action()
    action.action_number = 1024
    serialized = action.SerializeToString()
    ln1 = len(serialized)
    s.mysend(serialized)
    data = s.myreceive()
    ln = len(data)
    received_action = Action()
    received_action.ParseFromString(data[1:])

    pass
