from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox

import os, os.path
import random

class GameWindow:


    
    def __init__(self, master):

        self.master = master

        self.background_image=PhotoImage(file=self.get_background_image())

        w = self.background_image.width() 
        h = self.background_image.height() + 20
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
        gameMenu.add_command(label="Exit", command=master.quit)

        helpMenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="About...", command=self.callbackHelpAbout)

    def callbackNewGame(self):
        optsDialog = DialogNewGame(self.master)
        self.master.wait_window(optsDialog.top)      

        noOfPlayers = int(optsDialog.noOfPlayers)
        players = []

        player1 = Player(optsDialog.player1, 1)
        players.append(player1)

        if noOfPlayers > 1:
            player2 = Player(optsDialog.player2, 2)
            players.append(player2)     
        
        self.discardPile = DiscardPile() 
        self.drawPile = DrawPile(FullDeck().getCards())

        # Clear Board
        self.startButton.destroy()

        self.game = Game(players, self.discardPile, self.drawPile, self.canvas, self.status)

        self.status.set("CURRENT PLAYER: " + self.game.currentPlayer.name)
             

        




    def callbackHelpAbout(self):
        print ("help about")

    def callbackRestartGame(self):
        print ("restart game")
 
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

class DialogChooseColour:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)
        self.colourChoice = Card.COLOURS[0]

        Label(top, text="Choose a colour").pack()
        self.colours = ttk.Combobox(top, text="Colour", values=Card.COLOURS[:-1], justify='left', state='readonly')
        self.colours.pack(padx=5)
        self.colours.current(0)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

        self.colours.focus()


    def ok(self):

        self.colourChoice = self.colours.get()        

        self.top.destroy()

# Outlining the actions of the player
class Player:
    def __init__(self, playerName, playerID, cpu=False, playerhand=None, playerTurn=False):
        self.name = playerName
        self.playerid = playerID
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

    COLOURS = ["Blue", "Green", "Red", "Yellow", "Wild"]
    BLUE = 0
    GREEN = 1
    RED = 2
    YELLOW = 3
    ALL = 4

    def __init__(self,val,col,fac=False):
        self.value = self.VALUES[val]
        self.colour = self.COLOURS[col]
        self.faceup = fac

    def get_name(self):
        return self.colour + " " + self.value

    def get_image(self):
        return os.path.join(os.getcwd(), 'Cards', self.colour, self.colour+self.value+".png")        

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
    
    def removeCards(self):
        self.cards.clear()

    def removeCard(self, id):
        del self.cards[id]

    def addCard(self, card):
        self.cards.append(card)

    def addCards(self, cards):
        self.cards.extend(cards)

    def takeCards(self, no_of_cards):
        if not self.cards:
            return []
        if len(self.cards) < no_of_cards:
            somecards = cards
        else:
            somecards = self.cards[:no_of_cards]
        del self.cards[:no_of_cards]
        # If only 1 card, return as a single object
        if len(somecards) == 1:
            return somecards[0]
        else:
            # Return list
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

    def getTopCard(self):
        if not self.cards:
            return None
        else:
            return self.cards[-1]

class FullDeck(Deck):
    
    def __init__(self):
        super()
        self.cards = []
        # Add all cards
        colours = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,Card.DRAW2,Card.DRAW2,Card.REVERSE,Card.REVERSE,Card.SKIP,Card.SKIP]
        wilds = [Card.WILD,Card.WILD,Card.WILD,Card.WILD,Card.DRAW4,Card.DRAW4,Card.DRAW4,Card.DRAW4]
       
        for card in colours:
            self.cards.append(Card(card, Card.BLUE))
            self.cards.append(Card(card, Card.GREEN))
            self.cards.append(Card(card, Card.RED))
            self.cards.append(Card(card, Card.YELLOW))

        for wild in wilds:
            self.cards.append(Card(wild, Card.ALL))        

class Hand(Deck):
   def __init__(self,thesecards=[]):
       self.cards = thesecards
       super()

class DrawPile(Deck):
    def __init__(self,thesecards=[]):
       self.cards = thesecards
       super()
       

class DiscardPile(Deck):
    def __init__(self,thesecards=[]):
        self.cards = thesecards
        super()         

    def convertToDrawPile():
        pass


