from xing.remote_client import Client
from getpass import getpass


def draw(ht):
    print("[%s] %s" % (ht["shcode"], ht["hotime"]))
    print("-------------- + ------- + --------------")
    print("   매도잔량    |   가격  |   매수잔량")
    print("-------------- + ------- + --------------")
    print("%12s | %7s |               " % (ht["offerrem10"], ht["offerho10"]))
    print("%12s | %7s |               " % (ht["offerrem9"], ht["offerho9"]))
    print("%12s | %7s |               " % (ht["offerrem8"], ht["offerho8"]))
    print("%12s | %7s |               " % (ht["offerrem7"], ht["offerho7"]))
    print("%12s | %7s |               " % (ht["offerrem6"], ht["offerho6"]))
    print("%12s | %7s |               " % (ht["offerrem5"], ht["offerho5"]))
    print("%12s | %7s |               " % (ht["offerrem4"], ht["offerho4"]))
    print("%12s | %7s |               " % (ht["offerrem3"], ht["offerho3"]))
    print("%12s | %7s |               " % (ht["offerrem2"], ht["offerho2"]))
    print("%12s | %7s |               " % (ht["offerrem1"], ht["offerho1"]))
    print("-------------- + ------- + --------------")
    print("               | %7s |%12s" % (ht["bidho1"], ht["bidrem1"]))
    print("               | %7s |%12s" % (ht["bidho2"], ht["bidrem2"]))
    print("               | %7s |%12s" % (ht["bidho3"], ht["bidrem3"]))
    print("               | %7s |%12s" % (ht["bidho4"], ht["bidrem4"]))
    print("               | %7s |%12s" % (ht["bidho5"], ht["bidrem5"]))
    print("               | %7s |%12s" % (ht["bidho6"], ht["bidrem6"]))
    print("               | %7s |%12s" % (ht["bidho7"], ht["bidrem7"]))
    print("               | %7s |%12s" % (ht["bidho8"], ht["bidrem8"]))
    print("               | %7s |%12s" % (ht["bidho9"], ht["bidrem9"]))
    print("               | %7s |%12s" % (ht["bidho10"], ht["bidrem10"]))
    print("-------------- + ------- + --------------")
    print("%14s | 총 잔량 |%14s " % (ht["offer"], ht["bid"]))

if __name__ == "__main__":
    xing = Client(addr='192.168.1.105', port=50666)
    print("Lap time: ", xing.ping())
    xing.login(id=input("Id: "), passwd=getpass())

    for _ in range(3):
        data = xing.query("주식현재가호가조회", shcode="122630")
        draw(data["OutBlock"])

    xing.logout()
