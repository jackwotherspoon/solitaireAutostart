#CMPE 365 Solitaire Autostart Project
# Author: Jack Wotherspoon
# Created: Nov 1, 2018

#to be used for shuffling
import random
import copy
#to see runtime of program
import time

#suits and values in a standard deck of cards
suits = ['Hearts','Diamonds','Spades','Clubs']
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
#constants as specified in question
k = 2 #number of decks used (52 cards per deck)
n = 10 #number of starting piles of cards
m = 4  #number of cards on each starting pile
p = 8  #number of end piles that we are sorting cards onto

#maximum of cards in an end pile, can be max 13 for this scenario (one suit)
maxCards = len(values)
# global variables required
cards = [] #blank array to insert all cards into
#create the start and end piles blank so that cards can be shuffled and then dealt
stPiles = [[None for x in range(m)] for y in range(n)] #Starting piles of playable cards
finPiles = [[None for x in range(maxCards)] for y in range(p)] #finished piles (acePiles) that are sorted from lowest to highest

#Card-creates simple playing card with suit and rank
class Card(object):
    #initialization of and setting up of variables
    def __init__(self, suit, value):
        self.value = value
        self.suit = suit

    #function to show information of card
    def show(self):
        print(self.value, "of", self.suit)

    #return show information as a string
    def Info(self):
        return self.value + " of " + self.suit

#class that creates tree of all possible
class Branch(object):
    # initialization of Branch
    def __init__(self, Ca, depth, startPiles=[], acePiles=[]):
        self.card=Ca
        #blank lists to allow in making branches (clones) of current branch
        nextC = []
        topC = []
        theChildren = []

        #Deep copies of many variables for the Branch class. Deep copy creates clone that is now seperate entity from original.
        #Allows for us to move different cards at the same step and see which move was better and thus branch back to this copy and continue.
        #These were the only way I could get my branch and bound to properly work.
        self.children = copy.deepcopy(theChildren)
        self.startPiles = copy.deepcopy(startPiles)
        self.acePiles=copy.deepcopy(acePiles)
        self.depth = copy.deepcopy(depth)
        self.nextDepth = copy.deepcopy(depth+1)
        self.nextCards = copy.deepcopy(nextC)
        self.topCards = copy.deepcopy(topC)

        c1 = Card('blank', 'blank')
        for i in range(0, len(self.startPiles)):
            if len(self.startPiles[i]) > 0:
                # if there are still cards in the start pile, add them to the list
                self.topCards.append(self.startPiles[i][0])
            else:
            # if not, add a blank card as a placeholder so indexing doesn't get messed up
                self.topCards.append(c1)
        for i in range(0, p):
            if (self.acePiles[i][0] != None):
                # if there is a card that has already been played on the pile
                active = self.acePiles[i][0]
                # suit remains the same
                theSuit = active.suit
                anum = active.value
                # get index of previous value
                newNum = nextCard(anum)
                if newNum > 12:
                    theValue = 'X'  # can't have anything higher than a king (index 12)
                #get index of next required value
                else:
                    theValue = values[newNum + 1]
                # create this 'necessary' card, and then add it to the list of cards that are needed
                newCard = Card(theSuit, theValue)
                self.nextCards.append(newCard)
            else:
                theValue = 'A'  # aces start piles
                theSuit = 'W'  # wild, suit doesn't matter, can put ace on any end pile
                # create this 'necessary' card, and then add it to the list of cards that are needed
                newCard = Card(theSuit, theValue)
                self.nextCards.append(newCard)

    #make children (find all possibilities that can be played from Branch)
    def createChildren(self):
        startCount = 0
        #outer loop - iterating through the cards at the top of the starting piles
        while (startCount < len(self.startPiles)):
            found = 0
            eCount = 0
            #inner loop - iterating through the cards that need to be put on top of the ace piles
            while (eCount < len(self.acePiles) and found == 0):
                #look at each pairing of cards
                c1=self.topCards[startCount]
                c2=self.nextCards[eCount]
                #see if they are identical matches using separate function
                found = match(c1,c2)
                #if there's a match, create a child, with increased depth
                if found == 1:
                    #copy the starting and ace piles, except moving the card that will be moved.
                    self.startPilesCopy = copy.deepcopy(self.startPiles)
                    self.acePilesCopy = copy.deepcopy(self.acePiles)
                    self.acePilesCopy[eCount].insert(0, self.startPiles[startCount][0])
                    self.startPilesCopy[startCount].pop(0)
                    #create the Branch
                    n1 = Branch(self.startPiles[startCount][0], self.nextDepth, self.startPilesCopy, self.acePilesCopy)
                    #add it to the master list of the Branch's children
                    self.children.append(n1)
                eCount +=1
            startCount += 1

    #returns all children that the Branch made
    def getChildren(self):
        return self.children

    # prints out the status of the start and end piles. mostly used for testing accuracy
    def showPiles(self):
        count = 0
        # prints the starting piles
        print("Starting piles:")
        while (count < n):
            # as long as there are cards in the pile, print the top one
            if len(self.startPiles[count]) > 0:
                active=self.startPiles[count][0]
                # print the top card information
                print("Starting Pile", count + 1, ": ", active.Info())
            else:
                print("Starting Pile", count + 1, ": empty.")
            count += 1
        count = 0
        # prints the Ace piles
        print("Ace piles:")
        while (count < p):
            # same as the start piles, if there are cards on the pile print the information
            if self.acePiles[count][0] != None:
                print("Ace Pile", count + 1, ": ", self.acePiles[count][0].Info())
            else:
                print("Ace Pile", count + 1, ": empty.")
            count += 1

