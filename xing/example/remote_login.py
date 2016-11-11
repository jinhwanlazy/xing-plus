from xing.remote import Client
from getpass import getpass

if __name__ == "__main__":
    xing = Client(addr='127.0.0.1', port=50666)
    print("Lap time: ", xing.ping())
    xing.login(id=input("Id: "), passwd=getpass())
    print(xing.query("서버시간조회"))
