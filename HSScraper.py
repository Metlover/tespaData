from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
from pprint import pprint
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
import numpy as np
import pandas as pd
import requests
import csv
import json

startNdx = int(input("Match index start (week 1: 127205, week 2: 127838): ")) #match index start for iteration
endNdx = int(input("Match index start (week 1: 127614, week 2: 128238): ")) #match index start for iteration
week = str(input("Week of competition: "))

classIDs = [637, 671, 893, 813, 31, 274, 930, 1066, 7,46116,41887, 47817,2829,40195,2827,2826, 39117,40183] #Hero IDs
className = ['Mage', 'Paladin','Warlock', 'Priest','Hunter','Druid','Rogue','Shaman', 'Warrior', 'Paladin','Priest','Warlock','Mage','Rogue','Paladin','Hunter','Mage','Shaman'] #Hero Names

deckListFile = 'tespaweek' + week + '.txt' #Tab separated file of team names and deck codes
cardFile = 'cards.collectible.json' #Json file of all collectible hearthstone cards
archetypesFile = 'archetypes.txt' #Tab separated file of the three core cards for each deck archetype (number of cards can vary)
baseURL = 'https://compete.tespa.org/tournament/97/match/' #Scraping URL. May change with tournament.

cards = json.load(open(cardFile, encoding='utf8')) #creates dict with cards stored  

cardDbfIds = []
cardName = []

for card in cards: #creates list of all hearthstone cards
    cardDbfIds = cardDbfIds + [card['dbfId']]
    cardName = cardName + [card['name']]

archetypeList = csv.reader(open(archetypesFile, newline=''), delimiter='\t', quotechar='|') #opens deck archetype list
archetypes = {}
archetypeFixVal = 0
for archetype in archetypeList: #creates dictionary of deck archetypes and core cards
    if archetypeFixVal == 0:
        archetypeFixVal = archetypeFixVal + 1
    else:
        archetypes[archetype[0]] = [archetype[1],archetype[2],archetype[3]]

# for archetype in archetypes:
    # print(archetypes[archetype][0])
    
r = csv.reader(open(deckListFile, newline=''), delimiter='\t', quotechar='|') #opens tespa match csv
tespaDecks = {}
fixValue = 0 #lets me skip the header

