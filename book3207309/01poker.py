# Coding: utf-8

# Cards Module


class Card:
    """ A playing card"""
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS = ["梅", "方", "红", "黑"]  # "梅"为梅花，"方"为方钻，"红"为红心，"黑”为黑桃

    def __init__(self, rank, suit, face_up=True):
        self.rank = rank  # 指的是牌面数字1~13
        self.suit = suit  # 指的是花色
        self.is_face_up = face_up  # 是否显示牌的正面

    def __str__(self):  # 重写print方法，打印一张牌的信息
        if self.is_face_up:
            rep = self.suit + self.rank
        else:
            rep = "XX"
        return rep

    def pic_order(self):  # 牌的顺序
        if self.rank == "A":
            FaceNum = 1
        elif self.rank == "J":
            FaceNum = 11
        elif self.rank == "Q":
            FaceNum = 12
        elif self.rank == "K":
            FaceNum = 13
        else:
            FaceNum = int(self.rank)

        if self.suit == "梅":
            Suit = 1
        elif self.suit == "方":
            Suit = 2
        elif self.suit == "红":
            Suit = 3
        else:
            Suit = 4

        return (Suit - 1) * 13 + FaceNum

    def flip(self):  # 翻牌方法
        self.is_face_up = not self.is_face_up


class Hand:
    """A hand of playing cards."""

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "\t"
            else:
                rep = "无牌"
            return rep

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):  # 把一张牌给其他牌手
        self.cards.remove(card)
        other_hand.add(card)


# CLass Poke
class Poke(Hand):
    """A deck of playing cards"""

    def populate(self):  # 生成一副牌
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))

    def shuffle(self):  # 洗牌
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand=13):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.cards.remove(top_card)
                    hand.add(top_card)
                    # self.give(top_card,hand) #上两句可用此语句替换
                else:
                    print("不能继续发牌了，牌已经发完了！")


# 主程序
if __name__ == "__main__":
    print("This is a module with classes for playing cards")
    # 4个玩家
    players = [Hand(), Hand(), Hand(), Hand()]
    poke1 = Poke()
    poke1.populate()  # 生成一副牌
    poke1.shuffle()
    poke1.deal(players, 13)  # 发给每人13张牌
    # 显示4位牌手的牌
    n = 1
    for hand in players:
        print("牌手", n, end=":")
        print(hand)
        n = n + 1
    input("\nPress the enter key to exit.")
