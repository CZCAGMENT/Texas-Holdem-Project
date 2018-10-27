# player_login.py

import getpass
from menu import *
import socket
from text_client import *


class Player_login(object):
    def __init__(self, s):
        self.s = s
        self.sockfr = socket.socket()
        

    def user_login(self):
        '''用户登录'''
        name = input('User:')
        passwd = getpass.getpass()
        msg = 'L {} {}'.format(name, passwd)
        self.s.send(msg.encode())
        data = self.s.recv(128).decode()
        if data == 'ok':
            return name
        elif data == "on":
            return 2
        else:
            return

    def user_register(self):
        '''用户注册'''
        while True:
            name = input('User:')
            passwd = getpass.getpass()
            passwd1 = getpass.getpass('Aganin:')
            if (' ' in name) or (' ' in passwd):
                print('用户名密码不允许有空格')
                continue
            if passwd != passwd1:
                print('两次密码不一致')
                continue

            msg = 'R {} {}'.format(name, passwd)
            self.s.send(msg.encode())
            data = self.s.recv(128).decode()
            print(data)
            if data == 'ok':
                print('注册成功')
                return
            elif data == 'EXISTS':
                print('用户存在')
            else:
                print('注册失败')

    def user_play(self, name):
        '''选择桌号'''
        while True:
            # 未完成
            menu1(['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'])
            try:
                cmd = input('请选择桌号(q退出)')
            except KeyboardInterrupt:
                self.do_online_out(name)
                self.sockfr.close()
                sys.exit("客户端退出")
            except Exception as e:
                print(e)
                print('命令错误')
                continue
            if cmd == 'q':
                self.do_online_out(name)
                return
            if int(cmd) not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
                print('请输入正确选项')
                sys.stdin.flush()
                continue
            else:
                self.do_join(name, cmd)
                print("又回来了")

    def do_join(self, name, num):
        '''获取牌桌相关信息　进入桌子'''
        msg = 'J {} {}'.format(name, num)
        self.s.send(msg.encode())
        data = int(self.s.recv(128).decode())
        print(data)
        playgame = PlayDesk_client(data,name)
        playgame.roomthing()
    

    def do_online_out(self,name):
        msg = 'B '+ name
        self.s.send(msg.encode())

















