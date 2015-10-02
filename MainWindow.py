from PyQt4 import QtCore, QtGui
from C4.Storage import Storage
from C4.NewGame import NewGame
from C4.GameMatrix import GameMatrix
from C4.GameWidget import GameWidget
from C4.ScoreBoard import ScoreBoard


class MainWindow(QtGui.QMainWindow):
    def __init__(self, database=False):
        QtGui.QMainWindow.__init__(self)
        mb = self.menuBar()
        self.menu_game = mb.addMenu('Game')
        self.menu_game.addAction('New', self.new_game)
        self.menu_game.addAction('Save', self.save_game)
        self.menu_game.addAction('Scoreboard', self.show_scoreboard)
        self.menu_game.addAction('Saved Games', self.show_saved_games)
        self.tabs = QtGui.QTabWidget(parent=self)
        self.tabs.currentChanged.connect(self.change_tab)
        self.setCentralWidget(self.tabs)
        self.game_widgets = []
        
        self.storage = Storage(database=database)
        
        self.resize(800, 700)
        
    def save_finished(self):
        """If active game is finished, save and close its tab.
        Otherwise, pause it."""
        g = self.tabs.currentIndex()
        if g < 0: return False
        gw = self.game_widgets[g]
        game = gw.game   
        if not game.winner_idx:
            game.pause()
            return False
        self.save_game()
        return True    
        
    def new_game(self):
        """Show new game dialog and start it"""
        self.save_finished()
        
        dia = NewGame(self)
        r = dia.exec_()
        user1 = unicode(dia.user1.text())
        user2 = unicode(dia.user2.text())
        if user1 == user2:
            QtGui.QMessageBox.warning(self, 'User names cannot be equal', 'You entered two equal user name.\n Please enter different user names.')
            return
        
        user_uid = self.storage.add_users((user1, user2))  # name:uid
        user_map = {1:user_uid[user1], 2:user_uid[user2]}  # player:uid
        shape = (dia.height.value(), dia.width.value())
        game = GameMatrix(shape=shape, goal=dia.goal.value())
        gw = GameWidget(game, user_map, user_uid, parent=self)
        self.game_widgets.append(gw)
        name = str(len(self.game_widgets))
        self.tabs.addTab(gw, name)
        game.start()
        
    
    def save_game(self):
        """Save game status into paused games and closes its tab."""
        g = self.tabs.currentIndex()
        gw = self.game_widgets.pop(g)
        game = gw.game
        game.pause()
        print 'SAVING', game, gw.user_map
        self.storage.save_game(game, gw.user_map)
        self.tabs.removeTab(g)
        
    
    def resume_game(self):
        """Display paused games and allow to select a game to be resumed"""
        pass
    
    def change_tab(self, new_index):
        """Changing the tab pauses all games and resume the currently active tab"""
        for i in range(self.tabs.count()):
            if i == new_index: 
                self.game_widgets[i].game.resume()
                continue
            self.game_widgets[i].game.pause()
            
    def show_scoreboard(self):
        sb = ScoreBoard(self.storage.database, parent=self)
        sb.show()
        self._scoreboard = sb
    
    def show_saved_games(self):
        pass
    
