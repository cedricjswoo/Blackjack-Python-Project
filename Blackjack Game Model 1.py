import random 

#Blackjack
#   6 Decks
#   Dealer Stays on all 17
#   Blackjack pays 2-1
#   No Splitting
#   No Doubling Down
#   Dealer reshuffles at 1/2 deck


#Deck of 52 Cards
deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11]*6
random.shuffle(deck)
#Dealer & Player Hands
dealer = []
player = []
#Counters
#Win - Ties - Loses - Blackjacks - Games
#Dictionary
score ={'wins':0,'ties':0,'loses':0,'blackjack':0,'games':0}



#In Case of showdown
class showdowns:
    def __init__(self,dealercards,playercards,score):
        self.dealer = dealercards
        self.player = playercards
        self.score = score
    def compare(self):
        if sum(self.player) > sum(self.dealer):
            self.score['wins'] += 1 
        if sum(self.player) == sum(self.dealer):
            self.score['ties'] += 1
            self.score['games'] -= 1
        if sum(self.player) < sum(self.dealer):
            self.score['loses'] += 1


def hitmax(handcards,ace):
    handcards.append(deck.pop(0))
    if handcards[len(handcards)-1] == 11:
        ace = 1
    if sum(handcards) > 21:
        if handcards[len(handcards)-1] == 11:
            handcards[len(handcards)-1] = 1
        else:
            for i in range (len(handcards)):
                if handcards[i] == 11:
                    handcards[i] = 1
                    ace = 0

#Running Games 
while score['games'] < 100000:
    score['games'] += 1
    showdown = 1
    ace = 0
    

    if len(deck) <= 156:
        deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11]*6
        random.shuffle(deck)
    

    #Player & Dealers Draw 
    dealer.append(deck.pop(0))
    dealer.append(deck.pop(0))
    player.append(deck.pop(0))
    player.append(deck.pop(0))

    #If Dealer gets blackjack, then game ends 
    if sum(dealer) == 21:
        showdown = 0
        #Unless player also has blackjack,
        if sum(player) == 21:
            score['ties'] += 1
            score['games'] -= 1
        else:
            score['loses'] += 1

    #If Player gets blackjack when Dealer does not, then game ends
    if (sum(player) == 21 and showdown == 1):
        score['blackjack'] += 1
        showdown = 0
    

    #Check if player has an ace, if so, ace flag comes on    
    for i in range(len(player)):
        if player[i] == 11:
            ace = 1

    #If Both Initial Cards are Ace, first ace will be turned to 1
    if sum(player) > 21:
        player[0] = 1
    if sum(dealer) > 21:
        dealer[0] = 1
       
    #If Dealer's whole card is 6 or less hit until 11 
    if dealer[1] <= 6:
        while sum(player) <= 11:
            handcards = hitmax(player,ace)
        while (sum(player) <= 17 and ace == 1):
            handcards = hitmax(player,ace)
            
    #If Dealer has more than 6
    if dealer[1] > 6:
        while sum(player) <= 16:
            handcards = hitmax(player,ace)


    #If Player is above 21 after hitting phase, then player loses   
    if (sum(player) > 21 and showdown == 1):
        score['loses'] += 1
        showdown = 0
   
    #Dealer has to hit if he has 16 or less
    while(sum(dealer) <= 16 and showdown ==1):
        dealercards = hitmax(dealer,0)
                    
    #If Dealer is above 21 after hitting phase, then dealer loses
    if (sum(dealer) > 21 and showdown ==1):
        score['wins'] += 1 
        showdown = 0

    #If Showdown is still active, then higher sum wins        
    if showdown == 1:   
        showdowncards = showdowns(dealer,player,score)
        showdowncards.compare()

    #Reset Hands
    dealer = []
    player = []

print('total games - wins and loses:',score['games']-score['wins']-score['loses']-score['blackjack'])
print('wins: ',score['wins']+score['blackjack'],'loses: ',score['loses'],'ties: ',score['ties'])
print('Win Rate:',(1.5*score['blackjack']+score['wins'])/score['games'])
print('Blackjack Count :',score['blackjack'])