# Are two cards an identical when placing cards
def match(card, card2):
    # If they share the same suit and value, they are an identical match
    if card.suit == card2.suit and card.value == card2.value:
        ret = 1
    # if match is an Ace then it is fine because both can be moved to ace piles without problems
    elif card.value == 'A' and card2.value == 'A':
        ret = 1
    # if neither of these two cases occur, return a zero to show the cards are not identical match and continue on
    else:
        ret = 0
    return ret

# get index of the next value that needs to be found to find out what the next card needed will be
def nextCard(find):
    global values
    found = 0
    count = 0
    # find index of required value, scroll through list until found
    while (found == 0):
        if find == values[count]:
            found = 1
        else:
            count += 1
    return count

#creates shuffled deck
def makeDeck():
    global cards
    global values
    global suits
    #outer for loop circles through the four suits
    for i in range(0,4):
        #middle for loop circles through the possible values, making exactly one unique combination of each value and suit
        for j in range (0,13):
                #adds each card to the deck k number of times, as specified in the question
                for z in range(0,k):
                    card = Card(suits[i],values[j])
                    #add created card to master list
                    cards.append(card)
    #shuffle the cards into random order using random
    random.shuffle(cards)

#The initial deal of the cards into the n piles with m cards.
def Deal():
    global cards
    global stPiles
    global finPiles
    count = 0
    #for n number of piles and m per pile, a new card is moved onto the pile, and the count is incremented so a card isn't used twice
    for i in range(0, n):
        for j in range(0, m):
            stPiles[i][j] = cards[count]
            count += 1
#Check to see if game is over and no more cards can be played.
def GameOver(targetDepth, theList):
    found = 0
    count = 0
    #takes Branch List as input, checks to see if there are any cards with a depth that hasn't already been checked
    while (found == 0 and count < len(theList)):
        if theList[count].depth == targetDepth:
            found = 1
        else:
            count += 1
    return found
#complete one game with auto-start
def execute():
    nodes = []
    activeBranches = []
    activeNBranches2 = []
    makeDeck()
    Deal()
    #create the blank root node, using the initial starting piles
    root = Branch (None, 0, stPiles, finPiles)
    nodes.append(root)
    activeBranches.append(root)
    playGame = 1
    targetDepth = 0
    #keep going while cards can be played
    while (playGame == 1):
        playGame = GameOver(targetDepth, nodes)
        targetDepth +=1
        #iterate through list of previously untouched nodes, make their children
        for i in range (0,len(activeBranches)):
            curr = activeBranches[i]
            curr.createChildren()
            activeBranches2 = curr.getChildren()
        activeBranches = activeBranches2
        activeBranches2 = []
        #add these children to the master list of all Branches (tree)
        nodes.extend(activeBranches)
    print("The Game began looking like this:")
    root.showPiles()
    maximum = 0
    loc =0
    #find the number of cards autodealt by finding the greatest depth in the Branch list
    for i in range (0,len(nodes)):
        if nodes[i].depth > maximum:
            maximum = nodes[i].depth
            loc = i
        #comment below two lines to test for
    nodes[loc].showPiles()
    print ("Number of cards moved onto ace piles is:" , maximum)
    return maximum
#same function as execute just without print statements to help runtime for multiple iterations
def test():
    nodes = []
    activeBranches = []
    activeNBranches2 = []
    makeDeck()
    Deal()
    #create the blank root node, using the initial starting piles
    root = Branch(None, 0, stPiles, finPiles)
    nodes.append(root)
    activeBranches.append(root)
    playGame = 1
    targetDepth = 0
    #while there are still cards that can be played
    while (playGame == 1):
        playGame = GameOver(targetDepth, nodes)
        targetDepth +=1
        #iterate through list of previously untouched Branches, make their children
        for i in range (0,len(activeBranches)):
            curr = activeBranches[i]
            curr.createChildren()
            activeBranches2 = curr.getChildren()
        activeBranches = activeBranches2
        activeBranches2 = []
        #add these children to the master list of all Branches (tree)
        nodes.extend(activeBranches)
    maximum = 0
    loc =0
    #find the number of cards autodealt by finding the greatest depth in the Branch list
    for i in range (0,len(nodes)):
        if nodes[i].depth > maximum:
            maximum = nodes[i].depth
            loc = i
    return maximum
print("Here is a demo game.")
execute()
print ("This code searches for a certain amount of moves made.")
#create array of 0-40 for histogram data and set all to zero
results=[0 for i in range(41)]
counter=0
#grab start time
startTime=time.time()
cardDealt=0
#iterates through games until it gets one that makes atleast 5 autostart moves (was set to 15 to get histogram)
while (test()<5):
    cardDealt=test()
    results[cardDealt]=results[cardDealt]+1 #add one to index of number of cards dealt, captures data for histogram
    counter=counter+1
print("Number of Iterations:", counter)
print("Runtime: %s seconds" %(time.time()-startTime))
print ("Histogram Data:",results)
