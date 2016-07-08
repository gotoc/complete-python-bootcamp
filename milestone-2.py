# https://github.com/jmportilla/Complete-Python-Bootcamp/blob/master/Milestone%20Project%202%20-%20Assignment.ipynb
# Milestone Project 2 - Blackjack Game

import random

INPUT_TEXT = {  'H':"Hearts",'D':"Diamonds",'S':"Spades",'C':"Clubs",
                'J':"Jack",'Q':"Queen",'K':"King",'A':"Ace",
                'ace':"Would you like your Ace to count for 1 or 11 points? Enter 1 or 11: ",
                'bet':"%s, please enter a bet between 1 and %s: ", # player balance
                'hit':"%s, would you like a hit? Y or N: " # player name
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

    def reshuffle(self):
        self.__init__()

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

    def __init__(self, bank, name, dealer=False):
        Money.__init__(self, bank)
        Points.__init__(self, dealer)
        self.hand = []
        self.bet = 0
        self.stand = False
        self.name = name

    def add_card(self,cards):
        for c in cards:
            self.hand.append(c)
        self.set_points(cards)

    def clear_hand(self):
        del self.hand[:]


class Bet(object):

    def place_bet(self,player):
        if player.dealer == False:
            while True:
                try:
                    the_bet = int(raw_input(INPUT_TEXT['bet']%(player.name,str(player.balance))))
                    if the_bet >= 1 and the_bet <= player.balance:
                        player.bet = the_bet
                        break
                except:
                    continue

    def settle_bet(self,player,condition='T'):
        if condition == 'W':
            player.balance = player.bet + player.balance
        elif condition == "L":
            player.balance = player.balance - player.bet
        player.bet = 0


class Turn(object):

    def __init__(self,deck,player):
        # add condition for double(double bet, take card, stand)
        # add condition for surrender(lose 1/2 bet and forfeit hand)
        if player.dealer == False:
            # Take another card or stand
            while True:
                response = raw_input(INPUT_TEXT['hit']%(player.name)).upper()
                if response == "Y":
                    player.add_card(deck.deal_card(1))
                    break
                elif response == "N":
                    player.stand = True
                    break
        elif player.dealer == True:
            if player.points < 17:
                player.add_card(deck.deal_card(1))
            else:
                player.stand = True


class WinLose(object):

    def check_cond(self):
        pass
            # winner/loser is determined
            # if 21: win message
            # elif over 21: lose message


class Table(object):

    def __init__(self,players,bets):
        self.player = players
        self.bets = bets

    def draw(self):
        name = self.player[1].name
        print "-------------------------"
        print name + " balance: ",self.player[1].balance
        print name + " has bet: ",self.player[1].bet
        print name + " hand: ",self.player[1].hand
        print name + " points: ",self.player[1].points
        if self.player[1].stand == True:
            print name + " is standing."
        print "-------------------------"
        print "Dealer points: ",self.player[0].points
        print "Dealer hand: ",self.player[0].hand
        print "-------------------------"


class Main():

    # Player objects are stored in list
    player = [Player(0,"Dealer",True)]

    def __init__(self):
        self.deck = Deck()
        self.bets = Bet()
        t = Table(self.player,self.bets)

        # Set up the players
        num_players = 1  # can come back later to add input for multiplayer
        i = 0
        while i < num_players:
            name = raw_input("Please enter your name: ")
            self.player.append(Player(50,name))
            i += 1
        # Start the game
        print "Welcome, %s. This is Blackjack. It's a card game." %(self.player[1].name)
        # deal initial 2 cards to players
        self.player[0].add_card(self.deck.deal_card(2))
        self.player[1].add_card(self.deck.deal_card(2))
        t.draw()
        # Place bets before rounds begin
        for p in self.player:
            self.bets.place_bet(p)
        # Play through rounds until every player stands
        stand_count = 0
        while stand_count < num_players:
            for p in self.player:
                if p.stand == False:
                    Turn(self.deck,p)
                    if p.dealer == False:
                        t.draw()
                else:
                    stand_count += 1
            #WinLose()


Main()
