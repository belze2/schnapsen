# player and bot classes for superdeck.py
import menue
from random import shuffle, choice

class Player:
    def average_outpower(self, card):
        #
        if self.outcounts[card.element]:
            return self.outpowers[card.element] / self.outcounts[card.element]
        else: return 0
        
    def visithand(self, cardnames):
        #
        pik_cards = []
        herz_cards = []
        kreuz_cards = []
        caro_cards = []
        
        pik = chr(9828)
        herz = chr(9829)
        kreuz = chr(9831)
        caro = chr(9830)
        
        for card in cardnames:
            if self.handcards[card].element == 'Pik': pik_cards.append(self.handcards[card].value)
            elif self.handcards[card].element == 'Herz': herz_cards.append(self.handcards[card].value)
            elif self.handcards[card].element == 'Kreuz': kreuz_cards.append(self.handcards[card].value)
            elif self.handcards[card].element == 'Caro': caro_cards.append(self.handcards[card].value)
        
        pik_cards.sort()
        herz_cards.sort()
        kreuz_cards.sort()
        caro_cards.sort()
        
        if pik_cards:
            print(pik, end=' ')
            for v in pik_cards:
                print(v, end=' ')
        if herz_cards:
            print(herz, end=' ')
            for v in herz_cards:
                print(v, end=' ')
        if kreuz_cards:
            print(kreuz, end=' ')
            for v in kreuz_cards:
                print(v, end=' ')
        if caro_cards:
            print(caro, end=' ')
            for v in caro_cards:
                print(v, end=' ')
                
        print('')

    def getmerrycards(self, playcard):
        #
        erde = 0
        wasser = 0
        feuer = 0
        wind = 0
        
        merry = 0
        
        for card in self.handcards.values():
            if card.value == 3 or card.value == 4 and card not in self.merrychecked:
                self.merrychecked.append(card)
                if card.element == 'Herz': erde += 1
                elif card.element == 'Caro': wasser += 1
                elif card.element == 'Pik': feuer += 1
                elif card.element == 'Kreuz': wind += 1
        
        if erde == 2: merry += 1
        elif wasser == 2: merry += 1
        elif feuer == 2: merry += 1
        elif wind == 2: merry += 1
        
        if merry > 0 and playcard in self.merrychecked:
            self.merrypoints += 20
            print('Played Card is merried..')
        if playcard.element == self.masterelement:
            self.merrypoints += 20
        
        if merry: return 1
        return 0
    
    def prepare(self, tableCard):
        #
        self.outcounts[tableCard.element] -= 1
        self.outpowers[tableCard.element] -= tableCard.value
        ret = []
        rev = []
        for card in self.handcards.values():
            ret.append(self.average_outpower(card) - card.value)
            rev.append(card.name)
        self.referenz = rev
        self.averages = ret
        return ret, rev

    def grapcard(self, card):
        #
        card.player = self.name
        self.outcounts[card.element] -= 1
        self.outpowers[card.element] -= card.value
        self.handcards[card.name] = card
        

    def removeCard(self, card):
        #
        del self.handcards[card.name]
        
        
    def potcheck(self, points):
        #
        self.points += points
        self.initiative = 1
        
    def losscheck(self, points):
        #
        self.activeloss = points
        self.tableloss += points
        self.gameloss += points
        self.initiative = 0
        
    def finishTurn(self):
        #
        print(self.name, ':', self.points)
        if self.points >= 66: self.win = 1     

class Balisto(Player):
    def __init__(self, name, masterelement):
        #
        self.name = name
        self.handcards = {}
        self.masterelement = masterelement
        self.initiative = 0
        self.win = 0
        self.outpowers = {}
        self.outpowers['Herz'] = 30
        self.outpowers['Caro'] = 30
        self.outpowers['Pik'] = 30
        self.outpowers['Kreuz'] = 30
        self.outcounts = {}
        self.outcounts['Herz'] = 5
        self.outcounts['Caro'] = 5
        self.outcounts['Pik'] = 5
        self.outcounts['Kreuz'] = 5
        #
        self.activeloss = 0
        self.points = 0
        self.merrypoints = 0
        self.tableloss = 0
        self.gameloss = 0
        self.winpoints = 0
        #
        self.referenz = None
        self.averages = None
        self.merrychecked = []

        
    def playcard(self, gamephase):
        #
        print(self.name, 'playing...')
        options = []
        cardlist = self.handcards.values()
        for k, card in enumerate(cardlist):
            #
            if self.getmerrycards(card):
                #
                options.append(k)
                
            elif card.value >= int(self.average_outpower(card)):
                #
                options.append(k)
        
        print('options :', options)
        if options: c = list(cardlist)[choice(options)]
        else: c = choice(list(self.handcards.values()))
        self.getmerrycards(c)
        print(c.name, 'played..')
        return c
    
    def counter(self, tablecard, gamephase):
        #
        cardset = self.handcards.keys()
        set_element = []
        set_lows = []
        set_notrump = []
        rest = []
        taker = []
        if gamephase == 2:
            for card in self.handcards.values():
                #
                if card.element == tablecard.element:
                    set_element.append(card.name)
                    if card.value > tablecard.value:
                        taker.append(card.name)
                elif tablecard.element == self.masterelement:
                    set_notrump.append(card.name)
                    if card.value == 2:set_lows.append(card.name)
                else:
                    rest.append(card.name)

                if taker: rem = taker
                elif set_element: rem = set_element
                elif set_lows: rem = set_lows
                elif set_notrump: rem = set_notrump
                else: rem = rest

        elif gamephase == 1:
            rem = cardset
        
        c = choice(list(rem))
        print('Counter Card Played:', c)
        return self.handcards[c]
    
