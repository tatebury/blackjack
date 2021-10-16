from random import randint
from random import choice
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class BlackJack():
    def __init__(self):
        # the deck-->keys help construct the card name and 
        # values tell whether the card has been used or not (0==used)
        self.deck = {'c 1':1,'c 2':2,'c 3':3,'c 4':4,'c 5':5,'c 6':6,'c 7':7,'c 8':8,'c 9':9,'c 10':10,'c 11':11,'c 12':12,'c 13':13,
                     'd 1':1,'d 2':2,'d 3':3,'d 4':4,'d 5':5,'d 6':6,'d 7':7,'d 8':8,'d 9':9,'d 10':10,'d 11':11,'d 12':12,'d 13':13,
                     'h 1':1,'h 2':2,'h 3':3,'h 4':4,'h 5':5,'h 6':6,'h 7':7,'h 8':8,'h 9':9,'h 10':10,'h 11':11,'h 12':12,'h 13':13,
                     's 1':1,'s 2':2,'s 3':3,'s 4':4,'s 5':5,'s 6':6,'s 7':7,'s 8':8,'s 9':9,'s 10':10,'s 11':11,'s 12':12,'s 13':13}


        self.player_cards = []
        self.player_total = 0
        self.dealer_cards = []
        self.dealer_total = 0
        
        self.game_on = False
        
        
    # start-->print the starting text, 
    # deal each player two cards and print both the player's cards and one of the dealer's
    def start(self):
        print("\nOptions: 'hit', 'stand', 'quit', 'clear', or 'rules' ")
        self.player_cards.append(self.deal_card())
        self.player_cards.append(self.deal_card())
        self.dealer_cards.append(self.deal_card())
        self.dealer_cards.append(self.deal_card())
        for playercard in self.player_cards:
            try:
                self.player_total += int(playercard[:2])
            except:
                if playercard[:3]=='Ace':
                    self.player_total += 1
                else:
                    self.player_total += 10 
        for dealercard in self.dealer_cards:
            try:
                self.dealer_total += int(dealercard[:2])
            except:
                if dealercard[:3]=='Ace':
                    self.dealer_total += 1
                else:
                    self.dealer_total += 10 
        
        print(f"\nThe dealer's second card is the {self.dealer_cards[1]}")
        print(f"You have the {self.player_cards[0]} and {self.player_cards[1]}\n")
        self.check_score(round_end=False)
        self.play()


    # play-->ask the player for their desired action and do that.
    def play(self):
        self.game_on=True
        round_end = False
        while self.game_on==True:
            action = input("What would you like to do? ").lower().strip()
            
            if action=='hit':
                card_drawn = self.hit()
                print(f"You drew the {card_drawn}")
                try:
                    self.player_total += int(card_drawn[:2])
                except:
                    if card_drawn[:3]=='Ace':
                        self.player_total += 1
                    else:
                        self.player_total += 10 
                print(f"Your total is now {self.player_total}")
                if self.player_total == 21:
                    self.stand()
                    self.check_score(round_end=True)
                elif self.player_total > 21:
                    self.check_score(round_end=True)
            elif action=='stand':
                for playercard in self.player_cards:
                    if playercard[:3]=='Ace':
                        acemode = input("Do you want to count your ace as 11?(enter 'y'/'n') ").lower().strip()
                        if acemode=='y':
                            self.player_total += 10
                total = self.stand()
                print(f"Dealer total is {total}")
                round_end = True
                self.check_score(round_end)
            elif action=='quit':
                self.game_on = False
                break
            elif action=='clear':
                clear_screen()
            elif action=='rules':
                self.rules()
            else:
                print("Command not recognized")
            
                      
            
    # check_score-->check if the game is over, if so print the appropriate ending, 
    # refill the deck and ask the player if they want to play again.
    def check_score(self, round_end):
        
        if round_end==True or self.player_total >= 21:
            self.game_on = False
            if self.player_total != self.dealer_total:
                if self.player_total==21:
                    print("BlackJack! You win.")
                elif self.player_total<21 and self.player_total > self.dealer_total:
                    print("Congrats, you win.")
                elif self.player_total > 21:
                    print("Bust. Better luck next time.")
                elif self.dealer_total<=21:
                    print("Dealer wins. Try again.")
                else:
                    print("Dealer bust, you win.")
            else:
                if self.player_total==21:
                    print("Stalemate. 21 all.")
                else:
                    print("Stalemate.")
            self.refill_deck()
            play_again = input("Play again? (enter 'y'/'n') ").lower().strip()
            if play_again=='y':
                self.start()
                
            
    # hit-->basically just calls deal card, totally neccesary.
    def hit(self):
        new_card = self.deal_card()
        self.player_cards.append(new_card)
        return new_card

    # stand-->called when the player chooses to stand (crazy right?) 
    # first tells the dealer whether to hit and how many times, 
    # then adds up the dealer total and returns it
    def stand(self):
        print(f"Dealer has {self.dealer_cards[0]} and {self.dealer_cards[1]}")
        for dealercard in self.dealer_cards:
            if dealercard[:3]=='Ace':
                if self.dealer_total > 6 and self.dealer_total < 12:
                    self.dealer_total += 10
                    print("Dealer counted ace as 11")
        while self.dealer_total < 17: # change this number to affect the dealer's playstyle
            new_card = self.deal_card()
            self.dealer_cards.append(new_card)
            try:
                self.dealer_total += int(new_card[:2])
            except:
                if new_card[:3]=='Ace':
                    self.dealer_total += 1
                    if self.dealer_total > 6 and self.dealer_total < 12:
                        self.dealer_total += 10
                        print("Dealer counted ace as 11")
                else:
                    self.dealer_total += 10 
            print(f"Dealer hit and drew {new_card}.")
        return self.dealer_total
            
    # rules-->prints rules.
    def rules(self):
        print("\nRules of BlackJack: ")
        print("1. Closest to 21 without going over wins")
        print("2. Numbered cards have the value of their number, \n   Face cards are worth 10 and Aces can be 1 or 11")
        print("3. Dealer has to hit while under 17 and stand otherwise.")
        print("4. If counting an Ace as 11 puts the dealer at or above 17 and \n   not over 21, the dealer must do it.\n")

    # deal_card-->creates a random key until it finds one that hasn't been played, 
    # then converts it to a goodlooking card name and returns the card name.
    def deal_card(self):
        card = ''
        while card=='':
            suit_letter = choice('cdhs')
            num = randint(1,13)
            
            random_key = f"{suit_letter} {num}"
            if self.deck[random_key]!=0:
                if suit_letter=='c':
                    suit = 'Clubs'
                elif suit_letter=='d':
                    suit = 'Diamonds'
                elif suit_letter=='h':
                    suit = 'Hearts'
                else:
                    suit = 'Spades'
                    
                self.deck[random_key] = 0
                if num > 10:
                    if num==11:
                        num = 'Jack'
                    elif num==12:
                        num = 'Queen'
                    elif num==13:
                        num = 'King'
                elif num==1:
                    num = 'Ace'
                card = f"{num} of {suit}"
        
        return card

    # refill_deck-->resets totals, hands and each card in the deck to unused.
    def refill_deck(self):
        self.player_cards = []
        self.player_total = 0
        self.dealer_cards = []
        self.dealer_total = 0
        for k,v in self.deck.items():
            if v==False:
                self.deck[k] = int(k[-2:])
        

        
        
BlackJack().start()