class Game:    
    def __init__(self, theseplayers,thisDiscardPile,thisDrawPile,theCanvas,theStatus):
        self.players = theseplayers
        self.discardPile = thisDiscardPile
        self.drawPile = thisDrawPile
        self.canvas = theCanvas
        self.status = theStatus

        self.player1Pile = []
        self.player2Pile = []

        self.player1PileImages = []
        self.player2PileImages = []

        self.SKIPCARDS = ["Skip","Reverse","Draw2","Draw4"]
        self.DRAWCARDS = ["Draw2","Draw4"]
        self.WILDCARDS = ["Wild", "Draw4"]
        
        # Shuffle the cards
        self.drawPile.shuffleCards()

        # Give players some cards
        for player in self.players:
            player.setHand(Hand(self.drawPile.takeCards(7)))            
            
        # Select first player
        self.currentPlayer = self.chooseFirstPlayer()
        self.currentPlayer.setTurn(True)

        # Setup Board

        # Draw Pile Area
        self.reverse_image=PhotoImage(file=Card.get_reverse_image())
        self.drawPileArea = Button(self.canvas, text="Draw Pile", image=self.reverse_image,compound=BOTTOM,command=self.drawPileCallback)
        self.drawPileArea.place(relx=0.9, rely=0.5, anchor=CENTER)
        self.updateDrawPile()

        # Discard Pile Area
        self.empty_image=PhotoImage(file=Card.get_empty_image())
        self.discardPileArea = Label(self.canvas, text="Discard Pile", image=self.empty_image,compound=BOTTOM)
        self.discardPileArea.place(relx=0.5, rely=0.5, anchor=CENTER)       
        
        self.placeFirstCard()

        # Player 1 Area        
        self.player1Frame = LabelFrame(master=self.canvas,height=240,width=10000,borderwidth=2,background="orange",pady=10,highlightthickness=2,text=self.players[0].name+"'s Cards")
        self.player1Frame.pack(side=BOTTOM)
        self.player1Frame.pack_propagate(False)             

        self.player1Canvas = Canvas(self.player1Frame, height=220, width=90000, scrollregion=(0, 0, "2000", "220"))

        self.player1Canvas.scrollX = Scrollbar(self.player1Frame, orient=HORIZONTAL)
        self.player1Canvas['xscrollcommand'] = self.player1Canvas.scrollX.set
        self.player1Canvas.scrollX['command'] = self.player1Canvas.xview

        self.player1Canvas.scrollX.pack(side=BOTTOM, fill=X)

        self.player1Canvas.pack(side=LEFT)       
       
        self.drawCards(self.players[0], self.player1Canvas, self.player1Pile, self.player1PileImages)
        
        
        if len(self.players) > 1:
            # Player 2 Area
            self.player2Frame = LabelFrame(master=self.canvas,height=240,width=10000,borderwidth=2,background="coral",pady=10,highlightthickness=2,text=self.players[1].name+"'s Cards")            
            self.player2Frame.pack(side=TOP)
            self.player2Frame.pack_propagate(False)

            self.player2Canvas = Canvas(self.player2Frame, height=220, width=90000, scrollregion=(0, 0, "2000", "220"))

            self.player2Canvas.scrollX = Scrollbar(self.player2Frame, orient=HORIZONTAL)
            self.player2Canvas['xscrollcommand'] = self.player2Canvas.scrollX.set
            self.player2Canvas.scrollX['command'] = self.player2Canvas.xview

            self.player2Canvas.scrollX.pack(side=BOTTOM, fill=X)

            self.player2Canvas.pack(side=LEFT)       

            self.drawCards(self.players[1], self.player2Canvas, self.player2Pile, self.player2PileImages)

        # Disable cards
        self.disablePlayersCards()

    def placeFirstCard(self):
        # Put card onto the discard pile
        firstcard = self.drawPile.takeCards(1)
        
        while firstcard.value == "Draw4" and firstcard.colour == "Wild":            
            self.drawPile.addCard(firstcard)
            self.drawPile.shuffleCards()
            firstcard = self.drawPile.takeCards(1)
        self.updateDiscardPile(firstcard)
        self.updateDrawPile()

    def drawCards(self, player, canvas, pile, imagepile):
        imagepile.clear()
        pile.clear()

        for widget in canvas.winfo_children():
            widget.destroy()

        for idx,card in enumerate(player.hand.getCards()):
            card_image = PhotoImage(file=card.get_image())
            imagepile.append(card_image)
            card_button = Button(canvas,image=imagepile[idx],compound=BOTTOM,text=card.get_name(),padx=5,command=lambda i=idx: self.cardCallback(i,player,pile))
            canvas.create_window(0, 0, window = card_button)
            pile.append(card_button)
            pile[idx].pack(side=LEFT)  
            
           # frame.configure(scrollregion=frame.bbox("all"))
    
    def drawPlayersCards(self, player):
        # Update players pile
        if player.playerid == 1:
            self.drawCards(player, self.player1Canvas, self.player1Pile, self.player1PileImages)
        else:
            self.drawCards(player, self.player2Canvas, self.player2Pile, self.player2PileImages)

    def updateDiscardPile(self, selected_card):
        # Update discard pile
        self.discardPile.addCard(selected_card)
        cimg = PhotoImage(file=selected_card.get_image())
        self.discardPileArea.configure(image=cimg)
        self.discardPileArea.image = cimg
        self.discardPileArea.config(text="Discard Pile - " + str(self.discardPile.getNumberofCards()))

    def updateDrawPile(self):
        # Update draw pile        
        self.drawPileArea.config(text="Draw Pile - " + str(self.drawPile.getNumberofCards()))

    def cardCallback(self, id, player,pile):
        selected_card = player.getHand().getCards()[id]
        
        # Check for legal move
        if not self.checkMove(selected_card, self.discardPile.getTopCard()):
            self.status.set("Illegal move - try again")
            return

        # Update discard pile
        self.updateDiscardPile(selected_card)        
        self.updateDrawPile()

        # Update players hand
        player.getHand().removeCard(id)
                
        # Update players pile
        self.drawPlayersCards(player)                              

        # Check if card played is a wild card
        if selected_card.value in self.WILDCARDS:            
            colour_chooser = DialogChooseColour(self.canvas)
            self.canvas.wait_window(colour_chooser.top)
            colour_choice = colour_chooser.colourChoice           
            self.discardPile.getTopCard().colour = colour_choice

        # Check if card played is a skip card        
        if selected_card.value in self.SKIPCARDS:
            # Check if card played is a draw card
            if selected_card.value in self.DRAWCARDS:
                no_of_cards = 2
                if selected_card.value == "Draw4":
                    no_of_cards = 4
                if self.checkDrawPileEmpty(no_of_cards):
                    cards = self.drawPile.takeCards(no_of_cards)
                    self.getNextPlayer().getHand().addCards(cards)
                    self.drawPlayersCards(self.getNextPlayer())
                    self.disablePlayersCards()
                self.next_turn(True)
        else:            
            self.next_turn(False)


    def drawPileCallback(self):
        # Take card from the draw pile
        if self.checkDrawPileEmpty(1):
            newcard = self.drawPile.takeCards(1)
            # Add to player's hand
            self.currentPlayer.hand.addCard(newcard)
            self.drawPlayersCards(self.currentPlayer)       

        self.updateDrawPile()
        self.next_turn()

    def checkDrawPileEmpty(self, no_of_cards):
        if (self.discardPile.getNumberofCards() + self.drawPile.getNumberofCards()) < no_of_cards:
            self.disableDrawPile()
            return False

        if self.drawPile.getNumberofCards() < no_of_cards:
            self.drawPile.addCards(self.discardPile.getCards())
            self.discardPile.removeCards()
            self.drawPile.shuffleCards()
            self.placeFirstCard()
            self.enableDrawPile()

        return True

    def checkMove(self,card,discardCard):
        # Check discard pile empty
        if not discardCard:
            return True
        # Check colour
        elif card.colour == discardCard.colour or card.colour == "Wild" or discardCard.colour == "Wild":
            return True
        # Check value
        elif card.value == discardCard.value:
            return True
        else:
            return False

    def next_turn(self, skipPlayers=False):  
        self.updateDrawPile()

        # Declare UNO
        if len(self.currentPlayer.hand.getCards()) == 1:
            self.status.set(self.currentPlayer.name  + " declares UNO!")

        if not self.currentPlayer.hand.getCards():
            self.status.set("WIN - " + self.currentPlayer.name)
            self.endGame()
            return

        if skipPlayers:
            return

        for player in self.players:                 
            if player.turn:                
                player.setTurn(False)
            else:
                player.setTurn(True)
                self.currentPlayer = player          
        self.disablePlayersCards()
        self.status.set("CURRENT PLAYER: " + self.currentPlayer.name)

    def disableDrawPile(self):
        self.drawPileArea.config(state="disabled")
    
    def enableDrawPile(self):
        self.drawPileArea.config(state="normal")

    def disablePlayersCards(self):
        cards = []
        if self.currentPlayer.playerid == 1:
            for card in self.player1Pile:
                card.config(state="normal")
            for card in self.player2Pile:
                card.config(state="disabled")
        else:
            cards = self.player2Pile
            for card in self.player2Pile:
                card.config(state="normal")
            for card in self.player1Pile:
                card.config(state="disabled")
        

    def chooseFirstPlayer(self):
        return random.choice(self.players)
    
    def getNextPlayer(self):
        for player in self.players:                 
            if not player.turn:
                return player 
        return players[0]

    def endGame(self):
        messagebox.showinfo("WINNER", self.currentPlayer.name + " WINS!")        
        self.status.destroy()
        app.canvas.destroy()
        app.__init__(root)


root = Tk()

app = GameWindow(root)

root.mainloop()

if app:
    root.destroy() # optional; see description below