from xing.xasession import Session
from xing.query import Query
from getpass import getpass

userid = input("Id: ")
passwd = getpass()
session = Session()
session.login(id=userid, passwd=passwd)

print(session.account())
print(Query("서버시간조회").send())
print(Query("t0167").send())
print(session.heartbeat())
