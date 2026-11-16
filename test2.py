import random
import math

RED = "\033[31m"
RESET = "\033[0m"

enemy_types1 = ["Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Pink Slime",
                "Dyna-Dot", "Just A Goob", "Cheese Bro", "Math.png", ]

Gold = 400
TotalGold = 0

def Casino():
    global Gold, TotalGold
    
    # 5 kind, royal flush, straight flush, 4 kind, full house, flush, straight, 3 kind, 2 pair, pair, high card
    # spades beat hearts beat diamonds beat clubs

    def CardCheck(Hand):
        RANK_ORDER = {"A":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13}
        SUIT_ORDER = {"S":1, "H":2, "D":3, "C":4, "J": 5}
        
        suits = {}
        
        Hand.sort(key = lambda card:(RANK_ORDER[card[:-1]], SUIT_ORDER[card[-1]]))
        
        for card in Hand:
            rank = card[:-1]
            suit = card[-1]
            if rank not in suits:
                suits[rank] = set()
            suits[rank].add(suit)
        
        print(str(suits))

        best_hand = 0

        # Pair Check
        for i in range(len(suits)):
            for ij in range(len(suits)):
                if suits.get(i) == suits.get(ij) and i != ij:
                    best_hand = 1
        
        # Two Pair Check
        temp_suits = suits.copy()
        for i in range(len(suits)):
            for ij in range(len(suits)):
                if suits.get(i) == suits.get(ij) and i != ij:
                    temp_suits.pop(i)
                    temp_suits.pop(ij)
        for i in range(len(temp_suits)):
            for ij in range(len(temp_suits)):
                if suits.get(i) == suits.get(ij) and i != ij:
                    best_hand = 2

        # Three of a Kind Check
        for i in range(len(suits)):
            for ij in range(len(suits)):
                for ijk in range(len(suits)):
                    if suits.get(i) == suits.get(ij) == suits.get(ijk) and i != ij and i != ijk and ij != ijk:
                        best_hand = 3

        # Straight Check
        ranks = sorted(RANK_ORDER[rank] for rank in suits)
        for i in range(len(ranks) - 4):
            if ranks[i + 4] - ranks[i] == 4:
                best_hand = 4

        # Flush Check
        ranks = sorted(RANK_ORDER[rank] for rank in suits)
        for i in range(len(ranks) - 4):
            if ranks[i + 4] - ranks[i] == 4:
                best_hand = 4

        if best_hand == 0:
            print("You have a high card.")
        elif best_hand == 1:
            print("You have a pair.")
        elif best_hand == 2:
            print("You have two pair.")
        elif best_hand == 3:
            print("You have three of a kind.")
        elif best_hand == 4:
            print("You have a straight.")
    
    deck = [
        "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", # spades
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", # clubs
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", # hearts
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", # diamonds
        "AJ", "AJ"  # Jokers
    ]

    current_deck = deck

    deck_display = [
        "A♠", "2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "10♠", "J♠", "Q♠", "K♠",
        "A♣", "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "10♣", "J♣", "Q♣", "K♣",
        RED+"A♥"+RESET, RED+"2♥"+RESET, RED+"3♥"+RESET, RED+"4♥"+RESET, RED+"5♥"+RESET, RED+"6♥"+RESET, RED+"7♥"+RESET, RED+"8♥"+RESET, RED+"9♥"+RESET, RED+"10♥"+RESET, RED+"J♥"+RESET, RED+"Q♥"+RESET, RED+"K♥"+RESET,
        RED+"A♦"+RESET, RED+"2♦"+RESET, RED+"3♦"+RESET, RED+"4♦"+RESET, RED+"5♦"+RESET, RED+"6♦"+RESET, RED+"7♦"+RESET, RED+"8♦"+RESET, RED+"9♦"+RESET, RED+"10♦"+RESET, RED+"J♦"+RESET, RED+"Q♦"+RESET, RED+"K♦"+RESET,
        "🃟", RED+"🃟"+RESET
    ]

    card_display = dict(zip(deck, deck_display))

    yourhand = []
    enemy1hand = []
    enemy2hand = []
    benjihand = []
    river = []
    
    enemy1name = ""
    enemy2name = ""
    
    enemy1gold = abs(random.randint(Gold - 100, Gold + 500))
    enemy2gold = abs(random.randint(Gold - 100, Gold + 500))
    benjigold = random.randint(Gold + 500, Gold + 1000)

    enemy1name = random.choice(enemy_types1)
    enemy2name = random.choice(enemy_types1)
    
    pot = 0
    ante = 10
    
    cardsflipped = 5
    
    enemy1gold = round((enemy1gold), -1)
    enemy1gold /= 2
    enemy1gold = int(enemy1gold)
    enemy2gold = round((enemy2gold * 2), -1)
    enemy2gold /= 2
    enemy2gold = int(enemy2gold)
    benjigold = round((Gold * 2), -1)
    benjigold /= 2
    benjigold = int(Gold)

    print("Welcome to the casino!")
    print("Today you will be going up against...")
    input(enemy1name + "!")
    input(enemy2name + "!")
    input("And... Benji! \n")
    
    NewRound = False

    print("Shuffling and dealing cards...")
    random.shuffle(current_deck)
    print("The " + enemy1name + " has " + str(enemy1gold) + " gold.")
    print("The " + enemy2name + " has " + str(enemy2gold) + " gold.")
    print("Benji has " + str(benjigold) + " gold.")
    for i in range(13):
        card = current_deck.pop(0)
        if i <= 1:
            yourhand.append(card)
        elif i <= 3:
            enemy1hand.append(card)
        elif i <= 5:
            enemy2hand.append(card)
        elif i <= 7:
            benjihand.append(card)
        else:
            river.append(card)
    print("Everyone anted " + str(ante) + " gold. \n")
    pot = ante * 4
    Gold -= ante
    enemy1gold -= ante
    enemy2gold -= ante
    benjigold -= ante

    Gold = round((Gold * 2), -1)
    Gold /= 2
    Gold = int(Gold)

    while True:
        print("You have " + str(Gold) + " gold.")
        print("Your hand:", " ".join(card_display[card] for card in yourhand))
        CardCheck(yourhand + river)
        display = []
        for i, card in enumerate(river):
            if i < cardsflipped:
                display.append(card_display[card])
            else:
                display.append("??")
        print("River:", " ".join(display))
        print("Pot: " + str(pot) + " gold\n")
        userinput = input("What will you do? Type 0 to check, any other number to raise (rounded to the nearest 5), and 'fold' to fold. ").lower()
        if userinput == "0":
            print("You checked.")
        elif userinput == "fold":
            print("You folded.")
        else:
            if userinput.isdigit():
                if int(userinput) > 5 and int(userinput) <= Gold:
                    bet = int(userinput)
                    bet = round((bet * 2), -1)
                    bet /= 2
                    bet = int(bet)
                    Gold -= bet
                    pot += bet
                    print("You betted " + str(bet) + " gold.")
                else:
                    print("Input out of range. You can only bet between 5 and " + str(Gold) + " gold. You checked.")
            else:
                print("You checked.")


        
        print()
        if NewRound:
            print("Shuffling and dealing cards...")
            current_deck = deck.copy()
            random.shuffle(current_deck)
            cardsflipped = 0
            yourhand = []
            enemy1hand = []
            enemy2hand = []
            benjihand = []
            river = []
            for i in range(13):
                card = current_deck.pop(0)
                if i <= 1:
                    yourhand.append(card)
                elif i <= 3:
                    enemy1hand.append(card)
                elif i <= 5:
                    enemy2hand.append(card)
                elif i <= 7:
                    benjihand.append(card)
                else:
                    river.append(card)
            print("Everyone anted " + str(ante) + " gold.")
            pot = ante * 4
            Gold -= ante
            enemy1gold -= ante
            enemy2gold -= ante
            benjigold -= ante

Casino()