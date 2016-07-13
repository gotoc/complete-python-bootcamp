# https://github.com/jmportilla/Complete-Python-Bootcamp/blob/master/Milestone%20Project%202%20-%20Assignment.ipynb
# Milestone Project 2 - Blackjack Game

import random

INPUT_TEXT = {  'line':"-------------------------",
                'line2':"+++++++++++++++++++++++++",
                'welcome':"Welcome to the game, %s.", # player.name
                'ask_name':"Hello, Player %s. Please enter your name: ", # num_players
                'ace':"Would you like your Ace to count for 1 or 11 points? Enter 1 or 11: ",
                'bet':"%s, please enter a bet between 1 and %s: ", # player.name, player.balance
                'hit':"%s, would you like a hit? Y or N: ", # player.name
                'over':"%s busts with %s points.", # player.name, player.points
                'under':"%s stood with %s points.", # player.name, player.points
                'blackjack':"%s reached %s points.", # player.name, player.points
                'balance':"%s's balance: $%s", # player.name, player.balance
                'zero_balance':"Unfortunately, you have a balance of $0, so the game must end.",
                'replay':"Do you want to play again? (y or n): ",
                'goodbye':"Goodbye ... foolish human!\n\n"
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
        '''Add amount to the balance.'''
        self.balance += amount

    def sub_balance(self,amount):
        '''Subtract amount from the balance.'''
        self.balance -= amount


class Deck(object):

    suit = ['H','D','S','C']
    rank = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    def __init__(self):
        '''Build the deck of cards as list of tuples and shuffle.'''
        self.deck = []
        for s in self.suit:
            for r in self.rank:
                self.deck.append((s,r))
        random.shuffle(self.deck)

    def reshuffle(self):
        '''Reset the cards in the deck.'''
        self.__init__()

    def deal_card(self,amount=1):
        '''Gets amount of random cards from deck and delete them there. Return list of cards.'''
        cards = []
        i = 1
        while i <= amount:
            cards.append(self.deck.pop(0))
            i += 1
        return cards


class Points(object):

    def __init__(self, dealer=False):
        self.points = 0
        self.dealer = dealer

    def set_points(self,cards,auto_ace=False):
        '''Adds points to total based on cards inputted. auto_ace is a simple AI for selecting value of Ace.'''
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
        # The player's name.
        self.name = name
        # List of tuples representing cards dealt to player
        self.hand = []
        # Total money the player wishes to bet on a turn
        self.bet = 0
        # Values "under" - player can still play, "over" - player has busted, "blackjack" - player scored 21 points
        self.state = "under"
        # If true, the players turn is ended
        self.stand = False
        # If true, the player doesn't see a welcome message.
        self.intro = False

    def add_card(self,cards,auto_ace=False):
        '''Add an amount of cards to the player's hand.'''
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
        '''Reset all non-persistent values for the player.'''
        del self.hand[:]
        self.bet = 0
        self.points = 0
        self.state = "under"
        self.stand = False


class Bet(object):

    def place_bet(self,player):
        '''Asks for bet amount and sets player objects bet total.'''
        if player.dealer == False and player.balance > 0:
            while True:
                try:
                    the_bet = int(raw_input(INPUT_TEXT['bet']%(player.name,str(player.balance))))
                    if the_bet >= 1 and the_bet <= player.balance:
                        player.bet = the_bet
                        break
                except:
                    continue
            return True
        else:
            print "You don't have enough money left. Sorry!"
            return False

    def settle_bet(self,player,condition):
        '''Adds or subtracts bet from player object's balance and resets bet to 0.'''
        if condition == 'W':
            player.balance = player.bet + player.balance
        elif condition == "L":
            player.balance = player.balance - player.bet
        player.bet = 0


class Table(object):

    def draw_hand(self, player_obj):
        '''Output the player's hand of cards.'''
        cards = []
        for c in player_obj.hand:
            s,r = c
            cards.append(CARD_TEXT[str(r)] + " of " + CARD_TEXT[s])

        print INPUT_TEXT['line']
        print "%s's hand: "%(player_obj.name),cards
        print "Hand's point-worth: ",player_obj.points
        print INPUT_TEXT['line']

    def draw_money(self, player_obj):
        '''Output the player's balance and current bet.'''
        print INPUT_TEXT['line']
        print "%s's current bet: $%s"%(player_obj.name,str(player_obj.bet))
        print "%s's balance: $%s"%(player_obj.name,str(player_obj.balance))
        print INPUT_TEXT['line']

    def draw_turn_end(self,player_obj):
        '''Output the information for the end of a turn.'''
        if player_obj.state == "over":
            print "* %s busted! *"%(player_obj.name)
        elif player_obj.state == "blackjack":
            print "* %s got blackjack! *"%(player_obj.name)
        elif player_obj.stand == True:
            print "* %s is standing! *"%(player_obj.name)
        print INPUT_TEXT['line']

    def draw_welcome(self,player_obj):
        print INPUT_TEXT['line2']
        if player_obj.dealer == False:
            print INPUT_TEXT['welcome']%(player_obj.name)
        print INPUT_TEXT['line2']

    def draw_round_end(self,players):
        '''Output the information for the end of a round.'''
        # End the round
        print INPUT_TEXT['line2']
        print "     ROUND OVER!"
        print INPUT_TEXT['line2']
        print INPUT_TEXT['line']
        for p in players:
            print INPUT_TEXT[p.state]%(p.name,p.points)
        print INPUT_TEXT['line']
        for p in players:
            if p.dealer == False:
                print INPUT_TEXT['balance']%(p.name,str(p.balance))
        print INPUT_TEXT['line2']

class Game(object):

    deck = Deck()
    bets = Bet()
    t = Table()
    balance_alert = False

    def __init__(self,players):
        self.player = players
        self.round()
        if self.balance_alert == False:
            self.replay()
        else:
            self.exit_game()

    def round(self):
        '''A sequence of player turns.'''
        # Start the game
        for p in self.player:
            if p.dealer == True:
                p.add_card(self.deck.deal_card(2))
            else:
                if p.intro == False:
                    self.t.draw_welcome(p)
                # Place bets before rounds begin
                self.bets.place_bet(p)
                self.t.draw_money(p)
                # deal initial 2 cards to players
                p.add_card(self.deck.deal_card(2),True)
                self.t.draw_hand(p)
        # Play through a round until every player stands
        for p in self.player:
            # only bother with turn player qualifies
            if p.stand == False:
                # Perform a player's turn in the game
                self.turn(p)
                self.t.draw_turn_end(p)
        self.outcome()
        self.t.draw_round_end(self.player)

    def outcome(self):
        '''Determines the winner(s) and loser(s) of the round.'''
        for p in self.player:
            # dealer has no balance so not worth checking
            if p.dealer == False:
                # Player always loses on bust regardless of dealer hand.
                if p.state == "over":
                    self.bets.settle_bet(p,"L")
                # Player wins unless dealer also has 21, in which case it's a tie.
                elif p.state == "blackjack":
                    if p.points > self.player[-1].points:
                        self.bets.settle_bet(p,"W")
                    elif p.points < self.player[-1].points and self.player[-1].points > 21:
                        self.bets.settle_bet(p,"W")
                    elif p.points == self.player[-1].points:
                        self.bets.settle_bet(p,"T") #Tie
                # If under 21, player wins when higher than dealer or dealer busts, loses when lower, and ties when the same.
                elif p.state == "under":
                    if p.points > self.player[-1].points:
                        self.bets.settle_bet(p,"W")
                    elif p.points < self.player[-1].points and self.player[-1].points > 21:
                        self.bets.settle_bet(p,"W")
                    elif p.points == self.player[-1].points:
                        self.bets.settle_bet(p,"T") #Tie
                    else:
                        self.bets.settle_bet(p,"L")
                # Prevent player with zero balance from playing without restarting
                if p.balance == 0:
                    self.balance_alert = True

    def exit_game(self):
        '''Exits the game.'''
        if self.balance_alert == True:
            print INPUT_TEXT['zero_balance']
        else:
            print INPUT_TEXT['goodbye']

    def replay(self):
        '''Asks the player if they would like to play another round.'''
        # Give option to replay the game
        while True:
            again = raw_input(INPUT_TEXT['replay']).upper()
            print INPUT_TEXT['line']
            if again == "Y":
                for p in self.player:
                    p.clear()
                    p.intro = True
                self.deck.reshuffle()
                self.__init__(self.player)
                break
            else:
                self.exit_game()
                break

    def turn(self,player):
        '''Processes a specific player's turn within the game round.'''
        # add condition for double(double bet, take card, stand)
        # add condition for surrender(lose 1/2 bet and forfeit hand)
        # Manual turn for human players
        if player.dealer == False:
            while True:
                if player.stand == False:
                    response = raw_input(INPUT_TEXT['hit']%(player.name)).upper()
                    print INPUT_TEXT['line']
                    if response == "Y":
                        player.add_card(self.deck.deal_card(1))
                        self.t.draw_hand(player)
                    elif response == "N":
                        player.stand = True
                        break
                else:
                    break
        # Automatic turn for robot dealer
        elif player.dealer == True:
            while player.points < 17:
                player.add_card(self.deck.deal_card(1))
            else:
                player.stand = True
            self.t.draw_hand(player)


class Main():
    # Player objects are stored in list, add dealer.
    players = [Player(0,"Dealer",True)]

    def __init__(self):
        '''The main class for initializing the game.'''
        # Set up the players
        self.num_players = 1  # can come back later to add input for multiplayer
        i = 0
        while i < self.num_players:
            name = raw_input(INPUT_TEXT['ask_name']%(i+1))
            # Create a new player object and add to the list.
            self.players.append(Player(50,name))
            i += 1
        # Move dealer to the end of the list
        self.players += [self.players.pop(0)]
        # Start the game.
        Game(self.players)


Main()
