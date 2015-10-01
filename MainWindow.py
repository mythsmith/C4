from PyQt4 import QtCore, QtGui
from C4.BoardScene import BoardScene
from C4.GameMatrix import GameMatrix
from C4.Storage import Storage
from C4.NewGame import NewGame

class MainWindow(QtGui.QMainWindow):
    def __init__(self, database=False):
        QtGui.QMainWindow.__init__(self)
        mb = self.menuBar()
        self.menu_game = mb.addMenu('Game')
        self.menu_game.addAction('New', self.new_game)
        self.menu_game.addAction('Save', self.save_game)
        self.tabs = QtGui.QTabWidget(parent = self)
        self.tabs.currentChanged.connect(self.change_tab)
        self.setCentralWidget(self.tabs)
        self.scenes = []
        self.user_maps = []
        
        self.storage = Storage(database=database)
        
    def save_finished(self):
        """If active game is finished, save and close its tab"""
        g = self.tabs.currentIndex()
        if g<0: return False
        scene = self.scenes[g]
        game = scene.game   
        if not game.winner_idx:
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
        
        user_uid = self.storage.add_users((user1,user2))
        user_map = {1:user_uid[user1],2:user_uid[user2]}
        self.user_maps.append(user_map)
        game = GameMatrix()
        scene = BoardScene(game)
        scene.setSceneRect(0,0,700,600)
        view = QtGui.QGraphicsView(scene)
        view.setMouseTracking(True)
        self.scenes.append(scene)
        name = str(len(self.scenes))
        
        self.tabs.addTab(view, name)
        game.start()
        
    
    def save_game(self):
        """Save game status into paused games and closes its tab."""
        g = self.tabs.currentIndex()
        scene = self.scenes.pop(g)
        game = scene.game
        game.pause()
        user_map = self.user_maps.pop(g)
        print 'SAVING',game, user_map
        self.storage.save_game(game, user_map)
        self.tabs.removeTab(g)
        
    
    def resume_game(self):
        """Display paused games and allow to select a game to be resumed"""
        pass
    
    def change_tab(self, new_index):
        """Changing the tab pauses all games and resume the currently active tab"""
        for i in range(self.tabs.count()):
            if i == new_index: 
                self.scenes[i].game.resume()
                continue
            self.scenes[i].game.pause()
    