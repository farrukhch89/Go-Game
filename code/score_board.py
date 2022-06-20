'''
    Farrukh Jahangeer 2960928
    Khusmanda Ramanjooloo 2953316
'''
from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, \
      QDialog  # TODO import additional Widget classes as desired
from PyQt5.QtCore import pyqtSlot
from piece import Piece

class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setFixedWidth(200)
        self.setFixedHeight(550)
        self.center()
        self.setWindowTitle('ScoreBoard')

        #create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        #create two labels which will be updated by signals
        self.label_clickLocation = QLabel("<strong>Click Location: </strong>")
        self.label_timeRemaining = QLabel("<strong>Time remaining: </strong>")
        self.label_playerTurn = QLabel("<strong>Turn: </strong>")
        self.label_whitePrisoners = QLabel("<strong>White Captured: </strong>")
        self.label_blackPrisoners = QLabel("<strong>Black Captured: </strong>")
        self.label_whiteTerritories = QLabel("<strong>White Territories: </strong>")
        self.label_blackTerritories = QLabel("<strong>Black Territories: </strong>")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_playerTurn)
        self.mainLayout.addWidget(self.label_whitePrisoners)
        self.mainLayout.addWidget(self.label_blackPrisoners)
        self.mainLayout.addWidget(self.label_whiteTerritories)
        self.mainLayout.addWidget(self.label_blackTerritories)
        self.setWidget(self.mainWidget)
        self.show()

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        # when the updatePrionersSignal is emitted in the board the updatePrisoners slot receives it
        board.updatePrionersSignal.connect(self.updatePrisoners)
        board.updateTerritoriesSignal.connect(self.updateTerritories)
        board.showNotificationSignal.connect(self.displaynotification)
        board.displaychangeturnSignal.connect(self.updateturn)

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText(clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "<strong>Time Remaining: </strong>" + str(timeRemainng)
        self.label_timeRemaining.setText(update)

    #display message notification
    def displaynotification(self, message):
        dlg = QDialog(self)
        dlg.setFixedWidth(300)
        dlg.setWindowTitle("Notification")
        self.modallayout = QVBoxLayout()
        self.modallayout.addWidget(QLabel(message))
        dlg.setLayout(self.modallayout)
        dlg.exec_()

    # update turn
    def updateturn(self, Piece):
        if (Piece == 1):
            self.label_playerTurn.setText("<strong>Current Turn: </strong> Black")

        elif (Piece == 2):
            self.label_playerTurn.setText("<strong>Current Turn: </strong> White")

    # update  and record prisoners
    def updatePrisoners(self, n, Player):
        if (Player == Piece.white):
            update = "<strong>White Captured:  </strong>" + n
            self.label_whitePrisoners.setText(update)

        elif (Player == Piece.black):
            update = "<strong>Black Captured:  </strong>" + n
            self.label_blackPrisoners.setText(update)

    # update and record area taken
    def updateTerritories(self, n, Player):
        if (Player == Piece.white):
            update = "<strong>White Territories: </strong>" + n
            self.label_whiteTerritories.setText(update)

        elif (Player == Piece.black):
            update = "<strong>Black Territories: </strong>" + n
            self.label_blackTerritories.setText(update)