# Superdeck interface to play Schnapsen
import menue
import playerS
from random import shuffle, choice
import getpass
import sys


class Observer:
    def __init__(self):
        #
        pass
         
    def observe(self):
        #
        pass
    
    def refresh(self):
        #
        pass
    
    
# MATERIALS #
class SuperDeck:
    
    def __init__(self, mode):
        
        # 4 x 5 CARDS // 4 Elements, Cards 2, 3, 4, 10, 11 // 20 Cards shuffled for poping
        self.deck = [EarthTwo(), EarthThree(), EarthFour(), EarthTen(), EarthEleven(),
                      WaterTwo(), WaterThree(), WaterFour(), WaterTen(), WaterEleven(),
                      FireTwo(), FireThree(), FireFour(), FireTen(), FireEleven(),
                      WindTwo(), WindThree(), WindFour(), WindTen(), WindEleven()]
        shuffle(self.deck)
        #
        self.gamephase = 1
        self.sealcard = self.deck[0]
        self.masterelement = self.deck[0].element
        self.counter = 1
        #
        self.winner = None
        self.players = {}
        
        self.bots = ['Balisto', 'Susi']
        
        #self.players[username] = player.UserPlayer(username, self.masterelement)
        if mode == 'bots': self.players[self.bots[0]] = playerS.Balisto('Balisto', self.masterelement)
        else: self.players[mode] = playerS.UserPlayer(mode, self.masterelement)
        self.players[self.bots[1]] = playerS.Susi('Susi', self.masterelement)
        
        for i in self.players.values():
            i.initiative = 1
            break
        for i in self.players.values():
            for t in range(5):
                card = self.deck.pop()
                card.player = i.name
                i.grapcard(card)
            
        print('Game Start')
        print('Master:', self.sealcard.name, self.sealcard.symbol, self.masterelement)
        print('--------------------------------------------------------------------')
        
    def reset(self):
        #
        self.deck = [EarthTwo(), EarthThree(), EarthFour(), EarthTen(), EarthEleven(),
                      WaterTwo(), WaterThree(), WaterFour(), WaterTen(), WaterEleven(),
                      FireTwo(), FireThree(), FireFour(), FireTen(), FireEleven(),
                      WindTwo(), WindThree(), WindFour(), WindTen(), WindEleven()]
        shuffle(self.deck)
        #
        self.gamephase = 1
        self.sealcard = self.deck[0]
        self.masterelement = self.deck[0].element
        self.counter = 1
        #
        self.winner = None
        for player in self.players.values():
            player.win = 0
            player.initiative = 0
            player.outpowers['Herz'] = 30
            player.outpowers['Caro'] = 30
            player.outpowers['Pik'] = 30
            player.outpowers['Kreuz'] = 30
            player.outcounts = {}
            player.outcounts['Herz'] = 5
            player.outcounts['Caro'] = 5
            player.outcounts['Pik'] = 5
            player.outcounts['Kreuz'] = 5
            player.activeloss = 0
            player.points = 0
            player.merrypoints = 0
            player.tableloss = 0
        
        for i in self.players.values():
            i.initiative = 1
            break
        for i in self.players.values():
            i.handcards = {}
            for t in range(5):
                card = self.deck.pop()
                card.player = i.name
                i.grapcard(card)
        
        print('Master:', self.sealcard.name, self.sealcard.symbol, self.masterelement)
        print('*ready*')
        
    def giveCard(self, player):
        #
        if self.deck:
            card = self.deck.pop()
            card.player = player.name
            player.grapcard(card)
             
        
    def counterPlayerget(self):
        #
        for player in self.players.values():
            
            if player.initiative == 0: return player
        return 0
         
    def activePlayerget(self):
        #
        for player in list(self.players.values()):
            
            if player.initiative == 1: return player
        return 0

    def switchcard(self, handcards):
        # returns the sealcard or None
        kill = None
        for card in handcards:
            if card.element == self.masterelement and card.value == 2:
                self.deck[0] = card
                kill = card.name
        if kill:
            print('switch.')
            return self.sealcard, kill
        return None, None

        
    def start(self):
        #
        while self.gamephase == 1 or self.gamephase == 2:
            
            brick = 0
            for player in self.players.values():
                if player.win == 1: brick = 1
            if brick:
                self.gamephase = 3
                break
            
            if self.activePlayerget().points + self.activePlayerget().merrypoints >= 66:

                self.activePlayerget().win = 1
                self.gamephase = 3
                break

            if self.deck != [] and self.deck[0].value != 2:
                newc, kill = self.switchcard(list(self.activePlayerget().handcards.values()))
                if newc:
                    newc.player = self.activePlayerget().name
                    self.sealcard = self.activePlayerget().handcards[kill]
                    del self.activePlayerget().handcards[kill]
                    self.activePlayerget().handcards[newc.name] = newc
                
            # cards play
            firstplay = self.activePlayerget().playcard(self.gamephase)
            
            averages, referenz = self.counterPlayerget().prepare(firstplay)
            
            print('')
                
            secondplay = self.counterPlayerget().counter(firstplay, self.gamephase)
            
            self.activePlayerget().removeCard(firstplay)
            self.counterPlayerget().removeCard(secondplay)
            
            # 
            if firstplay.element == secondplay.element:
                if firstplay.value > secondplay.value:
                    
                    self.activePlayerget().potcheck(firstplay.value + secondplay.value)
                    self.counterPlayerget().losscheck(secondplay.value)
                    
                elif firstplay.value < secondplay.value:
                    
                    link = self.activePlayerget()
                    self.counterPlayerget().potcheck(firstplay.value + secondplay.value)
                    link.losscheck(firstplay.value)
                    
                    
            elif secondplay.element == self.masterelement:
                
                link = self.activePlayerget()
                self.counterPlayerget().potcheck(firstplay.value + secondplay.value)
                link.losscheck(firstplay.value)
                
            elif firstplay.element != secondplay.element:
                
                link = self.counterPlayerget()
                self.activePlayerget().potcheck(firstplay.value + secondplay.value)
                link.losscheck(secondplay.value)
            
            #if self.players[firstplay.player].initiative == 0: lossfunction(firstplay.value*(-1))
            #if self.players[firstplay.player].initiative == 1: lossfunction(firstplay.value + secondplay.value - 6.6)
            # redraw cards
            self.giveCard(self.activePlayerget())
            self.giveCard(self.counterPlayerget())
            self.counter += 1
            if self.deck == []:
                if self.gamephase == 1: print('Deck out of cards..')
                self.gamephase = 2
            if self.counter == 11: self.gamephase = 3
            else: print('cardround :', self.counter, 'starting..')
            
        if self.gamephase == 3:
            nope = 0
            ref_player = list(self.players.values())
            for player in ref_player:
                if player.win:
                    
                    print(player.name, 'has won the game.')
                    for pl in self.players.values():
                        if pl.name != player.name:
                            if pl.points >= 33: player.winpoints += 1
                            elif 0 < pl.points < 33: player.winpoints += 2
                            elif pl.points == 0: player.points += 3
                    nope += 1
                    
            if nope == 0:
                print(self.activePlayerget().name, 'has won the game.')
                for pl in ref_player:
                    if pl.name != self.activePlayerget().name:
                        if pl.points >= 33: self.activePlayerget().winpoints += 1
                        elif 0 < pl.points < 33: self.activePlayerget().winpoints += 2
                        elif pl.points == 0: self.activePlayerget().points += 3
              
        for player in self.players.values():
            print(player.name, 'loss', player.tableloss, 'Points ->', player.points + player.merrypoints)
            if player.win: print(player.name, 'WinPoints:', player.winpoints)
    
    
