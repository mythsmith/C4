from PyQt4 import QtCore, QtGui
from C4.Storage import Storage
from C4.NewGame import NewGame
from C4.GameMatrix import GameMatrix
from C4.GameWidget import GameWidget
from C4.ScoreBoard import ScoreBoard
from C4.SavedGames import SavedGames

def dialogize(widget, parent=None):
    """Puts `widget` into a QDialog. Returns the new QDialog."""
    d = QtGui.QDialog(parent=parent)
    d.resize(widget.width() + 50, widget.height() + 50)
    lay = QtGui.QVBoxLayout()
    lay.addWidget(widget)
    d.setLayout(lay)
    return d
    

class MainWindow(QtGui.QMainWindow):
    
    """Main application window to manage games and scores"""
    
    def __init__(self, database=False):
        QtGui.QMainWindow.__init__(self)
        mb = self.menuBar()
        self.menu_game = mb.addMenu('Game')
        self.menu_game.addAction('New', self.new_game)
        self.menu_game.addAction('Save', self.save_game)
        self.menu_scoreboard = mb.addMenu('Scoreboard')
        self.menu_scoreboard.addAction('Scoreboard', self.show_scoreboard)
        self.menu_scoreboard.addAction('Saved Games', self.show_saved_games)
        self.menu_scoreboard.addAction('Reset', self.reset_storage)
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
        """Show new game dialog and start it in a new tab"""
        self.save_finished()
        
        dia = NewGame(self)
        r = dia.exec_()
        users = [unicode(u.text()) for u in dia.users]
        players = len(users)
        if len(set(users)) != players:
            QtGui.QMessageBox.warning(self, 'User names cannot be equal', 'You entered equal user names.\n Please enter different user names.')
            return
        
        user_uid = self.storage.add_users(users)  # name:uid
        user_map = {}  # player:uid
        pid = 1
        for name in users:
            user_map[pid] = user_uid[name]
            pid += 1
        shape = [dim.value() for dim in dia.dims]
        game = GameMatrix(shape=tuple(shape), players=players, goal=dia.goal.value())
        self.add_game(game, user_map, user_uid)
        
    def add_game(self, game, user_map, user_uid):
        """Add a new game tab"""
        gw = GameWidget(game, user_map, user_uid, parent=self)
        self.game_widgets.append(gw)
        name = ', '.join(user_uid.keys())
        name += ' ({})'.format(len(self.game_widgets))
        self.tabs.addTab(gw, name)
        # If there are already moves, sync everything
        if game.moves:
            gw.scene.sync()
        if not game.winner_idx:
            game.start()
        return gw
    
    def save_game(self):
        """Save game status into paused games and closes its tab."""
        g = self.tabs.currentIndex()
        gw = self.game_widgets.pop(g)
        game = gw.game
        game.pause()
        print 'SAVING', game, gw.user_map
        self.storage.save_game(game, gw.user_map, gw.user_uid)
        self.tabs.removeTab(g)
        
    def resume_game(self, gid):
        """Load a paused/completed game by gid"""
        r = self.storage.search_gid(gid)
        if r is False:
            print 'NO GAME FOUND', gid
        game, user_map, user_uid = r
        game.validate()
        self.add_game(game, user_map, user_uid)
    
    def change_tab(self, new_index):
        """Changing the tab pauses all games and resume the currently active tab"""
        for i in range(self.tabs.count()):
            if i == new_index: 
                self.game_widgets[i].game.resume()
                continue
            self.game_widgets[i].game.pause()
            
    def show_scoreboard(self):
        """Show scoreboard widget"""
        sb = ScoreBoard(self.storage.database)
        d = dialogize(sb, self)
        d.exec_()
    
    _saved_games = False
    def show_saved_games(self):
        """Show SavedGames widgets and connect selections"""
        if self._saved_games:
            self._saved_games.close()
        sg = SavedGames(self.storage.database)
        d = dialogize(sg, self)
        d.show()
        # Keep reference
        self._saved_games = d
        sg.resume_game.connect(self.resume_game)
        
    def reset_storage(self):
        """Ask if to really delete the database and proceeds"""
        q = QtGui.QMessageBox.question(self, 'Deleting scoreboard',
                                      'Are you really sure you would like to delete the scoreboard with all saved games?',
                                      QtGui.QMessageBox.Ok | QtGui.QMessageBox.No)
        if q == QtGui.QMessageBox.Ok:
            self.storage.reset()
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    QtGui.qApp.exec_()
