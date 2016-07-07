# https://github.com/jmportilla/Complete-Python-Bootcamp/blob/master/Milestone%20Project%202%20-%20Assignment.ipynb
# Milestone Project 2 - Blackjack Game

import random

INPUT_TEXT = {  'H':"Hearts",'D':"Diamonds",'S':"Spades",'C':"Clubs",
                'J':"Jack",'Q':"Queen",'K':"King",'A':"Ace",
                'ace':"Would you like your Ace to count for 1 or 11 points? Enter 1 or 11: ",
             }

class Money(object):

    def __init__(self, balance=100):
        self.balance = balance

    def add_balance(self,amount):
        self.balance += amount

    def sub_balance(self,amount):
        self.balance -= amount

class Deck(object):

    suit = ['H','D','S','C']
    rank = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self):
        # Build the deck of cards as list of tuples
        self.deck = []
        for s in self.suit:
            for r in self.rank:
                self.deck.append((s,r))

    def get_card(self):
        # grab random card from deck
        while True:
            c = random.randrange(0,51)
            try:
                return self.deck[c]
                break
            except IndexError:
                continue

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

class Points(object):
    global INPUT_TEXT

    def __init__(self, dealer=False):
        self.points = 0
        self.dealer = dealer

    def set_points(self,cards):
        # expect cards to be a list of tuples
        for c in cards:
            s,r = c
            try:
                self.points += int(r)
            except:
                if r == "J" or r == "Q" or r == "K":
                    self.points += 10
                elif r == "A":
                    # dealer-mode adds default values for Ace depending on
                    # the current point total
                    if self.dealer == True:
                        if self.points <= 10:
                            self.points += 11
                        else:
                            self.points += 1
                    # allow the player to choose Ace value manually
                    else:
                        while True:
                            try:
                                a = int(raw_input(INPUT_TEXT['ace']))
                            except:
                                continue
                            if a == 1 or a == 11:
                                self.points += a
                                break
                            else:
                                continue

class Player(Money, Points):

    def __init__(self, bank, dealer=False):
        Money.__init__(self, bank)
        Points.__init__(self, dealer)
        self.hand = []
        self.hold = False

    def add_card(self,cards):
        for c in cards:
            self.hand.append(c)
        self.set_points(cards)

    def clear_hand(self):
        del self.hand[:]

class Round(object):

    def __init__(self,player_object):
        self.player = player_object
        # go through a round of BJ:
        # if player.dealer==False, player lays bet
        # if Player takes card, deal card
        # else Player.hold = True
        # winner/loser is determined
            # if 21: win message
            # elif over 21: lose message

class Table(object):
    pass
    # draw visual elements to show player

class Main():

    deck = Deck()
    player1 = Player(50)
    dealer = Player(5000,True)

    def __init__(self):
        print "This is Blackjack. It's a card game."
        # deal initial 2 cards to players
        self.dealer.add_card(self.deck.deal_card(2))
        self.player1.add_card(self.deck.deal_card(2))

        # while self.player1.hold == False and self.dealer.hold == False:
            # Table.draw()
            # Round()

        #### Testing out methods
        print "Player 1 balance: ",self.player1.balance
        print "Player 1 points: ",self.player1.points
        print "Player 1 hand: ",self.player1.hand
        print "-------------------------"
        self.player1.add_card(self.deck.deal_card(1))
        print "Player 1 hand: ",self.player1.hand
        print "Player 1 points: ",self.player1.points
        print "-------------------------"
        print "Dealer balance: ",self.dealer.balance
        print "Dealer points: ",self.dealer.points
        print "Dealer hand: ",self.dealer.hand
        print "-------------------------"
        print "Deck: ",self.deck.deck

Main()
