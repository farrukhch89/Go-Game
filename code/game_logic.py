'''
    Farrukh Jahangeer 2960928
    Khusmanda Ramanjooloo 2953316
'''
from piece import Piece
from piece import Stone
class GameLogic():
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    turn = Piece.black
    Xpos = 0
    Ypos = 0
    boardArray = 0
    blackprisoners = 0
    whiteprisoners = 0
    blackterritories = 0
    whiteterritories = 0

    def updateparams(self,boardArray,xpos,ypos):
        # update current variables
        self.Xpos = xpos
        self.Ypos = ypos
        self.boardArray=boardArray

    def checklogic(self,boardArray,xpos,ypos):
        # update current variables
        self.Xpos = xpos
        self.Ypos = ypos
        self.boardArray=boardArray

    def checkvacant(self):
        # check if the position is vacant
        if self.boardArray[self.Ypos][self.Xpos].Piece==Piece.NoPiece :
            return True
        else:
            return False

    def changeturn(self):
        # function to swap turns
        print("Turn Changed")
        if self.turn == Piece.white:
            self.turn = Piece.black
        else:
            self.turn = Piece.white

    def placestone(self):
        # function to place the stone on the board
        if self.turn == Piece.white:
            self.boardArray[self.Ypos][self.Xpos].Piece = Piece.white

        else:
            self.boardArray[self.Ypos][self.Xpos].Piece = Piece.black

        print("Liberties = " + str(self.boardArray[self.Ypos][self.Xpos].liberties) + "x pos = " + str(
            self.boardArray[self.Ypos][self.Xpos].x) + "y pos = " + str(self.boardArray[self.Ypos][self.Xpos].y))

    def updateLiberties(self):
        # update the liberties of all the available stones
        count = 0
        for row in self.boardArray :
            for cell in row :
                count=0
                if cell.Piece != Piece.NoPiece:
                    Stonecolor=cell.Piece

                    if cell.getup(self.boardArray) != None and (cell.getup(self.boardArray).Piece == Stonecolor or cell.getup(self.boardArray).Piece == Piece.NoPiece) :
                        count=count+1
                    if cell.getright(self.boardArray) != None and (cell.getright(self.boardArray).Piece == Stonecolor or cell.getright(self.boardArray).Piece == Piece.NoPiece) :
                        count=count+1
                    if cell.getleft(self.boardArray) != None and (cell.getleft(self.boardArray).Piece == Stonecolor or cell.getleft(self.boardArray).Piece == Piece.NoPiece) :
                        count=count+1
                    if cell.getdown(self.boardArray) != None and (cell.getdown(self.boardArray).Piece == Stonecolor or cell.getdown(self.boardArray).Piece == Piece.NoPiece) :
                        count=count+1
                    cell.setLiberties(count)

    def updatecaptures(self):
        # update captures of entire board, remove captured stone
        for row in self.boardArray :
            for cell in row :
                if(cell.liberties==0 and cell.Piece != Piece.NoPiece):
                    if(cell.Piece== Piece.white):
                        self.blackprisoners=self.blackprisoners+1
                        self.boardArray[cell.y][cell.x]=Stone(Piece.NoPiece,cell.x,cell.y)
                        return "<strong> White Stone Captured </strong>"
                    elif(cell.Piece== Piece.black):
                        self.whiteprisoners=self.whiteprisoners+1
                        self.boardArray[cell.y][cell.x] = Stone(Piece.NoPiece, cell.x, cell.y)
                        return "<strong> Black Stone Captured </strong>"
    #check liberties before capture
    def updatecaptures2(self):
        # function to check if any of the neighbouring stones of the current placement has 0 liberties left , if yes then capture them
        if self.boardArray[self.Ypos][self.Xpos].getup(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getup(self.boardArray).liberties == 0 and self.boardArray[self.Ypos][
                self.Xpos].getup(self.boardArray).Piece != Piece.NoPiece :
            return self.capturePiece(self.Xpos,self.Ypos-1)

        elif  self.boardArray[self.Ypos][self.Xpos].getright(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getright(self.boardArray).liberties == 0 and self.boardArray[self.Ypos][
                self.Xpos].getright(self.boardArray).Piece != Piece.NoPiece :
            return self.capturePiece(self.Xpos+1, self.Ypos)

        elif  self.boardArray[self.Ypos][self.Xpos].getleft(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getleft(self.boardArray).liberties == 0 and self.boardArray[self.Ypos][
                self.Xpos].getleft(self.boardArray).Piece != Piece.NoPiece :
            return self.capturePiece(self.Xpos-1, self.Ypos)

        elif  self.boardArray[self.Ypos][self.Xpos].getdown(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getdown(self.boardArray).liberties == 0 and self.boardArray[self.Ypos][
                self.Xpos].getdown(self.boardArray).Piece != Piece.NoPiece :
            return self.capturePiece(self.Xpos, self.Ypos+1)

    #capture
    def capturePiece(self,xpos,ypos):
        # captures a piece at the given position
        if self.boardArray[ypos][xpos].Piece == 1:  # if the piece is black
            self.whiteprisoners = self.whiteprisoners + 1
            self.boardArray[ypos][xpos] = Stone(Piece.NoPiece, xpos, ypos)
            return "<strong> Black Stone Captured  </strong>"

        else:  # if the piece is white
            self.blackprisoners = self.blackprisoners + 1
            self.boardArray[ypos][xpos] = Stone(Piece.NoPiece, xpos, ypos)
            return "<strong> White Stone Captured </strong>"

    # suicide check
    def checkforSuicide(self):
        oppositeplayer=Piece.NoPiece
        if self.turn==Piece.white :
            oppositeplayer=Piece.black
        else :
            oppositeplayer =Piece.white
        count=0
        # counts the neighbouring positions for opposite stones or nulls(end of board)
        if self.boardArray[self.Ypos][self.Xpos].getup(self.boardArray) == None or self.boardArray[self.Ypos][self.Xpos].getup(self.boardArray).Piece == oppositeplayer :
            count=count+1
        if self.boardArray[self.Ypos][self.Xpos].getleft(self.boardArray) == None or self.boardArray[self.Ypos][self.Xpos].getleft(self.boardArray).Piece == oppositeplayer :
            count = count + 1
        if self.boardArray[self.Ypos][self.Xpos].getright(self.boardArray) == None or self.boardArray[self.Ypos][self.Xpos].getright(self.boardArray).Piece == oppositeplayer :
            count = count + 1
        if self.boardArray[self.Ypos][self.Xpos].getdown(self.boardArray) == None or self.boardArray[self.Ypos][self.Xpos].getdown(self.boardArray).Piece == oppositeplayer :
            count = count + 1

        if(count==4) : # this means all side are of opposite color or end of board
            # now checking if any of the neighbours have a single liberty, if they do then by placing this stone, their liberties would turn to zero so it wont be suicide
            if self.boardArray[self.Ypos][self.Xpos].getup(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getup(self.boardArray).liberties == 1:
                return False
            if self.boardArray[self.Ypos][self.Xpos].getleft(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getleft(self.boardArray).liberties == 1:
                return False
            if self.boardArray[self.Ypos][self.Xpos].getright(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getright(self.boardArray).liberties == 1:
                return False
            if self.boardArray[self.Ypos][self.Xpos].getdown(self.boardArray) != None and self.boardArray[self.Ypos][
                self.Xpos].getdown(self.boardArray).liberties == 1:
                return False
            return True
        else :
            return False

    def getwhitePrisoner(self):
        return str(self.whiteprisoners)

    def getblackPrisoner(self):
        return str(self.blackprisoners)

    def getwhiteTerritories(self):
        return str(self.whiteterritories)

    def getblackTerritories(self):
        return str(self.blackterritories)

    def updateTeritories(self):
        # update the current positions occupied by each player
        countwhite = 0
        countblack = 0
        for row in self.boardArray:
            for cell in row:
                if cell.Piece == Piece.white:
                    countwhite = countwhite + 1
                elif cell.Piece == Piece.black:
                    countblack = countblack+1
        self.blackterritories = countblack
        self.whiteterritories = countwhite

    def getScore(self,Piece):
        if Piece==2:
            return self.whiteterritories+self.whiteprisoners
        else:
            return self.blackterritories+ self.blackprisoners