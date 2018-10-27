# menu.py


def menu0():
    print('+========================+')
    print('|                        |')
    print('|   1.登录               |')
    print('|    2.注册              |')
    print('|     3.退出             |')
    print('|                        |')
    print('+========================+')


def menu1(L):
    print('=========================================')
    print('|                                       |')
    print('|  1.01桌(%s/8) 2.02桌(%s/8) 3.03桌(%s/8)  |' % (L[0], L[1], L[2]))
    print('|  4.04桌(%s/8) 5.05桌(%s/8) 6.06桌(%s/8)  |' % (L[3], L[4], L[5]))
    print('|  7.07桌(%s/8) 8.08桌(%s/8) 9.09桌(%s/8)  |' % (L[6], L[7], L[8]))
    print('|  0.10桌(%s/8)                    |' % L[9])
    print('|                                       |')
    print('| 输入桌号,(q退出)                      |')
    print('=========================================')


def desk_print(dict, desk=''):
    for i in range(1, 9):
        if i not in dict:
            dict[i]='null'
    print('玩家1:%s' % dict[1])
    print('玩家2:%s' % dict[2])
    print('玩家3:%s' % dict[3])
    print('玩家4:%s' % dict[4])
    print('玩家5:%s' % dict[5])
    print('玩家6:%s' % dict[6])
    print('玩家7:%s' % dict[7])
    print('玩家8:%s' % dict[8])
    print('桌牌:%s' % desk)


if __name__ == '__main__':
    menu0()
    menu1()
    desk_print(['zhangsan', 'lisi'])







