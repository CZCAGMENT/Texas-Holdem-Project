# poker_frame.py

from multiprocessing import Process
from socket import *
# import sys
# import signal
import pymysql
from poker_desk import *
from port import *
import signal


def main():
    db = pymysql.connect('localhost', 'root', '123456', 'Texaspokes')
    for num in range(10):
        p = Process(target=desk, args=(num, db))
        p.start()


def desk(num, db):
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    port = d_port[str(num)]
    sockfd.bind(('127.0.0.1', port))
    sockfd.listen(8)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    pdk = PokerDesk(sockfd, db, num)
    pdk.server_run()


if __name__ == '__main__':
    main()
















