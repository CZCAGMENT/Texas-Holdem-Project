# poker_link.py
import time
from port import *


class PokerLink(object):
    '''服务器类　用于处理客户端　登录注册请求'''
    def __init__(self, c, db):
        self.c = c
        self.db = db
        self.cursor = self.db.cursor()

    def do_login(self, data):
        '''处理用户登录'''
        data_list = data.split(' ')
        name = data_list[1]
        passwd = data_list[2]
        sql = 'select * from player where name=%s \
               and password=%s'
        self.cursor.execute(sql, [name, passwd])
        r = self.cursor.fetchone()
        if r is None:
            self.c.send(b'FALL')
        elif r[4] == "on":
            self.c.send(b'on')
        else:
            self.c.send(b'ok')
            self.do_changeline(name)


    def do_changeline(self,name):
        sql = "update player set online='oo' where name=%s"
        try:
            self.cursor.execute(sql, name)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            print("设置在线状态成功")


    def do_lineout(self,data):
        data_list = data.split(' ')
        print(data_list)
        name = data_list[1]
        sql = "update player set online='out' where name=%s"
        try:
            self.cursor.execute(sql, name)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            print("设置离线状态成功")



    def do_register(self, data):
        '''处理用户注册'''
        data_list = data.split(' ')
        name = data_list[1]
        passwd = data_list[2]
        sql = 'select * from player where name=%s'
        self.cursor.execute(sql, [name])
        r = self.cursor.fetchone()
        if r is not None:
            self.c.send('EXISTS'.encode())
            return
        sql = 'insert into player (name,password,chouma) values (%s,%s,%s)'
        try:
            self.cursor.execute(sql, [name, passwd, 10000])
            self.db.commit()
            self.c.send(b'ok')
        except Exception as e:
            print(e)
            self.db.rollback()
            self.c.send(b'FALL')
        else:
            print("%s注册成功" % name)

    def do_join(self, data):
        '''处理用户进房间请求'''
        data_list = data.split(' ')
        print(data_list)
        port = d_port[data_list[2]]
        name = data[1]
        self.c.send(str(port).encode())
        # time.sleep(0.1)
        # self.c.send(name.encode)



if __name__ == '__main__':
    print(d_port)


