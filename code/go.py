'''
    Farrukh Jahangeer 2960928
    Khusmanda Ramanjooloo 2953316
'''
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QAction, QMessageBox
from PyQt5.QtCore import Qt
from qtpy import QtCore
from board import Board
from score_board import ScoreBoard

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.setStyleSheet("background-color: #e5e5cc;")
        self.board = Board(self)
        self.board.setStyleSheet("background-color:#000000;")
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()

        # backgroud colour on score board
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.resize(950, 840)
        self.center()
        self.setWindowTitle('Go')
        self.menu() # display menu bar
        self.show()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)

    def menu(self):
        # set up menus
        mainMenu = self.menuBar()  # create and a menu bar

        # main menu stylesheet
        mainMenu.setStyleSheet("background-color: #ffffff; border: 1px solid #000000; font-weight: bold; font-size:20px;" )

        #reset
        resetAction = QAction("Reset", self)
        resetAction.setShortcut("Ctrl+R")  # set shortcut
        resetAction.triggered.connect(self.board.resetGame)
        resetMenu = mainMenu.addAction(resetAction)

        # pass menu
        passAction = QAction("Pass", self)
        passAction.setShortcut("Ctrl+P")  # set shortcut
        passMenu = mainMenu.addAction(passAction)
        passAction.triggered.connect(self.click)

        # help menu
        helpAction = QAction("Help", self)
        helpAction.setShortcut("Ctrl+H")  # set shortcut
        helpMenu = mainMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        # exit menu
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+E")  # set shortcut
        exitMenu = mainMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)


    # help message display rules
    def help(self):
        msg = QMessageBox()
        msg.setText(
                    "<p><strong>Welcome to Go Game</strong></p> "
                    "<p><strong>Rules: </strong></p>"
                    "<p>A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces (called stones), one taking the white stones, "
                    "the other taking black. The main object of the game is to use your stones to form territories "
                    "by surrounding vacant areas of the board. It is also possible to capture your opponent's stones by completely surrounding them.</p>"

                    "<p>Players take turns, placing one of their stones on a vacant point at each turn, with black playing first. Note that stones are placed "
                    "on the intersections of the lines rather than in the squares and once played stones are not moved. However they may be captured, in which case"
                    " they are removed from the board, and kept by the capturing player as prisoners.</p>"
                    
                    "<p><strong> ==>> To reset game press ( Ctrl + R ) or Reset <br>"
                    "<br>==>> To Exit game press ( Ctrl + E ) or Exit <br>"
                    "<br>==>> To Pass your turn press (Ctrl + P ) or Pass </strong></p>"

        )
        msg.setWindowTitle("Help")
        msg.exec_()

    # exit file
    def exit(self):
        QtCore.QCoreApplication.quit()

    #click method for pass
    def click(self):
        if self.getBoard().passEvent() == True: # link to board to count passcount and change turn
            self.close()
        self.update()