# Cards
class Card:
    def info(self):
        pass
        
class EarthTwo(Card):
    def __init__(self):
        self.value = 2
        self.element = 'Herz'
        self.symbol = chr(9829)
        self.name = 'Herz Bube'
        self.player = None
        
class EarthThree(Card):
    def __init__(self):
        self.value = 3
        self.element = 'Herz'
        self.symbol = chr(9829)
        self.name = 'Herz Dame'
        self.player = None
        
class EarthFour(Card):
    def __init__(self):
        self.value = 4
        self.element = 'Herz'
        self.symbol = chr(9829)
        self.name = 'Herz König'
        self.player = None
        
class EarthTen(Card):
    def __init__(self):
        self.value = 10
        self.element = 'Herz'
        self.symbol = chr(9829)
        self.name = 'Herz Zehn'
        self.player = None
        
class EarthEleven(Card):
    def __init__(self):
        self.value = 11
        self.element = 'Herz'
        self.symbol = chr(9829)
        self.name = 'Herz Ass'
        self.player = None
        
class WaterTwo(Card):
    def __init__(self):
        self.value = 2
        self.element = 'Caro'
        self.symbol = chr(9830)
        self.name = 'Caro Bube'
        self.player = None
        
class WaterThree(Card):
    def __init__(self):
        self.value = 3
        self.element = 'Caro'
        self.symbol = chr(9830)
        self.name = 'Caro Dame'
        self.player = None
        
