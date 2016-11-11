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

    def start(self, port=50666):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:" + str(port))
        self.session = Session()
        self.done = False
        while not self.done:
            try:
                self.loop()
            except Exception as e:
                log.critical("There exist unhandled exception!", e.args)
        self.clean()

    def loop(self):
        topic = self.socket.recv()
        if topic == b"ping":
            self.socket.send(b"Hello, World!")
        if topic == b"login":
            args = unpack(self.socket.recv())
            res = self.login(**args)
            self.socket.send(pack(res))
        if topic == b"logout":
            self.logout()
            self.socket.send(b"ok")
        if topic == b"shutdown":
            self.done = True
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
        self.logout()
        self.socket.close()
        self.context.destroy()

    def login(self, **kwargs):
        self.session = Session()
        self.session.login(**kwargs)
        return True

    def logout(self):
        self.session.logout()
        self.session = None
