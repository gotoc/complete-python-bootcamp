# https://github.com/jmportilla/Complete-Python-Bootcamp/blob/master/Milestone%20Project%202%20-%20Assignment.ipynb
# Milestone Project 2 - Blackjack Game

import random

INPUT_TEXT = {  'line':"-------------------------",
                'ask_name':"Hello, Player %s. Please enter your name: ", # num_players
                'ace':"Would you like your Ace to count for 1 or 11 points? Enter 1 or 11: ",
                'bet':"%s, please enter a bet between 1 and %s: ", # player.name, player.balance
                'hit':"%s, would you like a hit? Y or N: ", # player.name
                'over':"%s busts with %s points.", # player.name, player.points
                'under':"%s stood with %s points.", # player.name, player.points
                'blackjack':"%s reached %s points.", # player.name, player.points
                'replay':"Do you want to play again? (y or n): "
                }
CARD_TEXT = {   'H':"Hearts",'D':"Diamonds",'S':"Spades",'C':"Clubs",
                'J':"Jack",'Q':"Queen",'K':"King",'A':"Ace",
                '2':"Two",'3':"Three",'4':"Four",'5':"Five",
                '6':"Six",'7':"Seven",'8':"Eight",'9':"Nine",'10':"Ten"
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

    def set_points(self,cards,auto_ace=False):
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
                    if self.dealer == True or auto_ace == True:
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
        self.name = name
        self.hand = []
        self.bet = 0
        self.state = "under"
        self.stand = False

    def add_card(self,cards,auto_ace=False):
        for c in cards:
            self.hand.append(c)
        self.set_points(cards,auto_ace)
        # Auto-stand
        if self.points > 21:
            self.state = "over"
            self.stand = True
        elif self.points == 21:
            self.state = "blackjack"
            self.stand = True

    def clear(self):
        del self.hand[:]
        self.bet = 0
        self.points = 0
        self.state = "under"
        self.stand = False


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


class Table(object):

    def draw_hand(self, player_obj):
        cards = []
        for c in player_obj.hand:
            s,r = c
            cards.append(CARD_TEXT[str(r)] + " of " + CARD_TEXT[s])

        print INPUT_TEXT['line']
        print "%s's hand: "%(player_obj.name),cards
        print "Hand's point-worth: ",player_obj.points
        print INPUT_TEXT['line']

    def draw_money(self, player_obj):
        print INPUT_TEXT['line']
        print "%s's current bet: $%s"%(player_obj.name,str(player_obj.bet))
        print "%s's balance: $%s"%(player_obj.name,str(player_obj.balance))
        print INPUT_TEXT['line']

    def draw_turn_end(self,player_obj):
        if player_obj.state == "over":
            print "* %s busted! *"%(player_obj.name)
        elif player_obj.state == "blackjack":
            print "* %s got blackjack! *"%(player_obj.name)
        elif player_obj.stand == True:
            print "* %s is standing! *"%(player_obj.name)
        print INPUT_TEXT['line']

    def draw_round_end(self,players):
        # End the round
        print "++++*****************++++\n       ROUND ENDED\n++++*****************++++"
        for p in players:
            print INPUT_TEXT[p.state]%(p.name,p.points)
        print "+++++++++++++++++++++++++"
        for p in players:
            if p.dealer == False:
                print "%s's balance: $%s"%(p.name,str(p.balance))


class Turn(object):

    t = Table()

    def __init__(self,deck,player):
        self.player = player
        # add condition for double(double bet, take card, stand)
        # add condition for surrender(lose 1/2 bet and forfeit hand)

        # Manual turn for human players
        if self.player.dealer == False:
            self.t.draw_hand(self.player)
            while True:
                if self.player.stand == False:
                    response = raw_input(INPUT_TEXT['hit']%(self.player.name)).upper()
                    if response == "Y":
                        self.player.add_card(deck.deal_card(1))
                        self.t.draw_hand(self.player)
                    elif response == "N":
                        self.player.stand = True
                        break
                else:
                    break
        # Automatic turn for robot dealer
        elif self.player.dealer == True:
            while self.player.points < 17:
                self.player.add_card(deck.deal_card(1))
            else:
                self.player.stand = True
            self.t.draw_hand(self.player)


class Main():

    # Player objects are stored in list
    player = [Player(0,"Dealer",True)]

    def __init__(self):
        self.deck = Deck()
        self.bets = Bet()
        self.t = Table()
        # Set up the players
        self.num_players = 1  # can come back later to add input for multiplayer
        i = 0
        while i < self.num_players:
            name = raw_input(INPUT_TEXT['ask_name']%(i))
            self.player.append(Player(50,name))
            i += 1
        # Move dealer to the end of the list
        self.player += [self.player.pop(0)]
        self.round()
        self.replay()

    def round(self):
        # Start the game
        for p in self.player:
            if p.dealer == True:
                p.add_card(self.deck.deal_card(2))
            else:
                print "Welcome, %s. This is Blackjack. It's a card game." %(p.name)
                # Place bets before rounds begin
                self.bets.place_bet(p)
                self.t.draw_money(p)
                # deal initial 2 cards to players
                p.add_card(self.deck.deal_card(2),True)
        # Play through a round until every player stands
        for p in self.player:
            # only bother with turn player qualifies
            if p.stand == False:
                print p.name + "'s turn..."
                # Perform a player's turn in the game
                Turn(self.deck,p)
                self.t.draw_turn_end(p)
        self.t.draw_round_end(self.player)

    def replay(self):
        # Give option to replay the game
        while True:
            again = raw_input(INPUT_TEXT['replay']).upper()
            if again == "Y":
                for p in self.player:
                    p.clear()
                self.deck.reshuffle()
                self.round()
            else:
                print "Goodbye ... foolish human!"
                break


Main()
