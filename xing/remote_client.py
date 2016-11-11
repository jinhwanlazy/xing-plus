import zmq
from umsgpack import packb as pack
from umsgpack import unpackb as unpack
from xing.logger import Logger
log = Logger(__name__)

class Client:
    def __init__(self, addr="127.0.0.1", port=50666):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        target = "tcp://%s:%s" % (addr, port)
        log.info("connect to " + target)
        self.socket.connect(target)

    def ping(self):
        time1 = time.time()
        self.socket.send(b"ping")
        self.socket.recv()
        time2 = time.time()
        return time2 - time1

    def login(self, **kwargs):
        assert all(key in kwargs for key in ("id", "passwd"))
        assert all(isinstance(val, str) for val in kwargs.values())
        self.socket.send(b"login", zmq.SNDMORE)
        self.socket.send(pack(kwargs))
        res = unpack(self.socket.recv())
        if not res:
            log.info("login falied")
        else:
            log.info("login ok")
        return res

    def logout(self):
        self.socket.send(b"logout")
        self.socket.recv()

    def query(self, tr, **kwargs):
        if not kwargs:
            kwargs = {}
        self.socket.send(b"query", zmq.SNDMORE)
        self.socket.send(pack([tr, kwargs]))
        res = self.socket.recv()
        msg = unpack(self.socket.recv())
        if res == b"ok":
            return msg
        else:
            return None
