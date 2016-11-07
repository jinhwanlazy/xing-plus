import zmq
import time
from umsgpack import packb as pack
from umsgpack import unpackb as unpack
from xing.xasession import Session
from xing.query import Query
from xing.logger import Logger
log = Logger(__name__)


class Server:
    MAX_RETRY = 5

    def __init__(self, port=50666):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:" + str(port))
        self.session = Session()
        self.done = False

    def start(self):
        self.done = False
        while not self.done:
            try:
                self.loop()
            except Exception as e:
                log.critical("There exist unhandled exception!")
                continue
        self.clean()

    def loop(self):
        topic = self.socket.recv()
        if topic == b"ping":
            self.socket.send(b"Hello, World!")
        if topic == b"login":
            args = unpack(self.socket.recv())
            res = self.login(**args)
            self.socket.send(pack(res))
        if topic == b"query":
            tr, args = unpack(self.socket.recv())
            try:
                res = Query(tr).send(**args)
                self.socket.send(b"ok", zmq.SNDMORE)
                self.socket.send(pack(res))
            except Exception as e:
                log.critical(e.args)
                self.socket.send(b"error", zmq.SNDMORE)
                self.socket.send(pack(e.args))
        else:
            pass

    def clean(self):
        pass

    def login(self, **kwargs):
        self.session = Session()
        self.session.login(**kwargs)
        return True


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
