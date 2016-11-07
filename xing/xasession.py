import win32com.client
import time
import pythoncom
from xyng import xacom
from xyng.logger import Logger
from xyng.query import Requester
log = Logger(__name__)


class _XASessionEvents:
    def __init__(self):
        self.code = -1
        self.msg = None

    def reset(self):
        self.code = -1
        self.msg = None

    def OnLogin(self, code, msg):
        self.code = str(code)
        self.msg = str(msg)

    def OnLogout(self):
        print("OnLogout method is called")

    def OnDisconnect(self):
        print("OnDisconnect method is called")


class Session:
    def __init__(self):
        self.session = win32com.client.DispatchWithEvents(
            "XA_Session.XASession", _XASessionEvents)

    def login_demo(self, **kwargs):
        self.session.reset()
        self.session.ConnectServer('demo.ebestsec.co.kr', 20001)
        self.session.Login(kwargs["id"], kwargs["passwd"], "", 0, 0)
        self.account_pass = "0000"

    def login_real(self, **kwargs):
        self.session.reset()
        self.session.ConnectServer('hts.ebestsec.co.kr', 20001)
        self.session.Login(kwargs["id"], kwargs["passwd"],
                           kwargs["certification_passwd"], 0, 0)
        self.account_pass = kwargs['account_pass']

    def login(self, **kwargs):
        if "certification_passwd" not in kwargs or "account_pass" not in kwargs:
            log.info("certification_passwd or account_pass are not given."
                     "Trying demo server...")
            self.login_demo(**kwargs)
        else:
            self.login_real(**kwargs)

        while self.session.code == -1:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)

        if self.session.code == "0000":
            log.info("로그인 성공")
            return True
        else:
            log.critical(
                "로그인 실패 : %s" % xacom.parseErrorCode(self.session.code))
            return False

    def logout(self):
        """서버와의 연결을 끊는다.

            ::

                session.logout()
        """
        self.session.DisconnectServer()

    def account(self):
        """계좌 정보를 반환한다.

            :return: 계좌 정보를 반환한다.
            :rtype: object {no: "계좌번호",
                            name:"계좌이름",
                            detailName:"계좌상세이름"}

            ::

                session.account()
        """
        acc = []
        for p in range(self.session.GetAccountListCount()):
            acc.append({
                "no": self.session.GetAccountList(p),
                "name": self.session.GetAccountName(p),
                "detailName": self.session.GetAcctDetailName(p)
            })
        return acc

    def heartbeat(self):
        """서버에 시간을 조회해서 서버 연결여부를 확인한다.

        :return: 연결될 경우, time과 dt를 포함한 dictionary를 반환한다.
                 연결이 끊어졌을 경우, None을 반환한다
        :rtype: None, object

            - 서버와의 연결이 끊어졌으면 None
            - 서버와의 연결이 유효하면 { time:"mmhhss", dt:"yyyymmdd"}

        ::

            session.heartbeat()
        """
        result = Requester("서버시간조회").send(id="")
        print(result)
