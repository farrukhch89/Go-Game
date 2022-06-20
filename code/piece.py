'''
    Farrukh Jahangeer 2960928
    Khusmanda Ramanjooloo 2953316
'''
class Piece(object):
    NoPiece = 0
    black = 1
    white = 2

class Stone(object):
    Piece = Piece.NoPiece
    liberties = 0
    x = -1
    y = -1

    def __init__(self, Piece,x,y):  # a contstuctor initialising variables
        self.Piece = Piece
        self.liberties = 0
        self.x = x
        self.y = y

    def getPiece(self): # a methoad to return Piece
        return self.Piece

    def getLiberties(self): # a method to return Liberties
        return self.liberties

    def setLiberties(self,liberties):   # a method to set Liberties
        self.liberties =liberties

    def getup(self,boardArray):
        if self.y == 0:
            return None
        else:
            return boardArray[self.y-1][self.x] # move y coordinate upwards

    def getright(self,boardArray):
        if self.x == 6:
            return None
        else:
            return boardArray[self.y][self.x+1] # move x coordinate to the right

    def getleft(self,boardArray):
        if self.x == 0:
            return None
        else :
            return boardArray[self.y][self.x-1] # move x coordinate to the left

    def getdown(self,boardArray):
        if self.y == 6:
            return None
        else :
            return boardArray[self.y+1][self.x] # move y coordinate to downwards