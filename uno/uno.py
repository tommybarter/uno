from tkinter import *
from tkinter import simpledialog
from tkinter import ttk

import os, os.path
import random

class GameWindow:


    
    def __init__(self, master):

        self.master = master

        self.background_image=PhotoImage(file=self.get_background_image())

        w = self.background_image.width() 
        h = self.background_image.height() + 50
        self.master.geometry("%dx%d+0+0" % (w, h))
        self.master.title("UNO GAME")        
        self.master.resizable(False, False)

        self.canvas = Canvas(self.master)        
        self.canvas.pack(side='top', fill='both', expand='yes')
        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW) 


        self.startButton = Button(self.canvas, text="New Game", font=('Helvetica', 24), command=self.callbackNewGame, background="dark orange", foreground="white")
        self.startButton.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.main_menu(self.master)
        self.status = StatusBar(self.master)
        self.status.pack(side=BOTTOM, fill=X)
        self.status.set("READY")        
       
       
    @staticmethod
    def get_background_image():
        return os.path.join(os.getcwd(), 'Images', 'UNOBackground.png')

    def main_menu(self, master):
        menu = Menu(master)
        master.config(menu=menu)

        gameMenu = Menu(menu)
        menu.add_cascade(label="Game", menu=gameMenu)
        gameMenu.add_command(label="New", command=self.callbackNewGame)
        gameMenu.add_command(label="Restart", command=self.callbackRestartGame)
        gameMenu.add_separator()
        gameMenu.add_command(label="Options", command=self.callbackRestartGame)
        gameMenu.add_separator()
        gameMenu.add_command(label="Exit", command=master.quit)

        helpMenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="About...", command=self.callbackHelpAbout)

    def callbackNewGame(self):
        optsDialog = DialogNewGame(self.master)
        self.master.wait_window(optsDialog.top)      

        noOfPlayers = int(optsDialog.noOfPlayers)
        players = []

        player1 = Player(optsDialog.player1)
        players.append(player1)

        if noOfPlayers > 1:
            player2 = Player(optsDialog.player2)
            players.append(player2)     
        
        self.discardPile = DiscardPile() 
        self.drawPile = DrawPile(FullDeck().getCards())

        # Clear Board
        self.startButton.destroy()

        self.game = Game(players, self.discardPile, self.drawPile, self.canvas)

        self.status.set("CURRENT PLAYER: " + self.game.currentPlayer.name)
             

        




    def callbackHelpAbout(self):
        print ("help about")

    def callbackRestartGame(self):
        print ("restart game")

   

class DialogOptions:
    
    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Value").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        
        self.top.destroy()


class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class DialogNewGame:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Number of Players").pack()
        self.cbNoOfPlayers = ttk.Combobox(top, text="Number of Players", values=[1,2], justify='left', state='readonly')
        self.cbNoOfPlayers.pack(padx=5)
        self.cbNoOfPlayers.current(1)
        
        Label(top, text="Names").pack()

        self.ePlayer1 = Entry(top)
        self.ePlayer1.pack(padx=5)

        self.ePlayer2 = Entry(top)
        self.ePlayer2.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

        self.ePlayer1.focus()


    def ok(self):

        self.noOfPlayers = self.cbNoOfPlayers.get()
        self.player1 = self.ePlayer1.get()
        self.player2 = self.ePlayer2.get()

        self.top.destroy()

# Outlining the actions of the player
class Player:
    def __init__(self, playerName, cpu=False, playerhand=None, playerTurn=False):
        self.name = playerName
        self.hand = None
        self.turn = False
        
    def setName(self, playerName):
        self.name = playerName

    def setHand(self, thishand):
        self.hand = thishand

    def getHand(self):
        return self.hand

    def setTurn(self, thisturn):
        self.turn = thisturn

    def placeCard():
        pass

    def drawCard(fromdeck):
        pass


