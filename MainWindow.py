from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        mb = self.menuBar()
        self.menu_game = mb.addMenu('Game')
        self.menu_game.addAction('New', self.new_game)
        self.menu_game.addAction('Pause', self.pause_game)
        self.tabs = QtGui.QTabWidget(parent = self)
        self.setCentralWidget(self.tabs)
        
        
    
    def new_game(self):
        """Show new game dialog and start it"""
        pass
    
    def pause_game(self):
        """Save game status into paused games and exit it"""
        pass
    
    def resume_game(self):
        """Display paused games and allow to select a game to be resumed"""
        pass
    