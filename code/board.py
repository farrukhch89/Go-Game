'''
    Farrukh Jahangeer 2960928
    Khusmanda Ramanjooloo 2953316
'''
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor
from piece import Piece
from piece import Stone
from game_logic import GameLogic

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    updatePrionersSignal = pyqtSignal(str, int) # signal sent when prisoner is updated.
    updateTerritoriesSignal = pyqtSignal(str, int) # signal sent territory is updated.
    showNotificationSignal = pyqtSignal(str)    # signal sent for notification message.
    displaychangeturnSignal = pyqtSignal(int)   # signal sent when swap player is updated.

    boardWidth = 7  # board width is set to 7
    boardHeight = 7  # board height is set to 7
    timerSpeed = 1000  # the timer updates ever 1 second
    counter = 120  # countdown is set to two minutes

    gamelogic = GameLogic()
    passcount = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self._history = [] # create a list of game history

    def initBoard(self):
        '''initiates board'''

        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer
        # creating a 2d int/Piece array to store the state of the game
        self.boardArray = [[Stone(Piece.NoPiece,i,j) for i in range(self.boardWidth)] for j in range(self.boardHeight)]
        self.gamelogic = GameLogic()
        self.printBoardArray()

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''

        print("boardArray:")
        for row in self.boardArray: # running double loop of boardArray
            for cell in row:
                if cell.Piece == Piece.NoPiece: # if NoPiece then print *
                    print(" * ", end=" ")
                if cell.Piece == Piece.white:   # if white then print 0
                    print(" 0 ", end=" ")
                if cell.Piece == Piece.black:   # if black then print 1
                    print(" 1 ", end=" ")
        print('\n')
        # print('\n'.join(['\t'.join([ str(cell ) for cell in row]) for row in self.boardArray]))

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return (self.contentsRect().width() - 49) / self.boardWidth #-49 to make space beside board so whole stone can be seen
    def squareHeight(self):
        '''returns the height of one square of the board'''
        return (self.contentsRect().height() - 49) / self.boardHeight #-49 to make space beside board so whole stone can be seen

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.counter == 0:   # if time is up
                self.shownotification("<strong>Timer Ran out : Game Over </strong>")  # show this message
                if self.gamelogic.turn == Piece.white:  # if next turn is white
                    self.shownotification("<strong> Black Player Wins </strong>")  # black wins, capturing more territories
                else:
                    self.shownotification("<strong> White Player Wins </strong>") # else white wins
                self.close()
            self.counter -= 1
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handeling other wise pass it to the super class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)    # initialising painter and passing it as a parameter
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "<strong>Click Location: </strong> <br> [" + str(event.x()) + "," + str(event.y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.mousePosToColRow(event)    # a method that converts the mouse click to a row and col.
        self.clickLocationSignal.emit(clickLoc)

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        xpos = event.x()    # assigning mouse click x & y event to variables
        ypos = event.y()
        xcoordinate = xpos / self.squareWidth() # setting up x & y coordinates
        ycoordinate = ypos / self.squareHeight()
        ''' The round() method returns the floating point number rounded off to the given ndigits
         digits after the decimal point. If no digits is provided, it rounds off the number to the 
         nearest integer.'''
        xp = round(xcoordinate) - 1
        yp = round(ycoordinate) - 1
        self.gamelogic.updateparams(self.boardArray, xp, yp) # passing parameters to update current variables.
        if (self.trytoplacestone()):    # if move is not suicide
            self.placeStone()   # place the stone on the board
            self.updatePrisonersandTerritories() # update prisoner & territory if any
        self.update()

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # setting the default colour of the brush
        brush = QBrush(Qt.Dense1Pattern)  # calling SolidPattern to a variable
        brush.setColor(QColor(255, 179, 102))  # setting color yellowish brown
        painter.setBrush(brush)  # setting brush color to painter
        for row in range(0, Board.boardHeight +1): # create an extra row of square
            for col in range(0, Board.boardWidth +2): # create 2 extra column of square
                painter.save()
                colTransformation = self.squareWidth() * col  # setting this value equal the transformation in the column direction
                rowTransformation = self.squareHeight() * row  # setting this value equal the transformation in the row direction

                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(col, row, self.squareWidth(), self.squareHeight(),
                                 brush)  # passing the above variables and methods as a parameter
                painter.restore()


    def drawPieces(self, painter):
        '''draw the prices on the board'''
        color = Qt.transparent  # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                ''' the string translate() method returns a string where each row and col is mapped to 
                its corresponding character in the translation table '''
                painter.translate(((self.squareWidth()) * row) + self.squareWidth() / 2,
                                  (self.squareHeight()) * col + self.squareHeight() / 2)
                color = QColor(0, 0, 0)  # set the color is unspecified

                if self.boardArray[col][row].Piece == Piece.NoPiece:  # if piece in array == 0
                    color = QColor(Qt.transparent)  # color is transparent

                elif self.boardArray[col][row].Piece == Piece.black:  # if piece in array == 1
                    color = QColor(Qt.black)  # set color to black

                elif self.boardArray[col][row].Piece == Piece.white:  # if piece in array == 2
                    color = QColor(Qt.white)  # set color to white

                painter.setPen(color)  # set pen color to painter
                painter.setBrush(color)  # set brush color to painter
                radius = (self.squareWidth() - 2) / 2
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()

    def trytoplacestone(self):
        '''  a methoad for checking rules before placing stone  '''
        if self.gamelogic.checkvacant():    # check if the position is vacant or not
            if self.gamelogic.checkforSuicide():  # if the move is suicide
                self.shownotification("<strong>Suicide Move Not Allowed</strong>")   # show message
                return False
            else:
                return True
        else:
            self.shownotification("<strong>Position Already Taken</strong>")
            return False

    def placeStone(self):
        self.gamelogic.placestone()  # place the stone on the board
        self.gamelogic.updateLiberties()  # update the liberties
        message = self.gamelogic.updatecaptures2()
        if (message != None):   # if no liberties left of the neighbouring stones
            self.shownotification(message)
            print("Stone Killed")
            self.gamelogic.updateLiberties()  # update the liberties again in case of capture
        self.gamelogic.updateTeritories()   # update territories
        self._push_history()    # push it to the history list
        if not self._check_for_ko():    # if board state is not in KO
            self.passcount = 0  # change the pass count to reflect that any one of the player has taken a turn
            self.changeturn()  # change the turn to next player in case of successful position of piece
        else:
            if self.gamelogic.turn == Piece.black:  # revert back the black prisoner count
                self.gamelogic.blackprisoners = self.gamelogic.blackprisoners - 1
            else:   # # revert back the white prisoner count
                self.gamelogic.whiteprisoners = self.gamelogic.whiteprisoners - 1
            # revert back the board to previous state
            self._pop_history(self._history[-2])
            # update the liberties and territories
            self.gamelogic.updateLiberties()
            self.gamelogic.updateTeritories()
            # push this state to history
            self._push_history()

    def _push_history(self):
        """
        Pushes game state onto history.
        """
        self._history.append(self.copyboard())  # adds it to the end of the list
        try:
            print("Last move") # prints the last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self._history[-1]]))
            print("Second Last")  # prints the second last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self._history[-2]]))
            print("3rd Last")   # prints the third last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self._history[-3]]))
        except IndexError:
            return None

    def _pop_history(self, previousstate):
        #Pops and loads game state from history
        rowindex = 0
        for row in previousstate:
            colindex = 0
            for cell in row:
                if cell.Piece == 1: # if piece is 1, assign black stone to the row and col index of boardArray
                    self.boardArray[rowindex][colindex] = Stone(Piece.black, colindex, rowindex)
                elif cell.Piece == 2: # if piece is 2, assign white stone to the row and col index of boardArray
                    self.boardArray[rowindex][colindex] = Stone(Piece.white, colindex, rowindex)
                elif cell.Piece == 0: # if piece is 0, assign null to the row and col index of boardArray
                    self.boardArray[rowindex][colindex] = Stone(Piece.NoPiece, colindex, rowindex)
                colindex = colindex + 1 # move to the next col index position
            rowindex = rowindex + 1 # move to the next row index position
        print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.boardArray]))
        # converting the value of col and row in boardArray to string before printing

    def copyboard(self):
        ''' A method to store and return the current state of the board '''
        copyofboard = [[Stone(Piece.NoPiece, i, j) for i in range(7)] for j in range(7)] # nested loop of Stone class to the size of board range.
        rowindex = 0
        for row in self.boardArray:
            colindex = 0
            for cell in row:
                if cell.Piece == Piece.black:
                    copyofboard[rowindex][colindex] = Stone(Piece.black, colindex, rowindex) # places the current value of black stone to the copyofboard row and col index
                elif cell.Piece == Piece.white:
                    copyofboard[rowindex][colindex] = Stone(Piece.white, colindex, rowindex) # places the current value of white stone to the copyofboard row and col index
                elif cell.Piece == Piece.NoPiece:
                    copyofboard[rowindex][colindex] = Stone(Piece.NoPiece, colindex, rowindex) # places the current value of Stone to the copyofboard row and col index
                colindex = colindex + 1 # increment col index
            rowindex = rowindex + 1 # increment row index
        return copyofboard

    def _check_for_ko(self):
        # Checks if board state is in KO.
        try:
            if self.compareboards(self._history[-1], self._history[-3]):
                self.shownotification('KO: Cannot make a move')
                return True  # return true if move is KO
        except IndexError:
            # Insufficient history...let this one slide
            pass
        return False  # return false in case its not KO

    def compareboards(self, current, previous):
        rowindex = 0
        for row in previous:
            colindex = 0
            for cell in row:
                if cell.Piece != current[rowindex][colindex].Piece:
                    return False  # return false if found a single position different
                colindex = colindex + 1
            rowindex = rowindex + 1
        return True  # else return true

    def changeturn(self):
        self.gamelogic.changeturn()  # function to swap turns
        #sself.Scoreboard.updateturn()
        self.counter = 120  # reset the timer for the next player
        self.displaychangeturnSignal.emit(self.gamelogic.turn)  # signal sent to display Current Turn message

    #update prison
    def updatePrisonersandTerritories(self):
        self.updatePrionersSignal.emit(self.gamelogic.getwhitePrisoner(), Piece.white)
        self.updatePrionersSignal.emit(str(self.gamelogic.getblackPrisoner()), Piece.black)
        self.updateTerritoriesSignal.emit(str(self.gamelogic.getblackTerritories()), Piece.black)
        self.updateTerritoriesSignal.emit(str(self.gamelogic.getwhiteTerritories()), Piece.white)

    # declaring winner
    def declarewinner(self):
        whitescore = self.gamelogic.getScore(Piece.white)   # gets the current score of white
        blackscore = self.gamelogic.getScore(Piece.black)    # gets the current score of black
        self.shownotification("<strong>Scores  <br> White : </strong>" + str(whitescore) + " <strong> <br> Black : </strong> " + str(blackscore)) # a notification for white and black score
        if whitescore > blackscore:
            self.shownotification("<strong>WHITE WINS</strong>")
        elif whitescore < blackscore:
            self.shownotification("<strong>BLACK WINS</strong>")
        else:
            self.shownotification("<strong>ITS A TIE</strong>")

    def getScore(self, Piece):
        return self.gamelogic.getScore(Piece) #  retrieve the sum of territories and prisoners

    def shownotification(self, message):
        self.showNotificationSignal.emit(message)

    def resetGame(self):
        '''clears pieces from the board'''
        print("Game Reset")
        self.shownotification("<strong>Game Reset</strong>")
        self.boardArray = [[Stone(Piece.NoPiece, i, j) for i in range(self.boardWidth)] for j in
                           range(self.boardHeight)]
        self.gamelogic.whiteprisoners = 0 #set captured to 0
        self.gamelogic.blackprisoners = 0 #set captured to 0
        self.gamelogic.whiteterritories = 0 #set territories to 0
        self.gamelogic.blackterritories = 0 #set territories to 0
        self.gamelogic.turn = Piece.black
        self.displaychangeturnSignal.emit(self.gamelogic.turn)

    def passEvent(self):
        self.shownotification("<strong> Move Passed </strong>")
        self.passcount = self.passcount + 1
        self.gamelogic.changeturn()
        self.displaychangeturnSignal.emit(self.gamelogic.turn)  # signal sent to display Current Turn message
        if self.passcount == 2:  #check if both players have passed their turns, this count is set to 0 after successfull placement of stone
            self.shownotification("<strong> GAME OVER </strong>")
            self.declarewinner()
            return True
        return False