class Card:
    VALUES = ["0","1","2","3","4","5","6","7","8","9","Skip","Reverse","Draw2","Wild","Draw4"]
    SKIP = 10
    REVERSE = 11
    DRAW2 = 12
    WILD = 13
    DRAW4 = 14

    COLOURS = ["Red","Yellow","Green","Blue","Wild"]
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    ALL = 4

    def __init__(self,val,col,fac=False):
        self.value = self.VALUES[val]
        self.colour = self.COLOURS[col]
        self.faceup = fac

    def get_name(self):
        return self.value + " of " + self.colour

    def get_image(self):
        pass

    @staticmethod
    def get_reverse_image():           
        return os.path.join(os.getcwd(), 'Cards', 'Card_Back.png')

    @staticmethod
    def get_empty_image():           
        return os.path.join(os.getcwd(), 'Cards', 'Card_Empty.png')

# Deck is the super class for Hand, DrawPile and DiscardPile because they use the same array of cards.
class Deck():
    MAXCARDS = 108
    
    def __init__(self, thesecards=[]):
        self.cards = thesecards
    
    def removeCards(self, cards):
        pass

    def addCards(self, cards):
        pass

    def takeCards(self, no_of_cards):
        somecards = self.cards[:no_of_cards]
        del self.cards[:no_of_cards]
        return somecards
    
    def turnAllCardsUp():
        pass

    def turnAllCardsDown():
        pass

    def getCards(self):
        return self.cards

    def shuffleCards(self):
        random.shuffle(self.cards)

    def getNumberofCards(self):
        return len(self.cards)

class FullDeck(Deck):
    
    def __init__(self):
        super()
        self.cards = []
        # Add all cards
        colours = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,Card.DRAW2,Card.DRAW2,Card.REVERSE,Card.REVERSE,Card.SKIP,Card.SKIP]
        wilds = [Card.WILD,Card.WILD,Card.WILD,Card.WILD,Card.DRAW4,Card.DRAW4,Card.DRAW4,Card.DRAW4]
       
        for card in colours:
            self.cards.append(Card(card, Card.RED))
            self.cards.append(Card(card, Card.GREEN))
            self.cards.append(Card(card, Card.BLUE))
            self.cards.append(Card(card, Card.YELLOW))

        for wild in wilds:
            self.cards.append(Card(wild, Card.ALL))        

class Hand(Deck):
   def __init__(self,thesecards=None):
       self.cards = thesecards
       super()

class DrawPile(Deck):
    def __init__(self,thesecards=None):
       self.cards = thesecards
       super()
       

class DiscardPile(Deck):
    def __init__(self,thesecards=None):
        self.cards = thesecards
        super()
       

       #self.fac=True

    def convertToDrawPile():
        pass


class Game:    
    def __init__(self, theseplayers,thisDiscardPile,thisDrawPile,theCanvas):
        self.players = theseplayers
        self.discardPile = thisDiscardPile
        self.drawPile = thisDrawPile
        self.canvas = theCanvas

        # Shuffle the cards
        self.drawPile.shuffleCards()

        # Give players some cards
        for player in self.players:
            player.setHand(Hand(self.drawPile.takeCards(7)))
            print(player.name)
            for card in player.hand.getCards():
                print(card.get_name())
            
        # Select first player
        self.currentPlayer = self.chooseFirstPlayer()

        # Setup Board
        self.reverse_image=PhotoImage(file=Card.get_reverse_image())
        self.drawPileHolder = Label(self.canvas, text="Draw Pile", image=self.reverse_image,compound=BOTTOM)
        self.drawPileHolder.place(relx=0.9, rely=0.5, anchor=CENTER)

        self.empty_image=PhotoImage(file=Card.get_empty_image())
        self.drawPileHolder = Label(self.canvas, text="Discard Pile", image=self.empty_image,compound=BOTTOM)
        self.drawPileHolder.place(relx=0.5, rely=0.5, anchor=CENTER)

        # First move
        self.next_turn()

        
    def checkMove(self,card,discard=True):
        pass

    def next_turn(self):
        pass

    def chooseFirstPlayer(self):
        return random.choice(self.players)

    def endGame(self):
        pass


root = Tk()

app = GameWindow(root)

root.mainloop()
root.destroy() # optional; see description below