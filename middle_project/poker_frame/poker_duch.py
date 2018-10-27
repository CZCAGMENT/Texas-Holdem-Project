# poker_dach.py

import itertools
import random


class Poker_duch(object):
    '''荷关类，用于发牌，比较大小，宣布赢家
    '''
    def __init__(self, numhands, n=2):
        '''发牌，生成玩家手牌列表　桌牌，
        numhands代表玩家数，n为手牌数量'''
        self.deck = [r + s for r in '23456789TJKQA' for s in'♥♠♣♦']
        random.shuffle(self.deck)
        self.player_deck = [
            self.deck[n * i:n * (i + 1)] for i in range(numhands)]
        self.desk_deck = self.deck[n * numhands:n * numhands + 5]
        self.show_desk = self.desk_deck[:3]
        self.show_desk1 = self.desk_deck[3]
        self.show_desk2 = self.desk_deck[4]

    def allplayerhands(self, hand_dict):
        '''将玩家手牌和桌牌生成玩家牌字典'''
        allhands_dict = {}
        for i in hand_dict:
            allhands_dict[i] = hand_dict[i] + self.desk_deck
        return allhands_dict

    def _group(self, items):
        '''处理５张牌组　返回含有（张数, 牌面）元组的列表'''
        groups = [(items.count(x), x) for x in set(items)]
        return sorted(groups, reverse=True)

    def hand_ranks(self, hand):
        '''根据牌型返回相应列表，用于比较大小'''
        hand_list = ['--23456789TJQKA'.index(r) for r, s in hand]
        groups = self._group(hand_list)
        # 用zip函数将含有（张数, 牌面）的元组转化为张数，牌面两个元组赋值给变量
        counts, ranks = zip(*groups)
        if ranks == (14, 5, 4, 3, 2):
            ranks = (5, 4, 3, 2, 1)
        # straight为判断顺子的布尔值
        straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
        # flush为判断顺子的布尔值
        flush = len(set([s for r, s in hand])) == 1
        if (5,) == counts:
            return [9, ranks]
        elif straight and flush:
            return [8, ranks]
        elif (4, 1) == counts:
            return [7, ranks]
        elif (3, 2) == counts:
            return [6, ranks]
        elif flush:
            return [5, ranks]
        elif straight:
            return [4, ranks]
        elif (3, 1, 1) == counts:
            return [3, ranks]
        elif (2, 2, 1) == counts:
            return [2, ranks]
        elif (2, 1, 1, 1) == counts:
            return [1, ranks]
        else:
            return [0, ranks]

    def allmax(self, iterable):
        '''根据玩家牌型列表选出最大牌型'''
        result, maxval = [], None
        for x in iterable:
            xval = self.hand_ranks(x)
            if not result or xval > maxval:
                result, maxval = [x], xval
            elif xval == maxval:
                result.append(x)
        return result

    def allhands(self, hands):
        '''根据７张牌排列出所有牌型列表'''
        allhands = list(itertools.combinations(hands, 5))
        return allhands

    def max_hand(self, hand_dict):
        '''比较所有玩家的最大牌型　宣布赢家'''
        winer = []
        allplayer_max = {}
        allhands_dict = self.allplayerhands(hand_dict)
        for i in allhands_dict:
            max_h = self.allmax(self.allhands(allhands_dict[i]))
            allplayer_max[i] = max_h[0]
        win_hand = self.allmax(allplayer_max.values())
        for p in allplayer_max:
            if allplayer_max[p] in win_hand:
                winer.append(p)
        return winer


if __name__ == '__main__':
    A = Poker_duch(5)
    print(A.desk_deck)
    print(A.show_desk, A.show_desk1, A.show_desk2)
    print(A.player_deck)
    hand_dict = {}
    n = 0
    for a in 'abcde':
        hand_dict[a] = A.player_deck[n]
        n += 1
    print(hand_dict)
    w = A.max_hand(hand_dict)
    print(w)











