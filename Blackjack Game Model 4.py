import random 

#Blackjack
#   6 Decks 
#   Dealer Stays on all 17
#   Blackjack pays 2-1
#   No Doubling down after splitting
#   Dealer reshuffles after 1/2 deck


#Deck of 52 Cards
deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11]*6
random.shuffle(deck)
#Win - Ties - Loses - Blackjacks - Games
score ={'wins':0,'ties':0,'loses':0,'blackjack':0,'games':0}

#In Case of showdown
def compare(dealer,player,score,double):
    if sum(player) > sum(dealer):
        score['wins'] += 1
        if double == 1:
            score['wins'] += 1
            score['games'] += 1
    if sum(player) == sum(dealer):
        score['ties'] += 1
        score['games'] -= 1
    if sum(player) < sum(dealer):
        score['loses'] += 1
        if double == 1:
            score['loses'] += 1
            score['games'] += 1
                
                        
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

def doubledown(handcards,double):
    handcards.append(deck.pop(0))
    double = 1


def decision(dealer,player,ace):
    #If Dealer's whole card is 6 or less hit until 11 
    if (dealer[1] <= 6):
        lim = 17
        #Unless dealer's whole card is 3 or less, then hit until 12
        if dealer[1] <= 3:
            small = 11
        else:
            small = 12
        while sum(player) <= small:
            handcards = hitmax(player,ace)
        while (sum(player) <= lim and ace == 1):
            handcards = hitmax(player,ace)
            if (sum(player) <= small and ace == 0):
                handcards = hitmax(player,ace)
                
    #If Dealer has more than 6
    if (dealer[1] > 6):
        small = 16
        if dealer[1] >= 9:
            lim = 18
        else:
            lim = 17
        while sum(player) <= small:
            handcards = hitmax(player,ace)
        while (sum(player) <= lim and ace == 1):
            handcards = hitmax(player,ace)
        

#Running Games 
while score['games'] < 10000000:
    score['games'] += 1
    showdown = 1
    showdownS = 1
    ace = 0
    aceS = 0 
    double = 0
    split = 0
    dealer = []
    player = []
    playerS = []
    
    #Reshuffle deck at 2/4 
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
    

    #Splitting
    if (player[0] == player[1] and showdown == 1):
        if (4 <= dealer[1] <= 7 and 4 <= sum(player) <= 6):
            split = 1
        elif (3 <= dealer[1] <= 6 and sum(player) == 12):
            split = 1           
        elif (2 <= dealer[1] <= 7 and sum(player) == 14):
            split = 1
        elif sum(player) == 16:
            split = 1
        elif ((2 <= dealer[1] <= 6 or 8 <= dealer[1] <= 9 ) and sum(player) == 18):
            split = 1         
        elif sum(player) == 22:
            split = 1
    if split == 1:
        playerS.append(player.pop(0))
        player.append(deck.pop(0))
        playerS.append(deck.pop(0))
        if sum(player) == 21:
            score['blackjack'] += 1
            showdown = 0
        if sum(playerS) == 21:
            score['blackjack'] += 1
            score['games'] += 1
            showdownS = 0
        for j in range(len(playerS)):
            if playerS[j] == 11:
                aceS = 1

    #Check if player has an ace, if so, ace flag comes on    
    for i in range(len(player)):
        if player[i] == 11:
            ace = 1

    #Doubling Down if cards have not been split 
    if (split == 0 and showdown == 1):
        if ace == 0:
            if (3 <= dealer[1] <= 6 and sum(player) == 9):
                handcards = doubledown(player,double)
            elif (2 <= dealer[1] <= 9 and sum(player) == 10):
                handcards = doubledown(player,double)
            elif (2 <= dealer[1] <= 10 and sum(player) == 11):
                handcards = doubledown(player,double)
        elif ace == 1:
            if (5 <= dealer[1] <= 6 and 13 <= sum(player) <= 14):
                handcards = doubledown(player,double)
            elif (4 <= dealer[1] <= 6 and 15 <= sum(player) <= 16):
                handcards = doubledown(player,double)
            elif (3 <= dealer[1] <= 6 and 17 <= sum(player) <= 18):
                handcards = doubledown(player,double)    

    #Decision if not doubled down and not split
    if (double == 0 and showdown == 1):
        handcards = decision(dealer,player,ace)
    if (split == 1 and showdownS == 1):
        handcards = decision(dealer,playerS,aceS)
    
    #If Player is above 21 after hitting phase, then player loses
    if (sum(player) > 21 and showdown == 1):
        score['loses'] += 1      
        showdown = 0
        if double == 1:
            score['loses'] += 1
            score['games'] += 1
    if (sum(playerS) > 21 and showdownS == 1):
        score['loses'] += 1
        score['games'] += 1
        showdownS = 0

    #Dealer has to hit if he has 16 or less
    while(sum(dealer) <= 16 and showdown == 1):
        dealercards = hitmax(dealer,0)
                    
    #If Dealer is above 21 after hitting phase, then dealer loses
    if (sum(dealer) > 21):
        if (showdown == 1):
            score['wins'] += 1
            showdown = 0
            if double == 1:
                score['wins'] += 1
                score['games'] += 1
        if (split == 1 and showdownS == 1):
            score['wins'] += 1
            score['games'] += 1
            showdownS = 0
                              
    #If Showdown is still active, then higher sum wins        
    if showdown == 1:   
        showdowncards = compare(dealer,player,score,double)
    if (split == 1 and showdownS == 1):
        showdowncards = compare(dealer,playerS,score,0)
        score['games'] += 1

print('total games - wins and loses:',score['games']-score['wins']-score['loses']-score['blackjack'])
print('wins: ',score['wins']+score['blackjack'],'loses: ',score['loses'],'ties: ',score['ties'])
print('Win Rate:',(1.5*score['blackjack']+score['wins'])/score['games'])
print('Blackjack Count :',score['blackjack'])

