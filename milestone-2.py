# https://github.com/jmportilla/Complete-Python-Bootcamp/blob/master/Milestone%20Project%202%20-%20Assignment.ipynb
# Milestone Project 2 - Blackjack Game

import random

class Money(object):

    def __init__(self, balance=100):
        self.balance = balance

    def add_balance(self,amount):
        self.balance += amount

    def sub_balance(self,amount):
        self.balance -= amount

class Deck(object):

    deck = []
    suit = ['H','D','S','C']
    rank = ['1','2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self):
        # Build the deck of cards as list of tuples
        for s in self.suit:
            for r in self.rank:
                self.deck.append((s,r))

    def get_card(self):
        # grab random card from deck
        c = random.randrange(0,52)
        return self.deck[c]

    def deal_card(self,amount=1):
        # add to hand and delete from deck
        cards = []
        i = 1
        while i <= amount:
            card = self.get_card()
            cards.append(card)
            self.deck.remove(card)
            i += 1
        return cards

class Player(Money):

    def __init__(self, bank):
        Money.__init__(self,bank)
        self.hand = []

    def add_card(self,cards):
        for c in cards:
            self.hand.append(c)

    def clear_hand(self):
        del self.hand[:]


class Main():

    deck = Deck()
    player1 = Player(50)
    dealer = Player(5000)

    def __init__(self):
        self.player1.add_card(self.deck.deal_card(2))
        self.dealer.add_card(self.deck.deal_card(2))

        print "This is Blackjack. It's a card game."

        print "Player 1 balance: ",self.player1.balance
        print "Player 1 hand: ",self.player1.hand
        print "Dealer balance: ",self.dealer.balance
        print "Dealer hand: ",self.dealer.hand
        print "Deck: ",self.deck.deck

Main()