class Susi(Player):
    def __init__(self, name, masterelement):
        #
        self.name = name
        self.handcards = {}
        self.masterelement = masterelement
        self.initiative = 0
        self.win = 0
        self.outpowers = {}
        self.outpowers['Herz'] = 30
        self.outpowers['Caro'] = 30
        self.outpowers['Pik'] = 30
        self.outpowers['Kreuz'] = 30
        self.outcounts = {}
        self.outcounts['Herz'] = 5
        self.outcounts['Caro'] = 5
        self.outcounts['Pik'] = 5
        self.outcounts['Kreuz'] = 5
        #
        self.activeloss = 0
        self.points = 0
        self.merrypoints = 0
        self.tableloss = 0
        self.gameloss = 0
        self.winpoints = 0
        #
        self.referenz = None
        self.averages = None
        self.merrychecked = []

        
    def playcard(self, gamephase):
        #
        print(self.name, 'playing...', end=' ')
        options = []
        cardlist = self.handcards.values()
        for k, card in enumerate(cardlist):
            #
            if self.getmerrycards(card):
                #
                options.append(k)
                
            elif gamephase == 2 and self.outcounts[card.element] and card.value >= int(self.average_outpower(card)):
                #
                options.append(k)

            elif gamephase == 1:
                for x, n in enumerate(self.referenz):
                    if n == card.name:
                        if self.averages[x] > 0: options.append(k)
        
        print('options :', options)
        if options: c = list(cardlist)[choice(options)]
        else: c = choice(list(self.handcards.values()))
        self.getmerrycards(c)
        print(c.name, 'played..')
        return c
    
    def counter(self, tablecard, gamephase):
        #
        cardset = self.handcards.keys()
        set_element = []
        set_trump = []
        rem = None
        if gamephase == 2:
            for card in self.handcards.values():
                #
                if card.element == tablecard.element: set_element.append(card.name)
                if card.element == self.masterelement: set_trump.append(card.name)
                
            if set_element: rem = set_element 
            elif set_trump: rem = set_trump
            else: rem = cardset
        elif gamephase == 1:
            rem = cardset
        
        c = choice(list(rem))
        print('Counter Card Played:', c)
        return self.handcards[c]
        
class UserPlayer(Player):
    def __init__(self, name, masterelement):
        #
        self.name = name
        self.handcards = {}
        self.masterelement = masterelement
        self.initiative = 0
        self.win = 0
        self.outpowers = {}
        self.outpowers['Herz'] = 30
        self.outpowers['Caro'] = 30
        self.outpowers['Pik'] = 30
        self.outpowers['Kreuz'] = 30
        self.outcounts = {}
        self.outcounts['Herz'] = 5
        self.outcounts['Caro'] = 5
        self.outcounts['Pik'] = 5
        self.outcounts['Kreuz'] = 5
        #
        self.activeloss = 0
        self.points = 0
        self.merrypoints = 0
        self.tableloss = 0
        self.gameloss = 0
        self.winpoints = 0
        #
        
        self.referenz = None
        self.averages = None
        self.merrychecked = []
        
        
    def playcard(self, gamephase):
        #
        print(self.name, 'playing...')
        self.visithand(self.handcards.keys())
        c = menue.play(self.handcards.keys(), 'Select a card to play:')
        self.getmerrycards(self.handcards[c])
        print(c, 'played...')
        return self.handcards[c]
    
    def counter(self, tablecard, gamephase):
        #
        cardset = self.handcards.keys()
        set_element = []
        set_trump = []
        rem = None
        if gamephase == 2:
            for card in self.handcards.values():
                #
                if card.element == tablecard.element: set_element.append(card.name)
                if card.element == self.masterelement: set_trump.append(card.name)
                
            if set_element: rem = set_element 
            elif set_trump: rem = set_trump
            else: rem = cardset
        elif gamephase == 1:
            rem = cardset
        
        self.visithand(rem)
        c = menue.play(rem, 'Select a COUNTER: '+tablecard.name)
        print('Counter Card Played:', c)
        return self.handcards[c]
