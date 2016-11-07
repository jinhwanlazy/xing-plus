from xing.remote import Client
from getpass import getpass

if __name__ == "__main__":
    xing = Client()

    ping = xing.ping()
    print("Lap time: ", ping)

    xing.login(id=input("Id: "), passwd=getpass())
    print(xing.query("서버시간조회"))
    
