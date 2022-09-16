import random

#create the deck of cards for each suit, rank, and values.
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
          'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

# class to create the cards
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

#class to create the deck for the cards.
class Deck:
    def __init__(self):
        self.deck = []  
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))  
    
    def __str__(self):
        deck_comp = ''  
        for card in self.deck:
            deck_comp += '\n '+card.__str__() 
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
    # for the dealer to be able to deal the cards to the player, and 
    # take the card out of the deck when dealed.
    def deal(self):
        single_card = self.deck.pop()
        return single_card

test_deck = Deck()
# class to create the hand of the player or dealer.
class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0   
        self.aces = 0   
    #add card to player
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
    
    def adjust_for_ace(self):
        pass
#testing
test_deck = Deck()
test_deck.shuffle()
test_player = Hand()
test_player.add_card(test_deck.deal())
test_player.add_card(test_deck.deal())
test_player.value

for card in test_player.cards:
    print(card)


#class to create the hand of player or dealer when given an ace
class Hand:
    
    def __init__(self):
        self.cards = [] 
        self.value = 0   
        self.aces = 0    
    #this will add a card to  a hand and append the value of the card. 
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  
    #adjust if given an ace
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1 
#class to create the chips for the bets.
class Chips:
    
    def __init__(self):
        self.total = 100  
        self.bet = 0
    #add winning bet to the total
    def win_bet(self):
        self.total += self.bet
    #subtract losing bet from the total 
    def lose_bet(self):
        self.total -= self.bet
#a method to take bets from a player.
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break
#method for when the player hits and is dealt another card. 
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

#method to ask the player if they want to hit or stand on a turn.
def hit_or_stand(deck,hand):
    global playing  
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
#player hits, and is dealt a card
        if x[0].lower() == 'h':
            hit(deck,hand)  
#player stands and move on to dealers turn.
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break
#a method to have the dealer show one card
def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
#show the dealers second card
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
#method to show all of the cards for the dealer and player
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)
#method for when the player goes over 21 and loses the hand
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()
#method for when the player wins the hand and collects its winnings
def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()
#method for when the dealer goes over 21 and loses the hand
def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
#method for when the dealer wins the hand. Player loses bet
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
#method for when the dealer and player tie. No one wins or loses
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")

#START OF THE GAME
while True:
   
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until it reaches 17. Aces count as 1 or 11.')
    
    #create the deck and shuffle it.
    deck = Deck()
    deck.shuffle()
    #adding two cards to the players hand
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    #adding two cards to the dealers hand
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
            
    #create the players chips
    player_chips = Chips()     
    
    #take bet from the player
    take_bet(player_chips)
    
    #show the players cards and the top card of the dealer
    show_some(player_hand,dealer_hand)
    
    while playing:  
        
        #ask the player to hit or stand 
        hit_or_stand(deck,player_hand) 
        
        #show the players cards and the top card of the dealer
        show_some(player_hand,dealer_hand)  
        
        #if players hand value is over 21, then they lose the hand and bet.
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break        


     #if the players hand is under or equal to 21
    if player_hand.value <= 21:
        #while the dealers hand is under 17, dealer will take another card 
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)    
    
       #player and dealer will show their cards.
        show_all(player_hand,dealer_hand)
        
        #If dealers hand is over 21, they bust and player wins.
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        #If dealers hand is greater then the players hand while being under 21, dealer wins. 
        #player loses bet.
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        #If players hand is greater than the dealers hand while being under or equal to 21, 
        #player wins and wins bet. 
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        #Dealer and player hands are equal. No one wins nor loses. 
        else:
            push(player_hand,dealer_hand)        

    print("\nPlayer's winnings stand at",player_chips.total)
    
   #Start a new game
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break
