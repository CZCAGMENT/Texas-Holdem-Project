# playpoker_main.py

import socket
# import os
import sys
from menu import *
from player_login import *


def main():
    sockfd = socket.socket()
    try:
        sockfd.connect(('127.0.0.1', 8888))
    except Exception as e:
        print(e)
        return
    pln = Player_login(sockfd)
    while True:
        menu0()
        try:
            cmd = int(input('请输入选项'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1, 2, 3]:
            print('请输入正确选项')
            sys.stdin.flush()
            continue
        elif cmd == 1:
            name = pln.user_login()
            if name !=2 and name != None:
                print('登录成功')
                pln.user_play(name)
            elif name == 2:
                print("用户已在线")
            else:
                print('用户名或密码不正确')
        elif cmd == 2:
            pln.user_register()
        elif cmd == 3:
            sockfd.send(b'E')
            sys.exit('谢谢使用')


if __name__ == '__main__':
    main()











