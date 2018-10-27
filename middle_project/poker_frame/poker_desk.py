# poker_desk.py
import pymysql
from socket import *
import select
from port import *
import time
from poker_duch import *


class PokerDesk(object):
    def __init__(self, s, db, num):
        self.desknum = str(num)
        self.db = db
        self.cursor = self.db.cursor()
        self.sockfd = s
        self.rlist = []         #套接字列表
        self.player_data = {}   #当局玩家筹码列表,以昵称为键,以当局个人下注总筹码为值
        self.fd_name = {}       #玩家昵称字典,以套接字为键,以昵称为值
        self.master = ''        #房主
        self.already = []       #准备玩家列表,为玩家套接字
        self.maxchip = []       #玩家数据库中的筹码值列表
        self.outline=[]         #掉线玩家列表,存套接字

    def server_run(self):
        self.rlist.append(self.sockfd)
        while True:
            r, w, e = select.select(self.rlist, [], [])
            for temp in r:
                if temp is self.sockfd:
                    self.new_coming(temp)
                else:
                    data = temp.recv(1024).decode()
                    print(data)
                    if data == "-ready" and temp in self.already:
                        data = "您已处于准备状态,无需准备"
                        temp.send(data.encode())
                    elif data == "-ready" and temp not in self.already:
                        data = "您已准备"
                        temp.send(data.encode())
                        self.already.append(temp)
                        msg = "玩家%s已准备"%self.fd_name[temp]
                        self.do_notice(msg,temp)

                    elif data == "-go" and self.fd_name[temp] == self.master and len(self.already) > 1:
                        win_player = self.play()
                        for x in win_player:
                            print(x)
                            data = "\n%s获胜" % (self.fd_name[x])
                            self.do_notice(data)
                            #打印本局筹码结果
                        print(self.player_data)
                        self.do_savechip(win_player)
                        for x in self.outline:
                            self.do_bengkui(x)
                        self.already.clear()
                        self.maxchip.clear()
                        self.outline.clear()

                    elif data == "-exit":
                        self.do_exit(temp)

                    elif data == "!@#":
                        self.do_bengkui(temp)


                    else:
                        data = self.fd_name[temp] + ' say : ' + data
                        self.do_notice(data,temp)

    #保存游戏结果到数据库
    def do_savechip(self,L):
        while True:
            for x in self.player_data:
                l = []
                for i in L:
                    l.append(self.fd_name[i])
                name = x
                sql = 'select name,chouma from player where name=%s '
                self.cursor.execute(sql, name)
                r = self.cursor.fetchone()
                sql_chouma = r[1]
                game_chouma = self.player_data.get(name)
                print(L)
                print(l)
                print(name)
                print(sql_chouma)
                print(game_chouma)
                if  name not in l:
                    chouma = sql_chouma - game_chouma
                else:
                    chouma = sql_chouma + (sum(self.player_data.values())-len(l)*max(self.player_data.values()))/len(l)
                sql = 'update player set chouma=%s where name=%s'
                try:
                    self.cursor.execute(sql, [chouma,name])
                    self.db.commit()
                except Exception as e:
                    print(e)
                    self.db.rollback()
                else:
                    print("游戏记录保存到数据库")
                    
            return
                




    def new_coming(self, temp):
        client, addr = temp.accept()
        name = client.recv(1024).decode()
        self.rlist.append(client)
        # 如果房间已满 不再允许进入
        if len(self.rlist) > 9:
            client.send(b'F')
            self.rlist.remove(client)
            return
        # 如果为第一人 定义为房主？
        elif len(self.rlist) == 2:
            self.master = name
        print(name, '进入')
        msg = '# %s进入了%s号桌' % (name, self.desknum)
        # 给其他玩家发送进房信息
        self.do_notice(msg,client)

        # for i in range(1, 9):
        #     if i not in self.player:
        #         self.player[i] = name
        #         break
        self.fd_name[client] = name
        nameList = "\n现在有%s在房间内,房主为:%s" % (self.who_in_room(),self.master)
        print("*******************")
        self.show_playerchip()
        self.do_notice(nameList)


    def who_in_room(self):
        name_list = []
        for k in self.fd_name:
            name_list.append(self.fd_name[k])
        data = "  ".join(name_list)

        return data

    def do_bengkui(self,temp):
        self.rlist.remove(temp)
        if len(self.rlist) == 1:
            self.master = ""
            self.do_lineout(temp)
            del self.fd_name[temp]
            temp.close()
            return
        data = self.fd_name[temp] + ' 离开了房间'
        print(data)
        self.do_notice(data,temp)
        if self.fd_name[temp] == self.master and len(self.rlist) > 1:
            self.master = self.fd_name[self.rlist[1]]
            # self.do_notice(data)
        self.do_lineout(temp)
        del self.fd_name[temp]
        nameList = []       
        nameList = "\n现在有%s在房间内,房主为:%s" % (self.who_in_room(),self.master)
        self.do_notice(nameList,temp)
        temp.close()


    def do_lineout(self,temp):
        name = self.fd_name[temp]
        print(name)
        sql = "update player set online='out' where name=%s"
        try:
            self.cursor.execute(sql, name)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            print("设置离线状态成功")


    def do_exit(self,temp):
        self.rlist.remove(temp)
        if len(self.rlist) == 1:
            self.master = ""
            del self.fd_name[temp]
            temp.close()
            return
        data = self.fd_name[temp] + ' 离开了房间'
        print(data)
        self.do_notice(data)
        if self.fd_name[temp] == self.master and len(self.rlist) > 1:
            self.master = self.fd_name[self.rlist[1]]
            # self.do_notice(data)
        del self.fd_name[temp]
        nameList = []       
        nameList = "\n现在有%s在房间内,房主为:%s" % (self.who_in_room(),self.master)
        self.do_notice(nameList)
        temp.close()


    def do_notice(self,data,own=None):  # 给除own以外玩家发送公告
        for all in self.rlist:
            if all  not in (self.sockfd,own) and all not in self.outline:
                try:
                    all.send(data.encode())
                except Exception as e:
                    print(e)



    def show_playerchip(self):
        chip = ""
        for x in self.fd_name:
            sql = 'select name,chouma from player where name=%s '
            self.cursor.execute(sql, [self.fd_name[x]])
            r = self.cursor.fetchone()
            chip =chip + "\n姓名:%s,筹码值:%s"%(r[0],r[1])
            self.maxchip.append(r[1])
        self.do_notice(chip)
            




    def play(self):
        hand_card = []  # 创建手牌列表
        number = len(self.already)  # 游戏玩家人数
        data = "玩家人数为:"+str(number)
        self.do_notice(data)
        msg = "本局最大下注总值为:%d"%max(self.maxchip)
        print(data)
        self.do_notice(msg)
        n = 0
        for p in range(len(self.already)):
            self.player_data[self.fd_name[self.already[p]]] = 100  # 创建当局玩家字典,默认底注100
            print(self.player_data)
        A = Poker_duch(number)  # 调用荷官类
        # public = A.desk_deck    # 生成5张公共牌

        # 第一轮发牌--手牌
        for handcards in A.player_deck:    # 每个玩家发2张手牌
            self.already[n].send(('\n手牌为:').encode())
            self.already[n].send("     ".join(handcards).encode())
            hand_card.append(handcards)   # 生成手牌列表
            n += 1
        player_dict = dict(zip(self.already, hand_card))  # 生成玩家对应手牌字典
        print(player_dict)
        sol1 = self.Bet()
        if self.the_lastplayer():
            return self.already
        time.sleep(1)

        # 第二轮发牌--3张公共牌
        print(A.show_desk)
        data = '\n公共牌为:' + "     ".join(A.show_desk)
        self.do_notice(data)
        sol2 = self.Bet()
        if self.the_lastplayer():
            return self.already
        time.sleep(1)

        # 第三轮发牌--第4张公共牌
        print(A.show_desk1)
        data = '\n公共牌为:' + "     ".join(A.show_desk) + "     "+A.show_desk1
        self.do_notice(data)
        sol3 = self.Bet()
        if self.the_lastplayer():
            return self.already
        time.sleep(1)

        # 第四轮发牌--第5张公共牌
        print(A.show_desk2)
        data = '\n公共牌为:' + "     ".join(A.show_desk) + "     " + A.show_desk1 + "     "+ A.show_desk2
        self.do_notice(data)
        alive = []  # 过度列表
        sol4 = self.Bet()
        if self.the_lastplayer():
            return self.already
        time.sleep(1)
        for i in self.already:  # 此already列表为最后参比玩家
            print(self.fd_name[i])
            alive.append(player_dict.get(i))
        last_handcard = dict(zip(self.already, alive))  # 利用过度列表生成最后参比玩家对应手牌字典
        print(last_handcard)

        winer = A.max_hand(last_handcard)
        print(winer)
        for w in winer:
            data = "获胜玩家手牌为:%s"%last_handcard[w]
            print(data)
            self.do_notice(data)
        self.already.clear()
        return winer

    #判断玩家人数,若为1人,则其余人弃牌,此人获胜,返回列表
    def the_lastplayer(self):
        if len(self.already) == 1:
            
            return True
        else:
            return None


    # 下注
    def Bet(self):
        circle = 0
        folder = []
        document = "\n-call:加注金额 , -raise跟注 , -check看牌 , -fold弃牌"
        while True:
            circle += 1
            for n in range(len(self.already)):
                while True:
                    try:
                        self.already[n].send(document.encode())  # 发送命令提示
                        self.already[n].settimeout(300)  # 设置阻塞超时检测300s
                    except Exception as e:
                        folder.append(self.already[n])
                        self.outline.append(self.already[n])
                        data = "玩家%s选择弃牌并离开了房间" % (self.fd_name[self.already[n]])
                        self.do_notice(data)
                        break
                    print("请等待对方选择")
                    try:
                        data = self.already[n].recv(256).decode()
                    except Exception as e:
                        print('等待超时', e)
                        folder.append(self.already[n])
                        data = "玩家%s选择弃牌" % (self.fd_name[self.already[n]])
                        self.do_notice(data)
                        break
                    else:
                        keyword = data.split(":")
                        if keyword[0] == "-call":  # 若为加注,更新当局玩家字典
                        #若加注不是最大.则重新加注
                            if self.player_data[self.fd_name[self.already[n]]] + int(keyword[1]) \
                                > max(self.player_data.values()):
                                self.player_data[self.fd_name[self.already[n]]] += int(keyword[1])

                                print(self.player_data)
                                data = "玩家%s选择加注%s" % (self.fd_name[self.already[n]], keyword[1])
                                self.do_notice(data)
                                break  # 发送玩家操作公告
                            elif self.player_data[self.fd_name[self.already[n]]] + int(keyword[1]) \
                                > max(self.maxchip):
                                data = "所加筹码不能大于本局最大下注总值%d"%max(self.maxchip)
                                self.already[n].send(data.encode())
                            else:
                                data = "所加筹码必需大于上一位玩家"
                                self.already[n].send(data.encode())
                        elif keyword[0] == "-raise":
                            # 若为跟注,则将筹码更新为当局玩家字典中最大值
                            self.player_data[self.fd_name[self.already[n]]] = max(self.player_data.values())
                            print(self.player_data)
                            data = "玩家%s选择跟注" % (self.fd_name[self.already[n]])
                            self.do_notice(data)
                            break
                        elif keyword[0] == "-check":
                            # 若为看牌,判断所下筹码是否为当前玩家字典最大值,如若是,直接发送公告,不做操作,若不是提示无法看牌
                            if self.player_data[self.fd_name[self.already[n]]] != max(self.player_data.values()):
                                data = "您无法选择看牌"
                                self.already[n].send(data.encode())
                            else:
                                data = "玩家%s选择看牌" % (self.fd_name[self.already[n]])
                                self.do_notice(data)
                                break
                            #若玩家在游戏中轮到他时掉线或者强退
                        elif data == "" or data =="!@#":
                            folder.append(self.already[n])
                            self.outline.append(self.already[n])
                            data = "玩家%s选择弃牌并离开了房间" % (self.fd_name[self.already[n]])
                            self.do_notice(data)
                            break

                        else:  # 若为其他输入,视为弃牌操作
                            folder.append(self.already[n])
                            data = "玩家%s选择弃牌" % (self.fd_name[self.already[n]])
                            self.do_notice(data)
                            break
                if circle > 1:
                    print("这是第%s圈" % circle)
                    for v in self.player_data.values():
                        if v != max(self.player_data.values()):
                            print("第%s圈结束" % circle)
                            break
                    else:
                        print("第%s圈达成一致" % circle)
                        for i in folder:
                            self.already.remove(i)
                        return self.player_data

            for i in folder:  # 更新玩家准备列表,将弃牌玩家移除
                self.already.remove(i)
            folder.clear()
            for t in self.already:  # 判断第一圈下注是否达成一致,如一致,返回当局玩家信息字典,如不一致,继续下注
                m = self.fd_name[t]
                v = self.player_data[m]
                print(v)
                print(max(self.player_data.values()))
                if v != max(self.player_data.values()):
                    break
            else:
                return self.player_data

        return self.player_data






