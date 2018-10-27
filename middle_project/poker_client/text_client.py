import socket
import select
import threading
import sys
import time

class PlayDesk_client(object):
    def __init__(self,port,name):
        self.host = "127.0.0.1"
        self.addr = (self.host, port)
        self.name = name


    def conn(self):
        s = socket.socket()
        s.connect(self.addr)
        return s


    def lis(self,s):
        my = [s]
        while True:
            r, w, e = select.select(my, [], [])
            for s in r:
                try:
                    data = s.recv(1024).decode()
                    if data == "F":
                        print("房间已满")
                        return
                    # if data == "#$%":
                    #     print("谢谢使用!")
                    #     return
                    print(data)
                except socket.error:
                    print('socket is error')
                    sys.exit()


    def roomthing(self):
        ss = self.conn()
        t1 = threading.Thread(target=self.lis, args=(ss,))
        t1.daemon = True
        t1.start()
        time.sleep(0.1)
        ss.send(self.name.encode())
        while True:
            try:
                info = input()
            except KeyboardInterrupt:
                ss.send(b"!@#")
                ss.close()
                sys.exit("客户端退出")
            except Exception as e:
                print(e)
            try:
                if info == "":
                    print("无法发送空消息")
                else:
                    ss.send(info.encode())
                    if info == "-exit":
                        print("您已退出房间")
                        ss.close()
                        time.sleep(0.5)
                        return
            except Exception as e:
                print(e)

            
            
           


if __name__ == '__main__':
    roomthing()