print('Scraping Tespa Decks.')
for row in r: #primary deck scraping loop
    try:
        if fixValue == 0:
            fixValue = fixValue + 1
        else:
            #print(row[2])
            #print(row[1])
            deckOneObj = Deck.from_deckstring(row[2]+'==') #creates deck objects - note that I could probably consolidate this into another for loop for all four decks but I'm fine with it as is.
            deckOneCards = []
            for card in deckOneObj.cards: #iterates through cards in the deck object
                for n in range(0,card[1]): #counts how many copies of the cards are in the deck)
                    for cardDbfId in cardDbfIds: #iterates through cardIDs from the card list
                        if card[0] == cardDbfId: #checks if the card's ID is equivalent to a given card in the card list.
                            deckOneCards = deckOneCards + [cardName[cardDbfIds.index(cardDbfId)]] #if the card is found in the card list, its name is stored in the deck
            deckOneHero = className[classIDs.index(deckOneObj.heroes[0])] #gets the name of the hero for the deck
            deckOneArchetype = ''
            for archetype in archetypes: #iterates through the archetypes to try and find if the deck matches a given archetype
                if set(archetypes[archetype]).issubset(deckOneCards):
                    deckOneArchetype = archetype
                    break
            if deckOneArchetype == '': #if it doesnt fit, stores deck archetype as unknown
                deckOneArchetype = 'Unknown ' + deckOneHero
            #print(deckOneArchetype)
            #print(deckOneObj.heroes[0])
            
            deckTwoObj = Deck.from_deckstring(row[3]+'==')
            deckTwoCards = []
            for card in deckTwoObj.cards:
                for n in range(0,card[1]):
                    for cardDbfId in cardDbfIds:
                        if card[0] == cardDbfId:
                            deckTwoCards = deckTwoCards + [cardName[cardDbfIds.index(cardDbfId)]]
            deckTwoHero = className[classIDs.index(deckTwoObj.heroes[0])]  
            deckTwoArchetype = ''
            for archetype in archetypes:
                if set(archetypes[archetype]).issubset(deckTwoCards):
                    deckTwoArchetype = archetype
                    break
            if deckTwoArchetype == '':
                deckTwoArchetype = 'Unknown ' + deckTwoHero
            deckThreeObj = Deck.from_deckstring(row[4]+'==')
            deckThreeCards = []
            for card in deckThreeObj.cards:
                for n in range(0,card[1]):
                    for cardDbfId in cardDbfIds:
                        if card[0] == cardDbfId:
                            deckThreeCards = deckThreeCards + [cardName[cardDbfIds.index(cardDbfId)]]
            deckThreeHero = className[classIDs.index(deckThreeObj.heroes[0])]
            deckThreeArchetype = ''
            for archetype in archetypes:
                if set(archetypes[archetype]).issubset(deckThreeCards):
                    deckThreeArchetype = archetype
                    break
            if deckThreeArchetype == '':
                deckThreeArchetype = 'Unknown ' + deckThreeHero
            #print(deckThreeObj.heroes[0])  
            deckFourObj = Deck.from_deckstring(row[5]+'==')
            deckFourCards = []
            for card in deckFourObj.cards:
                for n in range(0,card[1]):
                    for cardDbfId in cardDbfIds:
                        if card[0] == cardDbfId:
                            deckFourCards = deckFourCards + [cardName[cardDbfIds.index(cardDbfId)]]
            deckFourHero = className[classIDs.index(deckFourObj.heroes[0])]
            deckFourArchetype = ''
            for archetype in archetypes:
                if set(archetypes[archetype]).issubset(deckFourCards):
                    deckFourArchetype = archetype
                    break
            if deckFourArchetype == '':
                deckFourArchetype = 'Unknown ' + deckFourHero
            tespaDecks[row[1]] = [[deckOneObj,deckTwoObj,deckThreeObj,deckFourObj],[deckOneCards,deckTwoCards,deckThreeCards,deckFourCards],[deckOneArchetype, deckTwoArchetype, deckThreeArchetype, deckFourArchetype], [deckOneHero, deckTwoHero, deckThreeHero, deckFourHero]] #stores these deck objects
    except:
        print(row[1] + ' has a corrupted deck')
nDecks = str(len(tespaDecks))
print('Retrieved data for ' + nDecks + ' decks from Tespa.')
#print(tespaDecks['Kcolebuc Fren'][3])

matchResults = {}

print('Retrieving match data from Tespa website. This will take several minutes, be patient.')