class WaterFour(Card):
    def __init__(self):
        self.value = 4
        self.element = 'Caro'
        self.symbol = chr(9830)
        self.name = 'Caro König'
        self.player = None
        
class WaterTen(Card):
    def __init__(self):
        self.value = 10
        self.element = 'Caro'
        self.symbol = chr(9830)
        self.name = 'Caro Zehn'
        self.player = None
        
class WaterEleven(Card):
    def __init__(self):
        self.value = 11
        self.element = 'Caro'
        self.symbol = chr(9830)
        self.name = 'Caro Ass'
        self.player = None

class FireTwo(Card):
    def __init__(self):
        self.value = 2
        self.element = 'Pik'
        self.symbol = chr(9828)
        self.name = 'Pik Bube'
        self.player = None
        
class FireThree(Card):
    def __init__(self):
        self.value = 3
        self.element = 'Pik'
        self.symbol = chr(9828)
        self.name = 'Pik Dame'
        self.player = None
        
class FireFour(Card):
    def __init__(self):
        self.value = 4
        self.element = 'Pik'
        self.symbol = chr(9828)
        self.name = 'Pik König'
        self.player = None
        
class FireTen(Card):
    def __init__(self):
        self.value = 10
        self.element = 'Pik'
        self.symbol = chr(9828)
        self.name = 'Pik Zehn'
        self.player = None
        
class FireEleven(Card):
    def __init__(self):
        self.value = 11
        self.element = 'Pik'
        self.symbol = chr(9828)
        self.name = 'Pik Ass'
        self.player = None

class WindTwo(Card):
    def __init__(self):
        self.value = 2
        self.element = 'Kreuz'
        self.symbol = chr(9831)
        self.name = 'Kreuz Bube'
        self.player = None
        
class WindThree(Card):
    def __init__(self):
        self.value = 3
        self.element = 'Kreuz'
        self.symbol = chr(9831)
        self.name = 'Kreuz Dame'
        self.player = None
        
class WindFour(Card):
    def __init__(self):
        self.value = 4
        self.element = 'Kreuz'
        self.symbol = chr(9831)
        self.name = 'Kreuz König'
        self.player = None
        
class WindTen(Card):
    def __init__(self):
        self.value = 10
        self.element = 'Kreuz'
        self.symbol = chr(9831)
        self.name = 'Kreuz Zehn'
        self.player = None
        
class WindEleven(Card):
    def __init__(self):
        self.value = 11
        self.element = 'Kreuz'
        self.symbol = chr(9831)
        self.name = 'Kreuz Ass'
        self.player = None

if __name__ == '__main__':
    
    mode = ''
    if len(sys.argv) > 1:
        if sys.argv[1] == 'bots': mode = 'bots'
    
    if mode != 'bots': mode = getpass.getuser()
    
    
    Deck = SuperDeck(mode)
    
    end = 0
    while not end:
        a = Deck.start()
        for player in Deck.players.values():
            print(player.name, 'gameloss', player.gameloss, end=' ')
            if player.winpoints >= 7:
                end = 1
                print(player.name, 'has won the table.', end=' ')
                print('')
        if not end:
            print()
            Deck.reset()
            
        
        
