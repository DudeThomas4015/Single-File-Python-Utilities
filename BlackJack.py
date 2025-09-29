import random

# Define the card values and suits
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Define the deck class
class Deck:
    def __init__(self):
        self.deck = [(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Define the hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card[0]]
        if card[0] == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Define the functions for gameplay
def take_bet():
    while True:
        try:
            bet = int(input("How much would you like to bet? "))
        except ValueError:
            print("Sorry, a bet must be an integer!")
        else:
            if bet > 0:
                return bet
            else:
                print("Bet must be greater than zero!")

def hit(deck, hand):
    hand.add_card(deck.deal())

def hit_or_stand(deck, hand):
    global playing
    while True:
        choice = input("Would you like to Hit or Stand? Enter 'h' or 's': ")
        if choice[0].lower() == 'h':
            hit(deck, hand)
        elif choice[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips -= bet
    return chips

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips += bet
    return chips

def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips += bet
    return chips

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips -= bet
    return chips

def push(player, dealer):
    print("Dealer and Player tie! It's a push.")

# Main game logic
playing = True

while True:
    print("Welcome to Blackjack!")

    # Create and shuffle the deck, deal two cards to each player
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    chips = 100  # Starting chips
    bet = take_bet()

    show_some(player_hand, dealer_hand)

    while playing:  # Recall this variable from our hit_or_stand function
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            chips = player_busts(player_hand, dealer_hand, chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            chips = dealer_busts(player_hand, dealer_hand, chips)
        elif dealer_hand.value > player_hand.value:
            chips = dealer_wins(player_hand, dealer_hand, chips)
        elif dealer_hand.value < player_hand.value:
            chips = player_wins(player_hand, dealer_hand, chips)
        else:
            push(player_hand, dealer_hand)

    print("\nPlayer's total chips:", chips)

    new_game = input("Would you like to play another hand? Enter 'y' or 'n': ")
    if new_game[0].lower() == 'n':
        print("Thanks for playing!")
        break
    else:
        playing = True