#for n in range(startNdx, endNdx+1):
for n in range(startNdx, endNdx + 1): #iterates through Tespa Matches
    #print(n)
    matchURL = baseURL + str(n)
    page = requests.get(matchURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    teamOneName = soup.find_all('h2')[1].get_text().strip() #name of teamOne
    teamTwoName = soup.find_all('h2')[2].get_text().strip() #name of teamTwo
    if (teamOneName in tespaDecks.keys()) & (teamTwoName in tespaDecks.keys()):
        try: #error catching in case no table is present
            tables = pd.read_html(matchURL) #reads scoretable
            teamOneSchool = soup.find_all('span')[0].get_text().strip() #school of teamOne
            teamTwoSchool = soup.find_all('span')[5].get_text().strip() #school of teamTwo
            """
            Tespa does this weird thing where sometimes, a now show is reflected in the score table as three consecutive wins by the team that showed up, with both
            teams queuing as Druid for all three matches. other times, however, Tespa prints "No Show" by the school name, hence this tricky geometry.
            """
            if not (([tables[0]['Team 1 Class'][0],tables[0]['Team 1 Class'][1],tables[0]['Team 1 Class'][2]] == ['Druid','Druid','Druid']) & ([tables[0]['Team 2 Class'][0],tables[0]['Team 2 Class'][1],tables[0]['Team 2 Class'][2]] == ['Druid','Druid','Druid'])): 
                #print(teamOneName)
                #print(teamTwoName)
                if teamOneName in tespaDecks.keys(): #checks for name in the deck lists. Have not had an issue with this yet.
                    teamOne = tespaDecks[teamOneName] #accesses that key from tespaDecks dictionary
                if teamTwoName in tespaDecks.keys():
                    teamTwo = tespaDecks[teamTwoName]
                teamOneClasses = []
                teamOneArchetypes = []
                for deckClass in tables[0]['Team 1 Class']: #stores list of heroes/Archetypes for each game for the match.
                    teamOneClasses = teamOneClasses + [deckClass]
                    teamOneArchetypes = teamOneArchetypes + [teamOne[2][teamOne[3].index(deckClass)]]
                teamTwoClasses = []
                teamTwoArchetypes = []
                for deckClass in tables[0]['Team 2 Class']:
                    teamTwoClasses = teamTwoClasses + [deckClass]
                    teamTwoArchetypes = teamTwoArchetypes + [teamTwo[2][teamTwo[3].index(deckClass)]]
                winningClass = []
                winningArchetype = []
                winningTeam = []
                winningDeck = []
                losingClass = []
                losingArchetype = []
                losingTeam = []
                losingDeck = []
                counter = 0
                for winner in tables[0]['Winner']: #iterates through the winning school name per game, then stores the winner, winning class, winning deck, winning archetype, then does the same for losing.
                    winningTeam = winningTeam + [winner] 
                    if winner == teamOneName: 
                        losingTeam = losingTeam + [teamTwoName]
                        winningArchetype = winningArchetype + [teamOneArchetypes[counter]]
                        winningClass = winningClass + [teamOneClasses[counter]]
                        losingArchetype = losingArchetype + [teamTwoArchetypes[counter]]
                        losingClass = losingClass + [teamTwoClasses[counter]]
                        winningDeck = winningDeck + [teamOne[1][teamOne[3].index(teamOneClasses[counter])]]
                        losingDeck = losingDeck + [teamTwo[1][teamTwo[3].index(teamTwoClasses[counter])]]
                    else:
                        losingTeam = losingTeam + [teamOneName]
                        winningArchetype = winningArchetype + [teamTwoArchetypes[counter]]
                        winningClass = winningClass + [teamTwoClasses[counter]]
                        losingArchetype = losingArchetype + [teamOneArchetypes[counter]]
                        losingClass = losingClass + [teamOneClasses[counter]]
                        winningDeck = winningDeck + [teamTwo[1][teamTwo[3].index(teamTwoClasses[counter])]]
                        losingDeck = losingDeck + [teamOne[1][teamOne[3].index(teamOneClasses[counter])]]
                    counter = counter + 1
                #main storage into match results.
                matchResults[str(n)] = [[teamOneName,teamTwoName],[teamOneSchool,teamTwoSchool],[teamOne,teamTwo],[teamOneClasses,teamTwoClasses],[teamOneArchetypes, teamTwoArchetypes],[winningTeam,losingTeam],[winningArchetype,losingArchetype],[winningClass, losingClass],[winningDeck, losingDeck]]
            else:
                matchResults[str(n)] = [[teamOneName,teamTwoName],[teamOneSchool, teamTwoSchool],['Forfeit']]
        except:
            teamOneSchool = soup.find_all('span')[0].get_text().strip() #school of teamOne
            teamTwoSchool = soup.find_all('span')[1].get_text().strip() #school of teamTwo
            matchResults[str(n)] = [[teamOneName,teamTwoName],[teamOneSchool, teamTwoSchool],['Forfeit']]
    else:
        matchResults[str(n)] = [[teamOneName, teamTwoName],[teamOneSchool, teamTwoSchool],['Forfeit']]


nMatches = str(len(matchResults))
print(nMatches + 'retrieved from the tespa website for week ' + week + '.')
    
np.save('TespaDecksWeek' + week + '.npy', tespaDecks)
np.save('TespaMatchResultsWeek' + week + '.npy', matchResults)

print('Decks saved in directory as \"TespaDecksWeek' + week + '.npy\"')
print('Match results saved in directory as \"TespaMatchResultsWeek' + week + '.npy\"')

#1: import decklists from csv | DONE
#2 read in decklists and create them as deck objects  | DONE
#3 classify decks on archetypes (search for core cards within decks and classify them as such - possibly use CSV for this?) | DONE
#4 scrape matchup data from week 1 using startNdx, endNdx, bs4
#5 match deck lists to matchup data
#6 calculate archetype frequency, look at tech card matchups and how they improve WR
#7 write and research report