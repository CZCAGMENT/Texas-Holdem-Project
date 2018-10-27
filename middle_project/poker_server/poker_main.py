# poker_main.py

from socket import *
import os
import sys
import signal
import pymysql
from poker_link import *


def main():
    db = pymysql.connect('localhost', 'root', '123456', 'Texaspokes')
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(('', 8888))
    sockfd.listen(5)
    # 忽略子进程信号，子进程退出后由系统处理
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            c, addr = sockfd.accept()
            print(addr, '已连接')
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            plk = PokerLink(c, db)
            while True:
                data = c.recv(1024).decode()
                # 判断客户端请求
                if not data:
                    c.close()
                    sys.exit() 
                elif  data[0] == 'B':
                    plk.do_lineout(data)
                elif data[0] == 'L':
                    plk.do_login(data)
                elif data[0] == 'R':
                    plk.do_register(data)
                elif data[0] == 'J':
                    plk.do_join(data)
        else:
            c.close()
            continue


if __name__ == '__main__':
    main()



















