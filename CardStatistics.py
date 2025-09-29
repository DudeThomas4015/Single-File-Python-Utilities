import random

Cardbank = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Joker']
Type = ['Hearts', 'Spades', 'Diamonds', "Clubs"]

def drawCard():
    x = random.choice(Cardbank)
    y = " of " + str(random.choice(Type))
    if x == "Joker":
        y = ""
    return x,y

def pickACard():
    x,y = drawCard()
    print(f"Your card is the {x}{y}")
    return

def jokerLuck():
    x = "null"
    i = 0
    while x != "Joker":
        i += 1
        x,y = drawCard()
        print(f"{x}{y}")
    print(f"It took {i} tries to draw a joker!")

def shuffle():
    CardList = []
    i = 0
    while len(CardList) < 54:
        x,y = drawCard()
        NewCard = (str(x) + str(y))
        if NewCard not in CardList and x != "Joker":
            CardList.append(NewCard)
        elif x == "Joker" and i < 2:
            CardList.append(NewCard)
            i += 1
    print(CardList)
    
def main():
    x = input("What would you like to do?\n    1 - Draw a random card\n    2 - Draw Cards until you pull a Joker\n    3 - Shuffle a deck of cards\n")
    print("\n")
    if x == "1":
        pickACard()
    elif x == "2":
        jokerLuck()
    elif x == "3":
        shuffle()
    else:
        print("Sorry that's not a valid response")


main()