'''
- a famous card game -- driving a train;
- two players, the one with no card in hand loses;
'''

# random lib for shuffling cards
import random

# introduce game rules
def intro():
    global operation
    statement = '''Welcome to Driving a Train! This game starts between
    two players, each initially with 27 cards in hand. Each player has to 
    play with his/her top card for each round. If someone’s card number is 
    the same as a card shown before, he/she can take all the cards start from
    that card. The game continues until one player has no card in hand.'''

    print(statement)
    print('Press s to start the game!')
    

#--------------------------------------------#
## Creating card set & dividing up cards to two players

# Hearts, Diamonds, Clubs, Spades
card_suits = ('H','D','C','S')

# Card ranks
card_ranks = ('3','4','5','6','7','8','9','10','J','Q','K','A','2')
special_cards = ('BJ','RJ') # Black Joker & Red Joker

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def show_card(self):
        return(self.suit + self.rank)

class Deck:

    # create a deck of 54 cards
    def __init__(self):
        self.deck = []
        for suit in card_suits:
            for rank in card_ranks:
                self.deck.append(Card(suit, rank))
        for scard in special_cards:
            self.deck.append(Card('', scard))
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        first_player_cards = self.deck[:27]
        second_player_cards = self.deck[27:]
        return (first_player_cards, second_player_cards)


#--------------------------------------------#
## Two players checking their own cards in hand

class Hand:

    # each player has two cardsets
    # one for current round
    # the other save cards assigned to the player due to duplications
    # the save set isn't used until there is no card in the current set
    def __init__(self):
        self.cards = [] # current round
        self.save_cards = [] # saved for next round

    # player can only play the last card in card set
    def play(self):
        new_card = self.cards.pop()
        return new_card
    
    # methods for adding cards to two sets
    def add_cards(self, cardset):
        self.cards += cardset

    def add_save_cards(self, cardset):
        self.save_cards += cardset
    
    # method for deleting save set after it replaces the current set
    def delete_save_cards(self):
        self.save_cards = []
    
    # make the card set random again
    def shuffle(self, cardset):
        random.shuffle(cardset)

    # methods for the program to get two card sets' info
    def get_cards(self):
        return self.cards

    def get_num_cards(self):
        return len(self.cards)

    def get_save_cards(self):
        return self.save_cards

    # get the amount of cards in each set and the total amount
    def total_cards(self):
        num_this = len(self.cards)
        num_next = len(self.save_cards)
        total = len(self.cards + self.save_cards)
        return '''The hand has %s cards in total now,
        with %s cards in this round
        and %s cards saved for the next round.''' % (total, num_this, num_next)


#--------------------------------------------#
## Starting the game

class Playboard:

    def __init__(self):
        self.playboard = []
        self.playboard_rank = [] # save card numbers
    
    def update_playboard(self, new_card):
        self.playboard.append(new_card)
        self.playboard_rank.append(new_card.get_rank())

    # check if the player has a card num that appeared before
    def assign_cards(self, new_card):

        add_cardset = []

        if new_card.get_rank() in self.playboard_rank:
            # duplicative card: card num equals to this card
            # get the index of the duplicative card on the playboard
            index = self.playboard_rank.index(new_card.get_rank())
            
            # assign all cards start from the duplicative card to the set
            add_cardset = self.playboard[index:]

            # get the amount of cards added to 
            num_add = len(add_cardset)

            # update playboard & playboard rank
            self.playboard = self.playboard[:index]
            self.playboard_rank = self.playboard_rank[:index]

            print('''The card %s has the same number as a card 
        already on playboard, so the player is assigned %d cards.''' % (new_card.show_card(),num_add))

        else:
            print("The card number has no duplications.")
        return add_cardset


def main():

    global playing

    # starting the game
    intro()
    operation = input() # enter s to start game
    if operation != 's':
        print('Invalid input, please enter s to start.')
        return

    # creating a deck of cards and shuffle it
    deck = Deck()
    deck.shuffle()

    # creating a playboard
    playboard = Playboard()

    # creating two players
    real_player = Hand()
    robot_player = Hand()

    # deal cards to 2 players
    cardsets = deck.deal_cards()
    real_player.add_cards(cardsets[0])
    # retrieve cardset for real player
    real_card = real_player.get_cards()
    robot_player.add_cards(cardsets[1])
    # retrieve cardset for robot player
    robot_card = robot_player.get_cards()

    # start playing
    print("Press p to play a card or q to quit.")
    while(real_card != None and robot_card != None):

        playing = input()
        
        if playing == 'q':
            print("Thanks for playing!")
            exit()

        if playing == 'p':

            ## Real Player(You!)
            print('')
            # pop the last card in the card set
            cur_card = real_player.play()
            print("You play a card:", cur_card.show_card())

            # check if this card num has duplicate on playboard
            # if no duplicates the addset will be zero
            add_cardset1 = playboard.assign_cards(cur_card)
            real_player.add_save_cards(add_cardset1)

            # update real_player's info on playboard
            playboard.update_playboard(cur_card)

            # show total cards left for real_player & specific num for each set
            print(real_player.total_cards())

            # for replacing the empty card set with the save set
            if real_player.get_num_cards() == 0:
                real_saveset = real_player.get_save_cards()
                real_player.add_cards(real_saveset)
                real_player.delete_save_cards()
                real_player.shuffle(real_card)

            ## Robot Player
            print('')
            # pop the last card in the card set
            auto_card = robot_player.play()
            print("The robot plays a card:", auto_card.show_card())

            # check if this card num has duplicate on playboard
            # if no duplicates the addset will be zero
            add_cardset2 = playboard.assign_cards(auto_card)
            robot_player.add_save_cards(add_cardset2)

            # update robot_player's info on playboard
            playboard.update_playboard(auto_card)

            # show total cards left for robot_player & specific num for each set
            print(robot_player.total_cards())

            # for replacing the empty card set with the save set
            if robot_player.get_num_cards() == 0:
                robot_saveset = robot_player.get_save_cards()
                robot_player.add_cards(robot_saveset)
                robot_player.delete_save_cards()
                robot_player.shuffle(robot_card)

            print('')
            print("------------New Round------------")
            print("Press p to play the next card or q to quit.")

        else:
            print("Invalid input, please enter p to continue playing or q to quit.")
            playing = input()
    
    if real_card == None and robot_card != None:
        print("You lose! You have no card left.")
    elif real_card != None and robot_card == None: 
        print("You win! The robot has no card left.")  
    else:
        print("Tied! Both of you have no card left.")

if __name__ == '__main__' :
    main()
